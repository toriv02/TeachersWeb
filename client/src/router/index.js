import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import DocumentView from '@/views/DocumentView.vue'
import MainView from '@/views/MainView.vue'
import RecordView from '@/views/RecordView.vue'
import RegisterView from '@/views/RegisterView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/login",
      name: "LoginView",
      component: LoginView
    },
    {
      path: "/",
      name: "MainView",
      component: MainView
    },
    {
      path: "/records",
      name: "RecordView",
      component: RecordView
    },
    {
      path: "/documents",
      name: "DocumentView",
      component: DocumentView
    },
    {
      path: "/register",
      name: "RegisterView",
      component: RegisterView
    },
  ],
})

export default router