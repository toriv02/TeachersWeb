<script setup>
import { storeToRefs } from 'pinia';
import useUserStore from '@/stores/userStore';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import Cookies from 'js-cookie';

const username = ref("");
const pas = ref("");
const router = useRouter();

const userStore = useUserStore();
const { isAuthenticated,userId } = storeToRefs(userStore);

const errorText = ref("")

async function login() {
    const csrfToken = Cookies.get('csrftoken');
    errorText.value = ""
    try {
        const response = await axios.post("/api/user/login/", {
            user: username.value,
            password: pas.value
        }, {
            headers: {
                'X-CSRFToken': csrfToken
            }
        });
        if (response.status===200) {
            await userStore.fetchUser();
            if(isAuthenticated.value) router.push("/")
            
        } else {
           errorText.value = response.data.message
        }
    } catch (error) {
        console.error("Ошибка входа:", error);
        errorText.value = "Произошла ошибка при входе"
    }
}
</script>

<template>
    <section class="vh-75 gradient-custom">
     <div class="container py-5 h-100">
         <div class="row d-flex justify-content-center align-items-center h-100">
             <div class="col-10 col-md-6 col-lg-5 col-xl-4">
                 <div class="card custom-bg text-white" style="border-radius: 1rem;">
                     <div class="card-body p-4 text-center">
                         <div class="mb-md-4 mt-md-2 pb-3">
                             <h2 class="fw-bold mb-2 text-uppercase">Вход</h2>
                                 <p v-if="errorText" style="color:red">{{ errorText }}</p>
                             <div class="form-outline form-white mb-3">
                                 <input v-model="username" id="Login" class="form-control form-control-sm" />
                                 <label class="form-label" for="Login">Логин</label>
                             </div>
                             <div class="form-outline form-white mb-3">
                                 <input type="password" v-model="pas" id="typePasswordX"
                                     class="form-control form-control-sm" />
                                 <label class="form-label" for="typePasswordX">Паоль</label>
                             </div>
                             <button @click="login" class="btn btn-outline-light btn-sm px-4"
                                 type="submit">Войти</button>
                         </div>
                         <div>
                             <p class="mb-0">Нет аккаунта? <router-link to="/register" class="text-white-50 fw-bold">Зарегестрируйтесь</router-link>
                             </p>
                         </div>
                     </div>
                 </div>
             </div>
         </div>
     </div>
 </section>
</template>

<style>
.vh-75 {
   height: 75vh;
 }

 .custom-bg {
   background-color: #343a40;
   border-radius: 1rem;
   height: 390px;
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