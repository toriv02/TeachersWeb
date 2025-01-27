<script setup>
import { computed, onBeforeMount, ref } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { storeToRefs } from 'pinia';
import useUserStore from '../stores/userStore';

const userStore = useUserStore();
const { isSuperUser } = storeToRefs(userStore);

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
});

const documents = ref([]);
const currentPage = ref(1);
const totalPages = ref(1);
const documentToAdd = ref({});
const documentToEdit = ref({});
const filters = ref({
  content: '',
});
const hoveredDocument = ref(null);

onBeforeMount(async () => {
  await fetchDocuments();
});

async function fetchDocuments() {
    try {
        const response = await axios.get('/api/documents/', {
            params: {
                page: currentPage.value,
                ordering: '-time', 
                search: filters.value.content,
            },
        });
        documents.value = response.data.results;
        totalPages.value = Math.ceil(response.data.count / 5);
    } catch (error) {
        console.error('Ошибка загрузки документов:', error);
    }
}
async function onDocumentAdd() {
  await axios.post('/api/documents/', {
    ...documentToAdd.value,
  });
  await fetchDocuments();
}

async function onRemoveClick(document) {
  await axios.delete(`/api/documents/${document.id}/`);
  await fetchDocuments();
}

async function onDocumentEditClick(document) {
  documentToEdit.value = { ...document };
}

async function onUpdateDocument() {
  await axios.put(`/api/documents/${documentToEdit.value.id}/`, {
    ...documentToEdit.value,
  });
  await fetchDocuments();
}

function resetFilters() {
  filters.value = {
    content: '',
  };
  fetchDocuments();
}

function onPush(document) {
  window.open(document.ref);
}
</script>

<template>

<form @submit.prevent.stop="onDocumentAdd" v-if="isSuperUser">
  <div class="row">
    <div class="col">
      <div class="form-floating">
        <input
          type="text"
          class="form-control"
          v-model="documentToAdd.headline"
          required
        />
        <label for="floatingInput">Название</label>
      </div>

      <div class="form-floating">
          <textarea
            class="form-control"
            v-model="documentToAdd.description"
            rows="5"
            required
            style="overflow-y: auto; resize: none; min-height: 120px;"
          ></textarea>
          <label for="floatingInput">Описание</label>
        </div>

      <div class="form-floating">
        <input
          type="text"
          class="form-control"
          v-model="documentToAdd.ref"
          required
        />
        <label for="floatingInput">Ссылка</label>
      </div>
    </div>

    <div class="col-auto">
      <button class="btn btn-primary">
        Добавить
      </button>
    </div>
  </div>
</form>

<h4>Фильтрация</h4>
<div class="row mb-3 mt-3">
    <div class="col">
        <input type="text" class="form-control" placeholder="Пример текста" v-model="filters.content" @input="fetchDocuments">
    </div>
  <div class="col-auto">
        <button class="btn btn-primary" @click="resetFilters">Сбросить</button>
  </div>
</div>

<div class="check-document-container">
<div v-if="!documents.length">
  <p class="text-white">Нет документов</p>
</div>
<div v-else>
 <div v-for="item in documents" class="document-item">
    <div class="document-header">
      <div class="document-title">
          <h5>{{ item.headline }}:</h5>
      </div>
      <div class="document-actions">
          <button 
              v-if="isSuperUser"
              class="btn btn-success"
              @click="onDocumentEditClick(item)"
              data-bs-toggle="modal"
              data-bs-target="#editDocumentModal"
          >
              <i class="bi bi-pen-fill"></i>
          </button>
          <button 
              v-if="isSuperUser"
              class="btn btn-danger"
              @click="onRemoveClick(item)"
          >
              <i class="bi bi-x"></i>
          </button>
          <button 
              class="btn btn-info"
              @click="onPush(item)"
          >
          <i class="bi bi-arrow-bar-right"></i>
          </button>
      </div>
    </div>
    <div class="document-description">
      <span>{{ item.description}}</span>
    </div>
  </div>
  <div class="pagination">
      <button
              class="btn btn-secondary"
              :disabled="currentPage === 1"
              @click="currentPage--; fetchDocuments()"
          >
              <i class="bi bi-arrow-left"></i> Назад
          </button>
          <span class="text-white">{{ currentPage }} / {{ totalPages }}</span>
          <button
              class="btn btn-secondary"
              :disabled="currentPage === totalPages"
              @click="currentPage++; fetchDocuments()"
          >
              Вперед <i class="bi bi-arrow-right"></i>
          </button>
     </div>
  </div>
</div>


<!-- модальное окно для редактирования-->
<div class="modal fade" id="editDocumentModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered modal-lg"> 
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">
            Редактировать документ
          </h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
            <div class="form-floating mb-3">
                 <input
                    type="text"
                    class="form-control"
                    v-model="documentToEdit.headline"
                    id="floatingInputHeadline"
                    />
                 <label for="floatingInputHeadline">Заголовок</label>
            </div>

            <div class="form-floating mb-3">
                <textarea
                    class="form-control"
                    v-model="documentToEdit.description"
                    id="floatingInputDescription"
                    rows="5"
                ></textarea>
                <label for="floatingInputDescription">Описание</label>
           </div>


           <div class="form-floating mb-3">
                <input
                 type="text"
                 class="form-control"
                v-model="documentToEdit.ref"
                  id="floatingInputRef"
                 />
                <label for="floatingInputRef">Ссылка</label>
              </div>
           </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Закрыть
          </button>
          <button
            data-bs-dismiss="modal"
            type="button"
            class="btn btn-primary"
            @click="onUpdateDocument"
          >
            Сохранить
          </button>
        </div>
      </div>
    </div>
</div>


</template>

<style>
.document-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
}
.document-header{
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #fff;
}
.document-description{
  margin: 0.5rem;
  white-space: pre-line;
  word-wrap: break-word;
  color: #fff;
}
.document-actions{
  flex: none;
  display: flex;
  gap: 0.5rem;
}


.row{
  margin-top:10px;
}
.row > div {
  margin-bottom: 1rem;
}

.row > div:last-child {
  margin-bottom: 0;
}

.row > div > .form-floating {
    margin-bottom: 1rem;
}

.row > div > .form-floating:last-child {
    margin-bottom: 0;
}


.form-floating label {
  margin-bottom: 0.5rem;
}

.check-document-container {
    max-width: 1000px;
    margin: 20px auto;
    padding: 20px;
    border-radius: 1rem;
    background-color: #343a40;
}
.document-card {
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
.document-headline {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    font-weight: bold;
    color: white;
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