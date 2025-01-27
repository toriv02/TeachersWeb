<script setup>
import { onBeforeMount, ref } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
});
const records = ref([]);
const documents = ref([]);
onBeforeMount(async () => {
    await fetchRecords();
     await fetchDocuments();
});
async function fetchRecords() {
  try {
    const response = await axios.get('/api/records/', {
      params: {
        is_published: true,
        page: 1,
          ordering: '-time',
        page_size: 5
      }
    });
    records.value = response.data.results;
  } catch (error) {
    console.error('Ошибка загрузки записей:', error);
  }
}
async function fetchDocuments() {
   try {
    const response = await axios.get('/api/documents/', {
      params: {
        page: 1,
        page_size: 5
      }
    });
    documents.value = response.data.results;
  } catch (error) {
    console.error('Ошибка загрузки документов:', error);
  }
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
</script>

<template>
  <div class="home-container">
    <div class="section">
      <h2 class="text-white">Последние материалы</h2>
      <div v-if="!records.length">
           <p class="text-white">Нет опубликованных материалов</p>
       </div>
      <div v-else>
        <div v-for="record in records" :key="record.id" class="record-item">
          <h3 class="record-headline text-white">{{ record.headline }}</h3>
          <p class="record-date text-white">Дата: {{ formatDateTime(record.time) }}</p>
          <p class="record-subject text-white">Предметная область: {{ record.subject.name }}</p>
            <p class="record-comment text-white">{{ record.comment }}</p>
        </div>
        <router-link to="/records" class="view-all-link">Посмотреть все материалы</router-link>
      </div>
    </div>

    <div class="section">
      <h2 class="text-white">Последние документы</h2>
        <div v-if="!documents.length">
           <p class="text-white">Нет документов</p>
        </div>
      <div v-else>
        <div v-for="document in documents" :key="document.id" class="document-item">
          <h3 class="document-headline text-white">{{ document.headline }}</h3>
           <p class="document-description text-white">{{ document.description }}</p>
        </div>
           <router-link to="/documents" class="view-all-link">Посмотреть все документы</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 1000px;
  margin: 20px auto;
   padding: 20px;
   border-radius: 1rem;
    background-color: #343a40;
}
.section{
  background-color: #495057;
  border-radius: 10px;
    padding: 20px;
}
.record-item{
    padding: 10px;
    border-radius: 8px;
    border: 1px solid silver;
     margin-bottom: 5px;
}
.document-item{
    padding: 10px;
    border-radius: 8px;
    border: 1px solid silver;
     margin-bottom: 5px;
}
.view-all-link {
  display: inline-block;
  margin-top: 10px;
  text-decoration: none;
  color: #007bff;
}
.view-all-link:hover {
    color: #0056b3;
}
.record-headline{
  color: white;
}
.record-date{
  color: white;
   font-style: italic;
}
.record-subject{
  color: white;
}
.record-comment{
  color: white;
}
.document-headline{
  color: white;
}
.document-description{
  color: white;
}
</style>