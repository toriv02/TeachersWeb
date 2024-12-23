<script setup>
import { ref,onBeforeMount } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import Cookies from 'js-cookie';


const username = ref("");
const pas = ref("");
const pas2 = ref("")
const fio = ref("");
const email = ref("");
const selectedSchool = ref(null);
const schools = ref([])
const router = useRouter();
const csrfToken = Cookies.get('csrftoken');
const errorText = ref("");

async function fetchSchools() {
      try {
           const response = await axios.get("/api/schools/");
          schools.value = response.data;
      } catch (error) {
          console.error("Ошибка при получении школ:", error);
      }
   }


async function register() {
     errorText.value = "";
    if (pas.value !== pas2.value) {
       errorText.value = "Пароли не совпадают!";
        return;
    }
    if (!selectedSchool.value) {
        errorText.value = "Выберите школу!";

        return;
    }
    try {
        const response = await axios.post("/api/user/register/", {
            username: username.value,
            password: pas.value,
            fio: fio.value,
            email: email.value,
            school: selectedSchool.value,
        }, {
            headers: {
                'X-CSRFToken': csrfToken
            }
        });
        if (response.status === 201) {
            router.push('/login');
        } else {
            errorText.value = response.data.message;

        }
    } catch (error) {
       console.error("Ошибка регистрации:", error);
        errorText.value = "Произошла ошибка при регистрации!";
    }
}

onBeforeMount(async () => {
    await fetchSchools();
});
</script>

<template>
    <section class="vh-75 gradient-custom">
        <div class="container py-5 h-100">
            <div class="row d-flex justify-content-center align-items-center h-100">
                <div class="col-10 col-md-6 col-lg-5 col-xl-4">
                    <div class="card custom-bg text-white" style="border-radius: 1rem;">
                        <div class="card-body p-4 text-center">
                            <div class="mb-md-4 mt-md-2 pb-3">
                                <h2 class="fw-bold mb-2 text-uppercase">регистрация</h2>
                                <p v-if="errorText" style="color:red">{{ errorText }}</p>
                                <div class="form-outline form-white mb-3">
                                    <input v-model="fio" id="FIO" class="form-control form-control-sm" />
                                    <label class="form-label" for="FIO">ФИО</label>
                                </div>
                                <div class="form-outline form-white mb-3">
                                    <input v-model="email" type="email" id="Email" class="form-control form-control-sm" />
                                    <label class="form-label" for="Email">Email</label>
                                </div>
                                
                                <div class="form-outline form-white mb-3">
                                    <select class="form-select" v-model="selectedSchool" required>
                                        <option :value="s.id" v-for="s in schools" :key="s.id">
                                            {{ s.name }}
                                        </option>
                                    </select>
                                    <label for="floatingInput">Учебное заведение</label>
                                </div>

                                <div class="form-outline form-white mb-3">
                                    <input v-model="username" id="Login" class="form-control form-control-sm" />
                                    <label class="form-label" for="Login">Логин</label>
                                </div>
                                <div class="form-outline form-white mb-3">
                                    <input type="password" v-model="pas" id="typePasswordX"
                                        class="form-control form-control-sm" />
                                    <label class="form-label" for="typePasswordX">Пароль</label>
                                </div>
                                <div class="form-outline form-white mb-3">
                                    <input type="password" v-model="pas2" id="typePasswordX2"
                                        class="form-control form-control-sm" />
                                    <label class="form-label" for="typePasswordX2">Поавторите пароль</label>
                                </div>
                                <button @click="register" class="btn btn-outline-light btn-sm px-4"
                                    type="submit">Register</button>
                            </div>
                            <div>
                                <p class="mb-0">Уже есть аккаунт? <router-link to="/login"
                                        class="text-white-50 fw-bold">войдите</router-link>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>
<style scoped>
.vh-75 {
   height: 75vh;
 }

 .custom-bg {
   background-color: #343a40;
   border-radius: 1rem;
   height: 720px;
 }

 .card-body {
   padding: 1.5rem;
 }

 .btn-outline-light {
   color: #ffff;
   border-color: #ffff;
 }

 .btn-outline-light:hover {
   background-color: lightslategrey;
   color: #ffff;
 }
</style>