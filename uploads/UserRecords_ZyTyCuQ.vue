<script setup>
import { onBeforeMount, ref, computed, watchEffect } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { useRoute, useRouter } from 'vue-router';
import useUserStore from '../stores/userStore';
import { storeToRefs } from 'pinia';
import { times } from 'lodash';

const router = useRouter();
const userStore = useUserStore();
const { userId, isSuperUser, isAuthenticated } = storeToRefs(userStore);
const records = ref([]);
const errorText = ref('');
const loading = ref(false);
const recordStatuses = ref({});
const recordsPagination = ref({
    page: 1,
    pageSize: 5,
    totalCount: 0,
    hasNextPage: false,
    hasPreviousPage: false,
});

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
});
watchEffect(async()=> {
    if(!isAuthenticated.value)
  {
      router.push('/login');
        return
   }
  await fetchUserRecords();
});

async function fetchUserRecords() {
  loading.value = true;
  try {
     const response = await axios.get(`/api/records/`, {
          params: {
           ordering: '-time',
           author: userId.value,
           page: recordsPagination.value.page,
           page_size: recordsPagination.value.pageSize
      }
    });
     records.value = response.data.results;
        recordsPagination.value.totalCount = response.data.count;
        recordsPagination.value.hasNextPage = response.data.next !== null;
        recordsPagination.value.hasPreviousPage = response.data.previous !== null;
       if (records.value && records.value.length > 0) {
          await updateRecordStatuses(records.value);
        }
  } catch (error) {
    console.error('Ошибка загрузки записей пользователя:', error);
    errorText.value = 'Ошибка загрузки записей пользователя';
  } finally {
        loading.value = false;
  }
}
async function updateRecordStatuses(newRecords) {
    for (const record of newRecords) {
       const feedback = await fetchFeedback(record)
       recordStatuses.value[record.id] =  getRecordStatus(record,feedback)
    }
}

function onRecordClick(record, status) {
    if (status === 'green') {
        router.push(`/records/${record.id}`);
    } else if (status === 'red') {
        router.push(`/edit-record/${record.id}`);
    }
}

function formatDateTime(dateTimeString) {
  if (!dateTimeString) {
    return '';
  }
  try {
    const date = new Date(dateTimeString);
    if (isNaN(date.getTime())) {
      console.error('Неверный формат даты:', dateTimeString);
      return 'Неверная дата';
    }
    const options = {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    };
    return new Intl.DateTimeFormat('ru-RU', options).format(date);
  } catch (error) {
    console.error('Ошибка при форматировании даты:', error);
    return 'Неверная дата';
  }
}
async function fetchFeedback(record) {
    try {
         const response = await axios.get(`/api/feedbacks/?records_FK=${record.id}`);
        if (response.data &&  Array.isArray(response.data) && response.data.length > 0) {
          return response.data[0];
        } 
    } catch (error) {
         console.error('Ошибка загрузки обратной связи:', error);
    }
  return null;
}
 function getRecordStatus(record,feedback) {
    if (record.is_published) {
        return 'green'; // Запись опубликована - зелёный
    }
    if (!feedback) {
        return 'yellow'; // Нет комментария - жёлтый
    }
    try{
        const recordTime = new Date(record.time);
        const feedbackTime = new Date(feedback.time);
        if(feedbackTime > recordTime){
           return 'red';  // Комментарий позже публикации - красный
        }
    }
    catch(error){
          console.error('Ошибка проверки даты', error);
    }
      return 'yellow';
};
 function handleRecordsPageChange(page) {
    recordsPagination.value.page = page;
    fetchUserRecords();
  }

   const hasNextPage = computed(() => {
            return recordsPagination.value.page * recordsPagination.value.pageSize < recordsPagination.value.totalCount;
        });

        const hasPreviousPage = computed(() => {
            return recordsPagination.value.page > 1;
        });
         const totalPages = computed(()=> {
             return Math.ceil(recordsPagination.value.totalCount/recordsPagination.value.pageSize);
        })
         function handlePageChange(page) {
            if(page > 0 && page <=  totalPages.value){
                handleRecordsPageChange(page);
            }
        }
</script>
<template>
  <div class="user-records-container">
    <h2 class="text-white">Ваши публикации</h2>
         <div v-if="loading">
                <p class="text-white">Загрузка публикаций...</p>
            </div>
    <div v-else-if="records.length > 0" >
         <div v-for="record in records" :key="record.id" class="record-item"
             :class="{'record-item-clickable': recordStatuses[record.id] !== 'yellow' }"
             @click="onRecordClick(record,recordStatuses[record.id])"
         >
            <div class="record-content">
                <h4 class="record-headline text-white">{{ record.headline }}</h4>
                  <p class="record-date text-white">Дата публикации: {{ formatDateTime(record.time) }}</p>
                  <div class="status">
                       <span :class="{'status-yellow': recordStatuses[record.id] === 'yellow',
                                  'status-green': recordStatuses[record.id] === 'green',
                                   'status-red': recordStatuses[record.id] === 'red'}">
                        </span>
                     <span v-if="recordStatuses[record.id] === 'red'" class="text-white">
                        Ждёт правок
                      </span>
                         <span v-else-if="recordStatuses[record.id] === 'yellow'" class="text-white">
                         Ждёт проверки
                       </span>
                         <span v-else-if="record.is_published"  class="text-white">
                         Опубликовано
                      </span>
                  </div>
                </div>
           </div>
           <!--  Встроенный шаблон пагинации  -->
           <div class="pagination" v-if="recordsPagination.totalCount > recordsPagination.pageSize">
             <button class="btn btn-secondary" :disabled="!hasPreviousPage" @click="handlePageChange(recordsPagination.page - 1)">
                    <i class="bi bi-arrow-left"></i> Назад
                </button>
                <span class="text-white">{{ recordsPagination.page }} / {{ totalPages }}</span>
                <button  class="btn btn-secondary" :disabled="!hasNextPage" @click="handlePageChange(recordsPagination.page + 1)">
                    Вперед <i class="bi bi-arrow-right"></i>
                </button>
          </div>
      </div>
        <div v-else>
            <p class="text-white">Нет публикаций</p>
        </div>
      <p v-if="errorText" class="text-danger mt-1">{{ errorText }}</p>
  </div>
</template>
<style scoped>
.user-records-container {
    max-width: 1000px;
    margin: 20px auto;
    padding: 20px;
    border-radius: 1rem;
    background-color: #343a40;
}
.record-item{
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
   background-color: #495057;
   display: flex;
   align-items: center;
}
.record-item:hover {
    background-color: #49545d;
}
.record-content{
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
    flex: 1;
}
.record-headline{
  font-size: 1.5rem;
}
.status{
    display: flex;
    gap: 5px;
    align-items: center;
}
.status-yellow {
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background-color: yellow;
  display: inline-block;
}

.status-green {
    width: 15px;
  height: 15px;
  border-radius: 50%;
  background-color: green;
  display: inline-block;
}

.status-red {
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background-color: red;
  display: inline-block;
}
.pagination {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 20px;
}
.pagination button {
    background-color: #007bff;
    color: white;
    border-color: #007bff;
}
.pagination button:hover{
    background-color: #0056b3;
    border-color: #0056b3;
}
.record-item-clickable {
    cursor: pointer;
}
</style>