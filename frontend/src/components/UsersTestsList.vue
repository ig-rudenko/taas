<template>

  <div class="my-4 flex align-items-end">
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="mr-2" viewBox="0 0 16 16">
      <path d="M12.5 3a.5.5 0 0 1 0 1h-5a.5.5 0 0 1 0-1zm0 3a.5.5 0 0 1 0 1h-5a.5.5 0 0 1 0-1zm.5 3.5a.5.5 0 0 0-.5-.5h-5a.5.5 0 0 0 0 1h5a.5.5 0 0 0 .5-.5m-.5 2.5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1 0-1z"/>
      <path d="M16 2a2 2 0 0 0-2-2H2a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2zM4 1v14H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zm1 0h9a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H5z"/>
    </svg>
    <h2 @click="showUsersTests = !showUsersTests" class="cursor-pointer mb-0 mt-3">Ваши тесты</h2>
    <div @click="showUsersTests = !showUsersTests" class="cursor-pointer">
      <svg v-if="showUsersTests" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="ml-2" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z"/>
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="ml-2" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/>
      </svg>
    </div>
  </div>

  <div v-if="showUsersTests && tests">
    <TestCard v-for="test in tests" :test="test" :edit-link="true" :show-user="false"/>
  </div>

  <div v-if="tests && !tests.length">
    Вы не создали ни единого теста
  </div>

</template>

<script lang="ts">
import Toast from "primevue/toast";

import api from "@/services/api";
import TestCard from "@/components/TestCard.vue";
import {createNewTestAboutList, TestAbout} from "@/questions";

export default {
  name: "UsersTestsList",
  components: {
    TestCard,
    Toast,
  },

  props: {
    userID: {required: true, type: String},
  },

  data() {
    return {
      tests: null as Array<TestAbout>,
      showUsersTests: false,
    }
  },

  mounted() {
    api.get("users/"+this.userID+"/questions").then(
        value => this.tests = createNewTestAboutList(value.data),
        error => {
          let message = (error.response && error.response.data && error.response.data.detail) || error.response.data || error.toString();
          this.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
        }
    )
  },

}
</script>

<style scoped>

</style>