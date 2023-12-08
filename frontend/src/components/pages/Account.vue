<template>
  <Menu :user="currentUser"/>
  <Toast/>

  <Container v-if="userData">

    <UserDetail :user-data="userData" />
    <div v-if="isMyAccount" class="mt-2">
      <div class="m-3 ml-2">
        <ChangePasswordForm :new-passwords="newPasswords" @error="e => handleError(e)" @change="passwordHasBeenChanged" />
      </div>

      <div class="flex flex-wrap">
        <div class="flex flex-column gap-2 m-2">
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
      <Button class="m-2" label="Обновить" @click="updateUserData" />
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
      <PassedTestsList v-if="userData" :userID="userData._id"/>
    </div>

  </Container>

  <Footer/>
  <ScrollTop/>

</template>

<script>
import Button from "primevue/button";
import InputText from "primevue/inputtext";
import ScrollTop from "primevue/scrolltop";
import Toast from 'primevue/toast';

import api from "@/services/api.js";
import Container from "@/components/Container.vue";
import Menu from "@/components/Menu.vue";
import PassedTestsList from "@/components/PassedTestsList.vue";
import Footer from "@/components/Footer.vue";
import UserDetail from "@/components/UserDetail.vue";
import ChangePasswordForm from "@/components/ChangePasswordForm.vue";

export default {
  name: "Account",
  components: {
    ChangePasswordForm,
    Button,
    Container,
    InputText,
    Footer,
    Menu,
    PassedTestsList,
    ScrollTop,
    Toast,
    UserDetail,
  },

  data() {
    return {
      userData: null,
      currentUser: null,
      showPassedTests: true,
      showChangePasswordModal: false,
      newPasswords: {
        password1: "",
        password2: ""
      }
    }
  },

  mounted() {
    if (!this.loggedIn && this.isMyAccount) this.$router.push("/login")

    this.getCurrentUser()
    this.getUserData()
  },

  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },
    accountUsername() {
      if (this.$route.params && this.$route.params.username) {
        return this.$route.params.username
      }
      return "myself"
    },
    isMyAccount() {
      return this.accountUsername === "myself"
    }
  },

  methods: {

    getCurrentUser() {
      api.get("users/myself").then(
          res => {
            this.currentUser = res.data
            if (this.isMyAccount) {this.userData = res.data}
          },
          error => this.handleError(error)
      )
    },

    getUserData() {
      if (this.isMyAccount) return;

      api.get("users/"+this.accountUsername).then(
          res => this.userData = res.data,
          error => this.handleError(error)
      )
    },

    updateUserData() {
      api.patch("users/myself", this.userData).then(
          () => {this.$toast.add({ severity: 'success', summary: 'Success', detail: "Данные пользователя обновлены", life: 3000 });},
          error => this.handleError(error)
      )
    },

    handleError(error) {
      let message = (error.response && error.response.data && error.response.data.detail) || error.response.data || error.toString();
      this.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
    },

    passwordHasBeenChanged() {
      this.$toast.add({ severity: 'success', summary: 'Success', detail: "Пароль был обновлен", life: 3000 });
    }
  }
}
</script>

<style scoped>

</style>