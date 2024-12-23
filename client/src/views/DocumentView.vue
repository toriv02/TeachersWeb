<script setup>
import {computed, onBeforeMount, ref} from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { storeToRefs } from 'pinia';
import useUserStore from '../stores/userStore';

const userStore = useUserStore();
const { isSuperUser} = storeToRefs(userStore);

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

const documents=ref([])

const documentToAdd=ref({})
const documentToEdit=ref({})


const filters = ref({
    headline: "",
    description: ""
});


onBeforeMount(async ()=>{
  await fetchDocuments()
})
async function fetchDocuments(){
  const r =await axios.get("/api/documents/");
  console.log(r.data);
  documents.value=r.data;
}

async function onDocumentAdd() {
  await axios.post("/api/documents/", {
    ...documentToAdd.value,
  });
  await fetchDocuments(); // переподтягиваю
}

async function onRemoveClick(document) {
  await axios.delete(`/api/documents/${document.id}/`);
  await fetchDocuments(); // переподтягиваю
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

const filteredDocuments = computed(() => {
    return documents.value.filter(document => {
    const headlineMatch = !filters.value.headline || (document.headline && document.headline.toLowerCase().includes(filters.value.headline.toLowerCase()));
    const descriptionMatch = !filters.value.description || (document.description && document.description.toLowerCase().includes(filters.value.description.toLowerCase()));

    return headlineMatch && descriptionMatch;
    });
});

function resetFilters() {
    filters.value = {
        headline: "",
        description: ""
    };
}

function onPush(document){
    window.location.href =document.ref
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
            rows="3"
            required
             style="overflow-y: auto; resize: none;"
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
        <input type="text" class="form-control" placeholder="Загаловок" v-model="filters.headline">
    </div>
    <div class="col">
        <input type="text" class="form-control" placeholder="Описание" v-model="filters.description">
    </div>
  <div class="col-auto">
        <button class="btn btn-primary" @click="resetFilters">Сбросить</button>
  </div>
</div>

<div v-for="item in filteredDocuments" class="document-item">
    <div class="document-info">
        <span><h5>{{ item.headline }}:</h5></span>
        <span>{{ item.description}}</span>
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

<!-- модальное окно для редактирования жанра-->
<div class="modal fade" id="editDocumentModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">
            редактировать
          </h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="row">

            <div class="col">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  v-model="documentToEdit.headline"
                />
                <label for="floatingInput">Загаловок</label>
              </div>
            </div>

            <div class="col">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  v-model="documentToEdit.description"
                />
                <label for="floatingInput">Описание</label>
              </div>
            </div>

            <div class="col">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  v-model="documentToEdit.ref"
                />
                <label for="floatingInput">Ссылка</label>
              </div>
            </div>


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
  align-items: center;
  gap: 1rem;
}
.document-info{
  display: flex;
  flex-wrap: wrap;
  gap:0.5rem;
  flex: 1;
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
</style>

