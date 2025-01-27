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

const schools=ref([])

const schoolToAdd=ref({})
const schoolToEdit=ref({})


const filters = ref({
  name: '',
});

const currentPage = ref(1);
const totalPages = ref(1);

const router = useRouter();


const userStore = useUserStore();
const { isSuperUser } = storeToRefs(userStore);

onBeforeMount(async ()=>{
  if(!isSuperUser.value) router.push("/error")
  await fetchSchools()
})
async function fetchSchools(){
  try {
    const r =await axios.get("/api/schools/", {
              params: {
                  page: currentPage.value,
                  search: filters.value.name,
              },
        });
      schools.value = r.data.results;
      totalPages.value = Math.ceil(r.data.count / 5);
  } catch (error) {
        console.error('Ошибка загрузки документов:', error);
  }
}

async function onSchoolAdd() {
  await axios.post("/api/schools/", {
    ...schoolToAdd.value,
  });
  await fetchSchools(); // переподтягиваю
}

async function onRemoveClick(school) {
  await axios.delete(`/api/schools/${school.id}/`);
  await fetchSchools(); // переподтягиваю
}

async function onSchoolEditClick(school) {
  schoolToEdit.value = { ...school };
}

async function onUpdateSchool() {
  await axios.put(`/api/schools/${schoolToEdit.value.id}/`, {
    ...schoolToEdit.value,
  });
  await fetchSchools();
}

function resetFilters() {
    filters.value = {
        name: '',
    };
}


</script>

<template>

<form @submit.prevent.stop="onSchoolAdd">
  <div class="row">
    <div class="col">
      <div class="form-floating">
        <input
          type="text"
          class="form-control"
          v-model="schoolToAdd.name"
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
        <input type="text" class="form-control" placeholder="Пример текста" v-model="filters.name" @input="fetchSchools">
    </div>
  <div class="col-auto">
        <button class="btn btn-primary" @click="resetFilters">Сбросить</button>
  </div>
</div>


<div class="check-school-container">
  <div v-if="!schools.length">
    <p class="text-white">Нет школ</p>
  </div>
  <div v-else>
    <div v-for="item in schools" class="school-item">
      <div>{{ item.name }}</div>
      <div class="school-actions">
        <button
          class="btn btn-success"
          @click="onSchoolEditClick(item)"
          data-bs-toggle="modal"
          data-bs-target="#editSchoolModal"
        >
          <i class="bi bi-pen-fill"></i>
        </button>
        <button class="btn btn-danger" @click="onRemoveClick(item)">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>
    <div class="pagination">
      <button
              class="btn btn-secondary"
              :disabled="currentPage === 1"
              @click="currentPage--; fetchSchools()"
          >
              <i class="bi bi-arrow-left"></i> Назад
          </button>
          <span class="text-white">{{ currentPage }} / {{ totalPages }}</span>
          <button
              class="btn btn-secondary"
              :disabled="currentPage === totalPages"
              @click="currentPage++; fetchSchools()"
          >
              Вперед <i class="bi bi-arrow-right"></i>
          </button>
     </div>
  </div>
</div>



<!-- модальное окно для редактирования-->
<div class="modal fade" id="editSchoolModal" tabindex="-1">
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
                  v-model="schoolToEdit.name"
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
            @click="onUpdateSchool"
          >
            Сохранить
          </button>
        </div>
      </div>
    </div>
</div>



</template>

<style>
.school-item{
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
  display: flex;
    align-items: center;
  justify-content: space-between;
    color: #fff;
}

.school-actions{
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

.check-school-container {
    max-width: 1000px;
    margin: 20px auto;
    padding: 20px;
    border-radius: 1rem;
    background-color: #343a40;
}
.school-card {
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

