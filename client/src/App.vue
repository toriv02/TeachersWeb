<script setup>
import { onBeforeMount } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { storeToRefs } from 'pinia';
import useUserStore from './stores/userStore';
import {useRouter, useRoute} from "vue-router";
import 'bootstrap/dist/js/bootstrap.bundle.min'



const userStore=useUserStore();
const {
    isAuthenticated,
    isSuperUser,
}=storeToRefs(userStore)
const router = useRouter();
const route = useRoute();

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

async function logout() {
  const csrfToken = Cookies.get('csrftoken');
  try {
    const response = await axios.post('/api/user/logout/', {}, {
      headers: {
        'X-CSRFToken': csrfToken
      }
    });
    if (response.data.success) {
      userStore.resetUser();
      
    }
    window.location.reload();
  } catch (error) {
    console.error('Ошибка выхода:', error);
  }
}

const isActive = (routePath) => {
  return route.path === routePath;
};
</script>
<template>
  
  <div class="container">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="/"> Обмен</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav mb-2 mb-lg-0">
            <li class="nav-item" :class="{ 'active': isActive('/documents') }">
              <router-link class="nav-link" to="/documents">Документы</router-link>
            </li>
            <li class="nav-item" :class="{ 'active': isActive('/records') }">
              <router-link class="nav-link" to="/records">Материалы</router-link>
            </li>
          </ul>

          <ul v-if="isSuperUser" class="navbar-nav">
            <li class="nav-item" :class="{ 'active': isActive('/subjects') }">
              <router-link class="nav-link" to="/subjects">Предметы</router-link>
            </li>
            <li class="nav-item" :class="{ 'active': isActive('/schools') }">
              <router-link class="nav-link" to="/schools">Школы</router-link>
            </li>
          </ul>

          <ul class="navbar-nav ms-auto">
            <li v-if="!isAuthenticated" class="nav-item">
              <router-link class="nav-link" to="/login">Войти</router-link>
            </li>
            <li v-if="!isAuthenticated" class="nav-item">
              <router-link class="nav-link" to="/register">Зарегестрироваьтся</router-link>
            </li>
            <li v-if="isAuthenticated" class="nav-item">
              <router-link class="nav-link" to="/my">Мои публикации</router-link>
            </li>
            <li v-if="isAuthenticated" class="nav-item">
               <a class="nav-link" href="#" @click.prevent="logout">выйти</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>

  


  
  <div class="container">
    <router-view/>
  </div>

</template>



