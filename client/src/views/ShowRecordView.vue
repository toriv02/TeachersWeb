<script setup>
import { onBeforeMount, ref, watch, computed } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { useRoute, useRouter } from 'vue-router';
import useUserStore from '../stores/userStore';
import { storeToRefs } from 'pinia';

const route = useRoute();
const router = useRouter();
const recordId = ref(route.params.id);
const record = ref(null);
const reviews = ref([]);
const newReviewText = ref('');
const reviewPagination = ref({
    page: 1,
    pageSize: 5,
    totalCount: 0,
    hasNextPage: false,
    hasPreviousPage: false,
});
const userStore = useUserStore();
const { isSuperUser, userId } = storeToRefs(userStore);
const errorText = ref('');
const loadingReviews = ref(false);
// новые поля
const feedback = ref(null); // текущий комментарий модератора
const newFeedbackText = ref(''); // текст модераторского комментария
const loadingFeedback = ref(false); // статус загрузки
const csrfToken = Cookies.get('csrftoken');

onBeforeMount(() => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
});

onBeforeMount(async () => {
    await fetchRecord();
});
watch(record, async()=>{
    if (isSuperUser.value && record.value) {
        await fetchFeedback();
    }
})

async function fetchRecord() {
    try {
        const response = await axios.get(`/api/records/${recordId.value}/`);
        record.value = response.data;
        if (!isSuperUser.value && !record.value.is_published) {
            router.push('/error');
        }
        await fetchReviews();
      
    } catch (error) {
        console.error('Ошибка загрузки записи:', error);
        router.push('/error');
    }
}

async function fetchReviews() {
    loadingReviews.value = true;
    try {
        const response = await axios.get(`/api/reviews/?records_FK=${recordId.value}&page=${reviewPagination.value.page}&page_size=${reviewPagination.value.pageSize}`);
        reviews.value = response.data.results;
        reviewPagination.value.totalCount = response.data.count;
        reviewPagination.value.hasNextPage = response.data.next !== null;
        reviewPagination.value.hasPreviousPage = response.data.previous !== null;
    } catch (error) {
        console.error("Ошибка загрузки рецензий:", error);
        reviews.value = [];
    } finally {
        loadingReviews.value = false;
    }
}
async function fetchFeedback() {
    loadingFeedback.value = true;
    try {
        const response = await axios.get(`/api/feedbacks/?records_FK=${recordId.value}`);
        console.log('Бекенд вернул:', response.data);
        console.log('Бекенд вернул:', response.data.length);
        if (response.data && response.data.length > 0) {
            const feedbackData = response.data[0];
            feedback.value = feedbackData;
            newFeedbackText.value = feedbackData.content;
            console.log('Комментарий получен:', feedback.value);
        } else {
             feedback.value = null;
             newFeedbackText.value = '';
            console.log('Нет комментария для этой записи');
        }
    } catch (error) {
        console.error('Ошибка загрузки обратной связи:', error);
        feedback.value = null;
        newFeedbackText.value = '';
    } finally {
         loadingFeedback.value = false;
    }
}

async function addReview() {
    errorText.value = '';

    const formData = new FormData();
    formData.append('content', newReviewText.value);
    formData.append('records_FK_id', recordId.value);
    formData.append('author', userId.value);

    try {
        const response = await axios.post('/api/reviews/',formData, {
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': false,
                'processData': false
            }
        });
        newReviewText.value = '';
        reviewPagination.value.page = 1;
        await fetchReviews();
    } catch (error) {
        console.error('Ошибка добавления рецензии:', error);
        errorText.value = 'Ошибка добавления рецензии';
    }
}

