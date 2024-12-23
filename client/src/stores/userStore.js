import { onBeforeMount, ref } from "vue";
import axios from "axios";
import { defineStore } from "pinia";

const useUserStore = defineStore("UserStore", () => {
  const isAuthenticated = ref(false);
  const username = ref("");
  const userId = ref(null);
  const fio = ref("");
  const schoolID = ref(null);
  const error = ref(null); 
  const isSuperUser=ref(false);
  async function fetchUser() {
    try {
      const response = await axios.get("/api/user/info/");
      isAuthenticated.value = response.data.is_authenticated;
      username.value = response.data.username;
      userId.value = response.data.user_id;
      fio.value = response.data.fio;
      schoolID.value = response.data.schoolID;
      isSuperUser.value=response.data.is_superuser;
      error.value = null;
    } catch (err) {
      console.error("Ошибка при получении данных пользователя:", err);
      error.value = err.message; 
      isAuthenticated.value = false;
      username.value = "";
      userId.value = null;
      fio.value = "";
      schoolID.value = null;
      isSuperUser.value=false;
    }
  }

  function resetUser() {
    isAuthenticated.value = false;
    username.value = "";
    userId.value = null;
    fio.value = "";
    schoolID.value = null;
    error.value = null;
    isSuperUser.value=false;
  }


  onBeforeMount(() => {
    fetchUser();
  });

  return {
    isAuthenticated,
    username,
    userId,
    schoolID,
    fio,
    isSuperUser,
    fetchUser,
    resetUser,
    error 
  };
});

export default useUserStore;