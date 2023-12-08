<template>
  <Toast/>

  <div class="my-4 flex align-items-end">
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="mr-2" viewBox="0 0 16 16">
      <path d="M12.5 3a.5.5 0 0 1 0 1h-5a.5.5 0 0 1 0-1zm0 3a.5.5 0 0 1 0 1h-5a.5.5 0 0 1 0-1zm.5 3.5a.5.5 0 0 0-.5-.5h-5a.5.5 0 0 0 0 1h5a.5.5 0 0 0 .5-.5m-.5 2.5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1 0-1z"/>
      <path d="M16 2a2 2 0 0 0-2-2H2a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2zM4 1v14H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zm1 0h9a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H5z"/>
    </svg>
    <h2 @click="showPassedTests = !showPassedTests" class="cursor-pointer mb-0 mt-3">Статистика прохождения тестов</h2>
    <div @click="showPassedTests = !showPassedTests" class="cursor-pointer">
      <svg v-if="showPassedTests" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="ml-2" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z"/>
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="ml-2" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/>
      </svg>
    </div>
  </div>

  <div v-if="showPassedTests" class="my-3">
    <div v-for="result in data" class="p-4 border-1 border-200 border-round hover:shadow-2 my-3">
      <div class="flex justify-content-between">
        <div>
          <h3>{{result.question_group_name}}</h3>
          <div class="flex flex-wrap align-items-center">
            <div class="mr-3">Пройдено {{result.user_score}} из {{result.total_score}}</div>
            <div class="flex align-items-center">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="mr-2" viewBox="0 0 16 16">
                <path d="M10.854 7.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 9.793l2.646-2.647a.5.5 0 0 1 .708 0z"/>
                <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5M1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4z"/>
              </svg>
              {{formatDate(result.created_at)}}
            </div>
          </div>
          <div class="mt-4">
            <ProgressBar :value="userPercents(result)" ></ProgressBar>
          </div>
        </div>

        <div>
          <svg v-if="testPassedSuccessfully(result)" xmlns="http://www.w3.org/2000/svg" width="86" height="86" :fill="'#74c769'" class="bi bi-emoji-smile" viewBox="0 0 16 16">
            <path d="M10.067.87a2.89 2.89 0 0 0-4.134 0l-.622.638-.89-.011a2.89 2.89 0 0 0-2.924 2.924l.01.89-.636.622a2.89 2.89 0 0 0 0 4.134l.637.622-.011.89a2.89 2.89 0 0 0 2.924 2.924l.89-.01.622.636a2.89 2.89 0 0 0 4.134 0l.622-.637.89.011a2.89 2.89 0 0 0 2.924-2.924l-.01-.89.636-.622a2.89 2.89 0 0 0 0-4.134l-.637-.622.011-.89a2.89 2.89 0 0 0-2.924-2.924l-.89.01-.622-.636zm.287 5.984-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7 8.793l2.646-2.647a.5.5 0 0 1 .708.708z"/>
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="86" height="86" :fill="'#ea6767'" class="bi bi-emoji-smile" viewBox="0 0 16 16">
            <path d="M10.067.87a2.89 2.89 0 0 0-4.134 0l-.622.638-.89-.011a2.89 2.89 0 0 0-2.924 2.924l.01.89-.636.622a2.89 2.89 0 0 0 0 4.134l.637.622-.011.89a2.89 2.89 0 0 0 2.924 2.924l.89-.01.622.636a2.89 2.89 0 0 0 4.134 0l.622-.637.89.011a2.89 2.89 0 0 0 2.924-2.924l-.01-.89.636-.622a2.89 2.89 0 0 0 0-4.134l-.637-.622.011-.89a2.89 2.89 0 0 0-2.924-2.924l-.89.01-.622-.636zM6 7.5h4a.5.5 0 0 1 0 1H6a.5.5 0 0 1 0-1"/>
          </svg>

        </div>
      </div>
    </div>

    <div v-if="data && !data.length">
      Вы не прошли ни единого теста
    </div>

  </div>

</template>

<script>
import ProgressBar from "primevue/progressbar";
import Toast from 'primevue/toast';

import api from "@/services/api.js";

export default {
  name: "PassedTestsList",
  components: {
    ProgressBar,
    Toast,
  },

  props: {
    userID: {required: true, type: String},
  },

  data() {
    return {
      data: null,
      showPassedTests: true,
    }
  },

  mounted() {
    api.get("users/"+this.userID+"/passed-questions").then(
        value => this.data = value.data,
        error => {
          let message = (error.response && error.response.data && error.response.data.detail) || error.response.data || error.toString();
          this.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
        }
    )
  },

  methods: {
    testPassedSuccessfully(test) {
      return test.user_score / test.total_score > 0.7
    },
    formatDate(date) {
      let d = new Date(date)
      return new Intl.DateTimeFormat("ru", {day: "numeric", month: "long", year: "numeric", hour: "numeric", minute: "numeric"}).format(d)
    },
    userPercents(test) {
      return Math.floor((test.user_score / test.total_score) * 100)
    },
  },

}
</script>

<style scoped>

</style>