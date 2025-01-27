<script setup>
import { onBeforeMount, ref, computed } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { useRoute, useRouter } from 'vue-router';
import useUserStore from '../stores/userStore';
import { storeToRefs } from 'pinia';
import { v4 as uuidv4 } from 'uuid';


onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

const headline = ref('');
const comment = ref('');
const subject_id = ref(null);
const fileInput = ref(null);
const subjects = ref([]);
const record = ref(null);
const feedback = ref(null);
const selectedFiles = ref([])
const oldFiles = ref([])


const router = useRouter();
const route = useRoute();
const errorText = ref("");
const csrfToken = Cookies.get('csrftoken');
const recordId = ref(route.params.id);
const userStore = useUserStore();
const { userId } = storeToRefs(userStore);

onBeforeMount(async () => {
     await fetchSubjects();
      if (recordId.value) {
        await fetchRecord();
        await fetchFeedback();
        }
});

async function fetchRecord() {
      try {
           const response = await axios.get(`/api/records/${recordId.value}/`);
            record.value = response.data;
            headline.value = record.value.headline;
            comment.value = record.value.comment;
            subject_id.value = record.value.subject.id;
             if (record.value.files && record.value.files.length > 0) {
                 oldFiles.value = await Promise.all(record.value.files.map(async(file) => {
                     const response = await axios.get(`/api/files/?file=${file}`)
                     let preview= null
                      if(file.endsWith('.xlsx')){
                         preview="/icon-file-xlsx.png"
                      }
                      else if(file.endsWith('.pdf')){
                        preview="/icon-file-pdf.png"
                      }
                     else if (file.endsWith('.docx') || file.endsWith('.doc')) {
                         preview = "/icon-file-word.png";
                     }
                     else {
                        preview="/icon-file-another.png"
                     }
                     return  {
                         preview: preview,
                         id: response.data.id,
                         isOld: true,
                         file: { name: file.split('/').pop(), url:file }
                      }
                }));
                selectedFiles.value = [...oldFiles.value]
             }
        } catch (error) {
        console.error("Ошибка при получении записи:", error);
           errorText.value = "Ошибка при получении записи";
        }
}
async function fetchFeedback() {
      try {
           const response = await axios.get(`/api/feedbacks/?records_FK=${recordId.value}`);
            if(response.data && response.data.length > 0){
                 feedback.value = response.data[0];
            }
         } catch (error) {
           console.error("Ошибка при получении обратной связи:", error);
        }
}

async function fetchSubjects() {
    try {
        const response = await axios.get("/api/subjects/");
        subjects.value = response.data;
    } catch (error) {
        console.error("Ошибка при получении предметов:", error);
    }
}
const selectedSubject = computed(() => {
   return subjects.value.find(subject => subject.id === subject_id.value);
});

function handleFileChange() {
    const newFiles = Array.from(fileInput.value.files).map(file => {
          let preview = null;
           if(file instanceof File && file.type.startsWith('image/')){
              preview= URL.createObjectURL(file)
           }
          else if(file instanceof File && file.name.endsWith('.xlsx')){
              preview="/icon-file-xlsx.png"
         }
          else if(file instanceof File && file.name.endsWith('.pdf')){
              preview="/icon-file-pdf.png"
          }
         else if (file instanceof File && (file.name.endsWith('.docx') || file.name.endsWith('.doc'))) {
              preview = "/icon-file-word.png";
         }
          else {
              preview="/icon-file-another.png"
          }
        return {file,preview, id:uuidv4(), isOld:false}
        });
      selectedFiles.value.push(...newFiles);
      fileInput.value.value = null
}
async function removeFile(index, item) {
    selectedFiles.value.splice(index, 1);
   if (item.id && item.isOld) {
     try {
        await axios.delete(`/api/files/${item.id}/`, {
              headers: {
                'X-CSRFToken': csrfToken,
             }
        });
        console.log(`Файл с ID ${item.id} удален с сервера`);
     } catch (error) {
        console.error(`Ошибка удаления файла с ID ${item.id}:`, error);
         errorText.value = "Ошибка при удалении файла";
      }
    }
}
async function addRecord() {
    errorText.value = "";

    const formData = new FormData();
    formData.append('headline', headline.value);
    formData.append('comment', comment.value);
    formData.append('subject', selectedSubject.value ? selectedSubject.value.id : null);
    formData.append('is_published', record.value.is_published);
    formData.append('author', userId.value);

    let allFiles = [];
    selectedFiles.value.forEach(item => {
        if (item.file instanceof File) {
            allFiles.push(item.file);
        }
     });
     for (let i = 0; i < allFiles.length; i++) {
           formData.append('files', allFiles[i]);
        }
    try {
        const response = await axios.put(`/api/records/${recordId.value}/`, formData, {
                 headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': false,
                    'processData': false
                  }
             });
          if(response.status==200){
                router.push('/records')
          }
       else{
        errorText.value="Произошла ошибка при редактировании публикации"
       }
    } catch (error) {
        console.error("Ошибка при редактировании записи:", error);
       errorText.value="Произошла ошибка при редактировании публикации"
    }
}
</script>