async function publishRecord() {
    try {
        const response = await axios.put(`/api/records/${recordId.value}/`, {
            is_published: !record.value.is_published
        });
        record.value = response.data;
        await fetchRecord();
    } catch (error) {
        console.error('Ошибка публикации записи:', error);
        if (error.response) {
            console.error('Ошибка ответа сервера:', error.response.data);
            console.error('Status code', error.response.status)
        }
    }
}
function handleReviewPageChange(page) {
    reviewPagination.value.page = page;
    fetchReviews();
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

watch(recordId, async () => {
    await fetchRecord();
});
function getFileIcon(file) {
    let preview = null;
        if(file && file.url && file.url.endsWith('.xlsx')){
        preview="/icon-file-xlsx.png"
    }
    else if(file && file.url && file.url.endsWith('.pdf')){
        preview="/icon-file-pdf.png"
    }
    else if (file && file.url && (file.url.endsWith('.docx') || file.url.endsWith('.doc'))) {
        preview = "/icon-file-word.png";
    }
    else {
        preview="/icon-file-another.png"
    }
    return preview
}

// Логика для пагинации (встроенная)
const hasNextPage = computed(() => {
            return reviewPagination.value.page * reviewPagination.value.pageSize < reviewPagination.value.totalCount;
        });

        const hasPreviousPage = computed(() => {
            return reviewPagination.value.page > 1;
        });
         const totalPages = computed(()=> {
             return Math.ceil(reviewPagination.value.totalCount/reviewPagination.value.pageSize);
        })
         function handlePageChange(page) {
            if(page > 0 && page <=  totalPages.value){
                handleReviewPageChange(page);
            }
        }
// Метод добавления и обновления обратной связи
async function addOrUpdateFeedback() {
    try {
      const formData = new FormData();
       formData.append('content', newFeedbackText.value);
      formData.append('records_FK_id', recordId.value);
     formData.append('moderator', userId.value)


        if (feedback.value) {
             await axios.put(`/api/feedbacks/${feedback.value.id}/`, formData, {
                   headers: {
                       'X-CSRFToken': csrfToken,
                         'Content-Type': false,
                         'processData': false
                   }
             });
        } else {
          await axios.post('/api/feedbacks/', formData, {
              headers: {
                       'X-CSRFToken': csrfToken,
                         'Content-Type': false,
                        'processData': false
                   }
            });
        }

        await fetchFeedback();
        errorText.value = ''
    } catch (error) {
           console.error('Ошибка добавления/обновления обратной связи:', error);
         if (error.response) {
                errorText.value = `Ошибка добавления/обновления обратной связи: ${error.response.data}`;
                 console.error('Ошибка ответа сервера:', error.response.data);
                console.error('Status code', error.response.status)
              }
        else{
             errorText.value = 'Ошибка добавления/обновления обратной связи';
        }
    }
}

const isChecked = computed(() => {
  if (!record.value || !feedback.value) {
    return false;
  }
  try {
        const recordTime = new Date(record.value.time);
        const feedbackTime = new Date(feedback.value.time);
        return (recordTime < feedbackTime);
  } catch (error) {
      console.error('Ошибка при проверке даты:', error);
      return false
  }
});
const showStatus = computed(() => {
    return !(record.value && record.value.is_published)
});
</script>

<template>
    <div class="show-record-container" v-if="record">
        <div class="record-header">
            <div class="buttons-header">
                <button v-if="isSuperUser" @click="publishRecord" class="btn btn-success">
                    {{ record.is_published ? 'Снять с публикации' : 'Опубликовать' }}
                </button>
                <span v-if="showStatus" :class="{'text-success': isChecked, 'text-danger': !isChecked}" class="ms-2">
                            {{ isChecked ? 'Проверено' : 'Требует проверки' }}
                        </span>
            </div>
        </div>
        <div class="record-content">
            <div class="record-info">
                <h2 class="record-headline text-white">{{ record.headline }}</h2>
                <p class="record-author text-white">Автор: {{ record.author ? record.author.fio : "Не указано" }}</p>
                <p class="record-author text-white" v-if="record.author && record.author.school">Школа: {{ record.author.school.name }}</p>
                <p class="record-author text-white" v-else>Школа: Не указано</p>
                <p class="record-date text-white">Дата публикации: {{ formatDateTime(record.time) }}</p>
                <p class="record-comment text-white">{{ record.comment }}</p>
                <div v-if="record.files && record.files.length > 0" class="record-files">
                    <h4 class="record-files-header text-white">Прикрепленные файлы:</h4>
                    <ul class="file-list">
                        <li v-for="file in record.files" :key="file.id" class="file-item">
                            <div class="file-item-content">
                                <img :src="getFileIcon(file)" alt="Иконка файла" class="file-icon">
                                <a :href="file.url" class="text-white record-file-link" :download="decodeURIComponent(file.url.split('/').pop())">
                                    <span class="file-name">{{ decodeURIComponent(file.url.split('/').pop()) }}</span>
                                </a>
                            </div>
                        </li>
                    </ul>
                </div>

            </div>
        </div>
          <div class="record-feedback" v-if="isSuperUser">
                 <h3 class="text-white">Комментарий модератора</h3>
                    <div v-if="loadingFeedback">
                        <p class="text-white">Загрузка комментария...</p>
                   </div>
                 <div v-else class="feedback-content">
                    <textarea v-model="newFeedbackText" class="form-control mt-2" placeholder="Напишите ваш комментарий"></textarea>
                     <button @click="addOrUpdateFeedback" class="btn btn-primary mt-2">Сохранить</button>
                     <p class="text-danger mt-1">{{ errorText }}</p>
                  </div>
                    <p v-if="feedback" class="text-white feedback-date">Дата: {{ formatDateTime(feedback?.time) }}</p>

           </div>
        <div class="record-reviews">
            <h3 class="text-white">Рецензии</h3>
            <div v-if="loadingReviews">
                <p class="text-white">Загрузка рецензий...</p>
            </div>
            <div v-else-if="reviews.length > 0" class="review-list">
                <div v-for="review in reviews" :key="review.id" class="review-item">
                    <p class="review-author text-white">Автор: {{ review.author.fio ? review.author.fio : 'Не указано' }}</p>
                    <p class="review-content text-white">{{ review.content }}</p>
                </div>
            </div>
            <div v-else>
                <p class="text-white">Нет рецензий</p>
            </div>
            <div v-if="userId">
                <textarea v-model="newReviewText" class="form-control mt-2" placeholder="Напишите вашу рецензию"></textarea>
                <button @click="addReview" class="btn btn-primary mt-2">Добавить рецензию</button>
                <p v-if="errorText" class="text-danger mt-1">{{ errorText }}</p>
            </div>
        <!--  Встроенный шаблон пагинации  -->
            <div class="pagination" v-if="reviewPagination.totalCount > reviewPagination.pageSize">
                <button class="btn btn-secondary" :disabled="!hasPreviousPage" @click="handlePageChange(reviewPagination.page - 1)">
                    <i class="bi bi-arrow-left"></i> Назад
                </button>
                <span class="text-white">{{ reviewPagination.page }} / {{ totalPages }}</span>
                <button  class="btn btn-secondary" :disabled="!hasNextPage" @click="handlePageChange(reviewPagination.page + 1)">
                    Вперед <i class="bi bi-arrow-right"></i>
                </button>
            </div>
        </div>
    </div>
</template>
<style scoped>
.show-record-container {
    max-width: 1000px;
    margin: 20px auto;
    padding: 20px;
    border-radius: 1rem;
    background-color: #343a40;
}

.record-header{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}
.buttons-header{
    display: flex;
    gap: 10px;
}
.buttons-header button{
    color: white;
}
.record-content{
    display: flex;
    gap: 20px;
}

.record-info{
    flex: 2;
}
.record-reviews{
    margin-top: 20px;
    background-color: #495057;
    padding: 15px;
    border-radius: 8px;
}

.record-headline{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    font-weight: bold;
    word-break: break-word;
    word-wrap: break-word;
}
.record-author{
    font-style: italic;
    margin-bottom: 0.5rem;
}
.record-date{
    margin-bottom: 1rem;
}
.record-comment{
    white-space: pre-line;
    word-wrap: break-word;
}
.record-files {
    margin-top: 1rem;
    padding-top: 10px;
    border-top: 1px solid #ddd;
}
.record-files-header{
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}
.record-files-list{
    list-style: none;
    padding: 0;
    margin-top: 10px;
}
.record-file-link{
    display: flex;
    align-items: center;
    justify-content: space-between;
    text-decoration: none;
    color: #007bff;
    transition: color 0.3s;
    border: 1px solid #eee;
    padding: 10px;
    border-radius: 4px;
    margin-bottom: 5px;
    display: inline-flex;
}
.record-file-link:hover {
    color: #0056b3;
}
.file-list {
    list-style: none;
    padding: 0;
    margin-top: 10px;
}

.file-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border: 1px solid #eee;
    padding: 10px;
    border-radius: 4px;
    margin-bottom: 5px;
    margin-right: 5px;
}
.file-name {
    font-weight: bold;
    margin-right: 10px;
    color: white;
    word-break: break-word;
    word-wrap: break-word;
}

.file-preview {
    max-width: 50px;
    max-height: 50px;
    margin-right: 10px;
    border-radius: 4px;
}
.file-item-content {
    display: flex;
    align-items: center;
}
.file-icon {
    max-width: 30px;
    max-height: 30px;
    margin-right: 10px;
}
.review-list {
    margin-top: 10px;
}

.review-item {
    margin-bottom: 10px;
    padding: 10px;
    border-radius: 4px;
    background-color: #495057;
    border: 1px solid #ddd;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
}

.review-author {
    font-weight: bold;
    margin-bottom: 5px;
    color: white;
}
.review-content {
    color: white;
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
.record-feedback{
    margin-top: 20px;
        background-color: #495057;
        padding: 15px;
    border-radius: 8px;
}
.feedback-date {
  font-style: italic;
    margin-bottom: 0.5rem;
}
</style>