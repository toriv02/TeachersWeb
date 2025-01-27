<script setup>
import {computed, onBeforeMount, ref} from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import useUserStore from '../stores/userStore';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';



onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

const subjects=ref([])

const subjectToAdd=ref({})
const subjectToEdit=ref({})


const filters = ref({
  name: ""
});

const router = useRouter();

const userStore = useUserStore();
const { isSuperUser } = storeToRefs(userStore);

onBeforeMount(async ()=>{
  if(!isSuperUser.value) router.push('/error')
  await fetchSubjects()
})
async function fetchSubjects(){
  const r =await axios.get("/api/subjects/");
  console.log(r.data);
  subjects.value=r.data;
}

async function onSubjectAdd() {
  await axios.post("/api/subjects/", {
    ...subjectToAdd.value,
  });
  await fetchSubjects(); // переподтягиваю
}

async function onRemoveClick(subject) {
  await axios.delete(`/api/subjects/${subject.id}/`);
  await fetchSubjects(); // переподтягиваю
}

async function onSubjectEditClick(subject) {
  subjectToEdit.value = { ...subject };
}

async function onUpdateSubject() {
  await axios.put(`/api/subjects/${subjectToEdit.value.id}/`, {
    ...subjectToEdit.value,
  });
  await fetchSubjects();
}

const filteredSubjects = computed(() => {
    if (!filters.value.name) {
      return subjects.value;
    }
    const searchTerm = filters.value.name.toLowerCase();
    return subjects.value.filter(subject => {
    const nameMatch = subject.name && subject.name.toLowerCase().includes(searchTerm);
    

    return nameMatch;
    });
});

function resetFilters() {
    filters.value = {
        name: "",
    };
}


</script>

<template>

<form @submit.prevent.stop="onSubjectAdd">
  <div class="row">
    <div class="col">
      <div class="form-floating">
        <input
          type="text"
          class="form-control"
          v-model="subjectToAdd.name"
          required
        />
        <label for="floatingInput">Название</label>
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
        <input type="text" class="form-control" placeholder="Пример текста" v-model="filters.name">
    </div>
  <div class="col-auto">
        <button class="btn btn-primary" @click="resetFilters">Сбросить</button>
  </div>
</div>
<div class="check-subject-container">
  <div v-if="!filteredSubjects.length">
    <p class="text-white">Нет предметов</p>
  </div>
  <div v-else>
    <div v-for="item in filteredSubjects" class="subject-item">
      <div>{{ item.name }}</div>
      <div class="subject-actions">
        <button
          class="btn btn-success"
          @click="onSubjectEditClick(item)"
          data-bs-toggle="modal"
          data-bs-target="#editSubjectModal"
        >
          <i class="bi bi-pen-fill"></i>
        </button>
        <button class="btn btn-danger" @click="onRemoveClick(item)">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>
  </div>
</div>

<!-- модальное окно для редактирования-->
<div class="modal fade" id="editSubjectModal" tabindex="-1">
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
                  v-model="subjectToEdit.name"
                />
                <label for="floatingInput">Наименование</label>
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
            @click="onUpdateSubject"
          >
            Сохранить
          </button>
        </div>
      </div>
    </div>
</div>



</template>

<style>
.subject-item{
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
  display: flex;
    align-items: center;
  justify-content: space-between;
    color: #fff;
}
.subject-actions{
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
.check-subject-container {
    max-width: 1000px;
    margin: 20px auto;
    padding: 20px;
    border-radius: 1rem;
    background-color: #343a40;
}
</style>