<template>
  <div class="add-record-container">
    <h2 class="mb-4 text-white">Редактировать материал</h2>
         <p v-if="errorText" style="color:red">{{ errorText }}</p>
        <form @submit.prevent="addRecord">
            <div class="mb-3">
                <label for="headline" class="form-label text-white">Заголовок</label>
                <input type="text" class="form-control" id="headline" v-model="headline" required>
            </div>
            <div class="mb-3">
                <label for="comment" class="form-label text-white">Комментарий</label>
                <textarea class="form-control" id="comment" v-model="comment" rows="3"></textarea>
            </div>
            <div class="mb-3">
                <label for="subject" class="form-label text-white">Предметная область</label>
                <select class="form-select" v-model="subject_id" required>
                    <option :value="null" disabled>Выберите предмет</option>
                    <option v-for="subject in subjects" :key="subject.id" :value="subject.id">{{ subject.name }}</option>
                </select>
            </div>
             <div v-if="feedback" class="mb-3">
                  <h4 class="text-white">Комментарий администратора:</h4>
                   <p class="text-white">{{ feedback.content }}</p>
                </div>
                <div class="mb-3">
                  <label for="fileInput" class="form-label text-white">Файлы</label>
                  <div class="file-input-container">
                      <ul v-if="selectedFiles.length" class="file-list">
                           <li v-for="(item, index) in selectedFiles" :key="item.id" class="file-item">
                               <button type="button" class="remove-file-button" @click="removeFile(index, item)">
                                <i class="bi bi-x-circle"></i>
                                </button>
                              <div class="file-item-content">
                                   <img v-if="item.preview && item.file?.type?.startsWith('image/')" :src="item.preview" alt="Превью" class="file-preview">
                                  <img v-else-if="item.preview" :src="item.preview" alt="Иконка файла" class="file-icon">
                                  <div class="file-name text-white">{{ item.file.name }}</div>
                              </div>
                           </li>
                      </ul>
                        <input type="file" ref="fileInput" class="form-control" id="fileInput" multiple @change="handleFileChange">
                  </div>
                </div>
            <button type="submit" class="btn btn-primary">Сохранить</button>
        </form>
    </div>
</template>

<style scoped>
.add-record-container {
    max-width: 600px;
    margin: 20px auto;
    padding: 20px;
    border-radius: 1rem;
    background-color: #343a40;
}
.form-label {
    font-weight: bold;
}

.form-control, .form-select {
  margin-bottom: 1rem;
  background-color: #495057;
   color: white;
   border-color: #495057;
}
.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
    color: white;
}
.btn-primary:hover{
  background-color: #0056b3;
    border-color: #0056b3;
}
.file-input-container{
    position: relative;
}
.file-list{
    list-style: none;
    padding: 0;
    margin-top: 10px;
      display: flex;
    flex-wrap: wrap;
}
.file-item{
  display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    border: 1px solid #eee;
    padding: 10px;
    border-radius: 4px;
    margin-bottom: 5px;
    margin-right: 5px;
     width: 150px;
     position: relative;
}
.file-name{
    font-weight: bold;
     margin-right: 10px;
     color: white;
        word-break: break-word;
         word-wrap: break-word;
}

.remove-file-button{
    background-color: transparent;
    border: none;
    cursor: pointer;
    color: #dc3545;
    font-size: 1.2rem;
    position: absolute;
    top: 5px;
    right: 5px;
}
.remove-file-button:hover{
     color: #a71d2a;
}
.file-preview{
  max-width: 50px;
    max-height: 50px;
    margin-right: 10px;
}
.file-item-content{
  display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin-bottom: 5px;
}
.file-icon{
  max-width: 50px;
    max-height: 50px;
    margin-right: 10px;
    margin-bottom: 5px;
}
</style>