import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/LoginView.vue';
import MainView from '../views/MainView.vue';
import RecordView from '../views/RecordView.vue';
import AddRecordView from '../views/AddRecordView.vue';
import DocumentView from '../views/DocumentView.vue';
import RegisterView from '../views/RegisterView.vue';
import ErrorView from '../views/ErrorView.vue';
import SubjectView from '../views/SubjectView.vue';
import SchoolView from '../views/SchoolView.vue';
import ShowRecordView from '../views/ShowRecordView.vue';
import CheckRecordView from '../views/CheckRecordView.vue';
import UserRecords from '../views/UserRecords.vue';
import ChangeRecordView from '../views/ChangeRecordView.vue';


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
      path: "/records/add",
      name: "AddRecordView",
      component: AddRecordView
    },
       {
          path: '/records/:id',
          name: 'ShowRecordView',
          component: ShowRecordView,
          props: true, 
       },
        {
          path: '/records/check',
          name: 'CheckRecordView',
          component: CheckRecordView
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
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: ErrorView
    },
    {
      path: "/subjects",
      name: "SubjectView",
      component: SubjectView
    },
    {
      path: "/schools",
      name: "SchoolView",
      component: SchoolView
    },
    {
      path: "/my",
      name: "UserRecords",
      component: UserRecords
    },
    {
      path: "/edit-record/:id",
      name: "ChangeRecordView",
      component: ChangeRecordView,
      props: true,
    },
  ],
});

export default router;