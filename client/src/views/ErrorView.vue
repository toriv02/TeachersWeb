<template>
    <div class="error-container">
      <img
        src="https://i.pinimg.com/originals/5c/e3/4a/5ce34a5320f664485bd4841488f8aae3.gif"
        alt="Ошибка"
        class="error-gif"
      />
      <h2 class="error-message">Упс! Что-то пошло не так.</h2>
      <p class="error-text">
        Похоже, что страница, которую вы ищете, не существует или произошла ошибка.
      </p>
        <button @click="redirect" class="error-button">
           Перейти на главную
        </button>
    </div>
  </template>
  
  <script setup>
      import { useRouter } from 'vue-router';
      const router = useRouter()
      const redirect = ()=>{
        router.push('/')
      }
  
  </script>
  
  <style scoped>
  .error-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    text-align: center;
  }
  .error-gif {
      max-width: 300px;
      margin-bottom: 20px;
    }
     .error-message {
        font-size: 2rem;
      margin-bottom: 10px;
  }
  .error-text {
    font-size: 1.2rem;
    color: #555;
    margin-bottom: 20px;
  }
  .error-button {
  padding: 10px 20px;
   background-color: red;
   color: white;
   border: none;
  border-radius: 5px;
  cursor: pointer;
    font-size: 1rem;
  transition: background-color 0.3s ease;
  }
    .error-button:hover {
      background-color: rgb(226, 48, 48);
     }
  </style>