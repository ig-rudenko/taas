<template>
  <Menu/>
  <Toast/>

  <Container v-if="userData">
    <div class="mt-5 flex align-items-center">
      <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" :fill="'#545454'" class="mr-3" viewBox="0 0 16 16">
        <path d="M1.5 1a.5.5 0 0 0-.5.5v3a.5.5 0 0 1-1 0v-3A1.5 1.5 0 0 1 1.5 0h3a.5.5 0 0 1 0 1zM11 .5a.5.5 0 0 1 .5-.5h3A1.5 1.5 0 0 1 16 1.5v3a.5.5 0 0 1-1 0v-3a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 1-.5-.5M.5 11a.5.5 0 0 1 .5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 1 0 1h-3A1.5 1.5 0 0 1 0 14.5v-3a.5.5 0 0 1 .5-.5m15 0a.5.5 0 0 1 .5.5v3a1.5 1.5 0 0 1-1.5 1.5h-3a.5.5 0 0 1 0-1h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 1 .5-.5"/>
        <path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zm8-9a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
      </svg>
      <div style="font-size: 2rem">{{userData.username}}</div>
    </div>

    <div class="my-3 text-500 flex flex-row">
      <div class="mx-2 flex align-items-center">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="mr-2" viewBox="0 0 16 16">
          <path d="M2 2a2 2 0 0 0-2 2v8.01A2 2 0 0 0 2 14h5.5a.5.5 0 0 0 0-1H2a1 1 0 0 1-.966-.741l5.64-3.471L8 9.583l7-4.2V8.5a.5.5 0 0 0 1 0V4a2 2 0 0 0-2-2zm3.708 6.208L1 11.105V5.383zM1 4.217V4a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v.217l-7 4.2z"/>
          <path d="M14.247 14.269c1.01 0 1.587-.857 1.587-2.025v-.21C15.834 10.43 14.64 9 12.52 9h-.035C10.42 9 9 10.36 9 12.432v.214C9 14.82 10.438 16 12.358 16h.044c.594 0 1.018-.074 1.237-.175v-.73c-.245.11-.673.18-1.18.18h-.044c-1.334 0-2.571-.788-2.571-2.655v-.157c0-1.657 1.058-2.724 2.64-2.724h.04c1.535 0 2.484 1.05 2.484 2.326v.118c0 .975-.324 1.39-.639 1.39-.232 0-.41-.148-.41-.42v-2.19h-.906v.569h-.03c-.084-.298-.368-.63-.954-.63-.778 0-1.259.555-1.259 1.4v.528c0 .892.49 1.434 1.26 1.434.471 0 .896-.227 1.014-.643h.043c.118.42.617.648 1.12.648Zm-2.453-1.588v-.227c0-.546.227-.791.573-.791.297 0 .572.192.572.708v.367c0 .573-.253.744-.564.744-.354 0-.581-.215-.581-.8Z"/>
        </svg>
        Email: {{userData.email}}
      </div>

      <div class="mx-2 flex align-items-center">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="mr-2" viewBox="0 0 16 16">
          <path d="M10.854 8.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 0 1 .708-.708L7.5 10.793l2.646-2.647a.5.5 0 0 1 .708 0z"/>
          <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5M2 2a1 1 0 0 0-1 1v11a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1z"/>
          <path d="M2.5 4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5H3a.5.5 0 0 1-.5-.5z"/>
        </svg>
        Зарегистрирован: {{formatDate(userData.registration_date)}}
      </div>
    </div>

    <div class="mt-5">
      <div class="flex flex-wrap">
        <div class="flex flex-column gap-2 my-2">
          <label for="username">First Name</label>
          <InputText id="first_name" v-model="userData.first_name"/>
        </div>
        <div class="flex flex-column gap-2 m-2">
          <label for="username">Surname</label>
          <InputText id="surname" v-model="userData.surname"/>
        </div>
        <div class="flex flex-column gap-2 m-2">
          <label for="username">Last Name</label>
          <InputText id="last_name" v-model="userData.last_name"/>
        </div>
      </div>
      <Button label="Обновить" @click="updateUserData" />
    </div>


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

    <div v-show="showPassedTests" >
      <PassedTestsList :userID="userData._id"/>
    </div>

  </Container>

</template>

<script>
import Button from "primevue/button";
import InputText from "primevue/inputtext";
import Toast from 'primevue/toast';

import Container from "@/components/Container.vue";
import Menu from "@/components/Menu.vue";
import api from "@/services/api.js";
import PassedTestsList from "@/components/PassedTestsList.vue";

export default {
  name: "Account",
  components: {
    Button,
    Container,
    InputText,
    Menu,
    PassedTestsList,
    Toast,
  },

  data() {
    return {
      userData: null,
      showPassedTests: false,
    }
  },

  mounted() {
    if (!this.loggedIn) this.$router.push("/login")

    api.get("user/myself").then(
        res => this.userData = res.data,
        error => {
          let message = (error.response && error.response.data && error.response.data.detail) || error.response.data || error.toString();
          this.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
        }
    )
  },

  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },
  },
  methods: {
    formatDate(date) {
      let d = new Date(date)
      return new Intl.DateTimeFormat("ru", {day: "numeric", month: "long", year: "numeric", hour: "numeric", minute: "numeric"}).format(d)
    },

    updateUserData() {
      api.patch("user/myself", this.userData).then(
          () => {this.$toast.add({ severity: 'success', summary: 'Success', detail: "Данные пользователя обновлены", life: 3000 });},
          error => {
            let message = (error.response && error.response.data && error.response.data.detail) || error.response.data || error.toString();
            this.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
          }
      )
    }
  }
}
</script>

<style scoped>

</style>