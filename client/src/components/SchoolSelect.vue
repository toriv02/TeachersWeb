<script setup>
import { ref, onMounted, computed, watch } from 'vue';
const props = defineProps({
    schools:{
        type: Array,
        required: true
    },
    modelValue:{
      type: Number
    }
})
const emit = defineEmits(['update:modelValue'])

const searchQuery = ref("");
const isOpen = ref(false);


const filteredSchools = computed(() => {
  if (!searchQuery.value) {
    return props.schools;
  }
    return props.schools.filter((school) =>
    school.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const selectedSchoolName = computed(() => {
    const selected = props.schools.find(school => school.id === props.modelValue)
    return selected ? selected.name : ''
})

function selectSchool(school) {
    emit('update:modelValue',school.id)
    searchQuery.value=school.name
    isOpen.value = false;
  }


watch(() => searchQuery.value, () => {
    isOpen.value = true
})


</script>

<template>
    <div class="form-outline form-white mb-3 school-select" >
        <input
          type="text"
          v-model="searchQuery"
          class="form-control form-control-sm"
          @focus="isOpen=true"
           @blur="setTimeout(() => isOpen = false, 150)"
           :placeholder="selectedSchoolName ? selectedSchoolName : 'Начните вводить'"
         />
        <label class="form-label" >Школа</label>
    <ul v-if="isOpen" class="school-dropdown">
      <li v-for="school in filteredSchools" :key="school.id" @click="selectSchool(school)" class="school-item">
        {{ school.name }}
      </li>
      <li v-if="filteredSchools.length===0" style="text-align: center; margin-top: 5px;">Нет совпадений</li>
    </ul>
    </div>
</template>

<style scoped>
.school-select{
    position: relative;
}
.school-dropdown{
    list-style: none;
    padding: 0;
    margin: 0;
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    background: #617bee;
    border-radius: 5px;
    z-index: 10;
     max-height: 150px;
    overflow-y: auto;
}
.school-item{
    padding: 5px 10px;
    cursor: pointer;
    color: white;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1)
}
.school-item:hover{
    background: rgba(255, 255, 255, 0.1)
}
</style>