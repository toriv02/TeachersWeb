<script setup>
import { computed,onBeforeMount, ref } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import router from '@/router';
import useUserStore from '../stores/userStore';
import { storeToRefs } from 'pinia';

const userStore=useUserStore();
const {
    isSuperUser,
}=storeToRefs(userStore)

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

const records = ref([]);
const subjects = ref([]);
const currentPage = ref(1);
const totalPages = ref(1);
const hoveredRecord = ref(null);
const filters = ref({
    content: "",
    subject: "",
});

onBeforeMount(async () => {
    await fetchRecords()
    await fetchSubjects()
});

async function fetchRecords() {
  try {
    const response = await axios.get('/api/records/', {
      params: {
        is_published: true,
        page: currentPage.value,
        ordering: '-time',
        search: filters.value.content,
         subject: filters.value.subject
      }
    });
    records.value = response.data.results;
      totalPages.value = Math.ceil(response.data.count/5);
  } catch (error) {
    console.error('Ошибка загрузки записей:', error);
  }
}
async function fetchSubjects() {
  const r =await axios.get("/api/subjects/");
  console.log(r.data);
  subjects.value=r.data;
}
function formatDateTime(dateTimeString) {
  const date = new Date(dateTimeString);
  const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  };
  return new Intl.DateTimeFormat('ru-RU', options).format(date);
}

function onAdd(){
  router.push('/records/add')
}
 function onReviews(){
  router.push('/records/check')
}
</script>
<template>
    <div class="controls-container">
      <div class="review-button-container" v-if="isSuperUser">
        <button
        class="btn btn-primary btn-lg"
        @click="onReviews"
        >
          <i class="bi bi-list-task"></i> Заявки
        </button>
      </div>
    <div class="add-button-container">
      <button
       class="btn btn-primary btn-lg"
       @click="onAdd"
      >
        <i class="bi bi-plus"></i> Добавить
      </button>
    </div>
    <div class="filter-container">
      <h4>Фильтрация</h4>
      <div class="row mb-3 mt-3">
        <div class="col">
          <input
            type="text"
            class="form-control"
            placeholder="Пример текста"
            v-model="filters.content"
             @input="fetchRecords"
          />
        </div>
        <div class="col">
          <select class="form-select" v-model="filters.subject" @change="fetchRecords">
            <option value="">Предметные области</option>
            <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
              {{ subject.name }}
            </option>
          </select>
        </div>
        <div class="col-auto">
          <button class="btn btn-primary" @click="filters.content='';filters.subject='';fetchRecords()">Сбросить</button>
        </div>
      </div>
    </div>
  </div>
  <div class="check-record-container">
     <div v-if="!records.length">
       <p class="text-white">Нет записей для отображения</p>
     </div>
     <div v-else>
       <router-link
         v-for="record in records"
         :key="record.id"
         :to="{ name: 'ShowRecordView', params: { id: record.id } }"
         class="record-card"
         :class="{ 'hovered': hoveredRecord === record.id }"
         @mouseenter="hoveredRecord = record.id"
         @mouseleave="hoveredRecord = null"
       >
         <h3 class="record-headline text-white">{{ record.headline }}</h3>
         <p class="record-date text-white">Дата: {{ formatDateTime(record.time) }}</p>
         <p class="record-subject text-white">Предметная область: {{ record.subject.name }}</p>
         <p class="record-comment text-white">{{ record.comment }}</p>
       </router-link>
         <div class="pagination">
                <button
                        class="btn btn-secondary"
                        :disabled="currentPage === 1"
                        @click="currentPage--; fetchRecords()"
                >
                    <i class="bi bi-arrow-left"></i> Назад
                </button>
                <span class="text-white">{{ currentPage }} / {{ totalPages }}</span>
                <button
                        class="btn btn-secondary"
                        :disabled="currentPage === totalPages"
                        @click="currentPage++; fetchRecords()"
                >
                    Вперед <i class="bi bi-arrow-right"></i>
                </button>
            </div>
     </div>
  </div>
</template>
<style>
.controls-container {
  display: flex;
    flex-direction: column;
   align-items: flex-end; 
  margin-bottom: 1rem;
}
.filter-container {
   width: 100%;
}
.add-button-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
}
.review-button-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
}
@media (max-width: 768px) {
    .controls-container {
    flex-direction: column;
  align-items: flex-start;
  }
    .filter-container {
         width: 100%;
    }
      .row {
      flex-direction: column;
  }
     .add-button-container{
          justify-content: flex-start;
    }
}
.check-record-container {
    max-width: 1000px;
    margin: 20px auto;
    padding: 20px;
    border-radius: 1rem;
    background-color: #343a40;
}
.record-card {
    border: 1px solid #eee;
    margin-bottom: 20px;
    padding: 15px;
    border-radius: 5px;
    cursor: pointer;
    text-decoration: none;
    color: #333;
    display: block;
    transition: background-color 0.3s ease;
    background-color: #495057;
}

.record-card:hover,
.record-card.hovered {
    background-color: #495057;
    opacity: 0.8;
}
.record-headline {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    font-weight: bold;
    color: white;
}
.record-date {
    font-style: italic;
    margin-bottom: 0.5rem;
    color: #fff;
}
.record-subject {
    margin-bottom: 0.5rem;
    color: #fff;
}
.record-comment {
    margin-bottom: 1rem;
    color: #fff;
}
.button-container {
    display: flex;
    gap: 1rem;
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
</style>