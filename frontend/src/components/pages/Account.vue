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

    <UsersTestsList :userID="userData._id" />

    <PassedTestsList v-if="userData" :userID="userData._id"/>

  </Container>

  <Footer/>
  <ScrollTop/>

</template>

<script lang="ts">
import { defineComponent } from 'vue'
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
import UsersTestsList from "@/components/UsersTestsList.vue";

import {User} from "@/types.ts";

export default defineComponent({
  name: "Account",
  components: {
    UsersTestsList,
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
      userData: null as User,
      currentUser: null as User,
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
    loggedIn(): boolean {
      return this.$store.state.auth.status.loggedIn;
    },
    accountUsername(): string {
      if (this.$route.params && this.$route.params.username) {
        return this.$route.params.username
      }
      return "myself"
    },
    isMyAccount(): boolean {
      return this.accountUsername === "myself"
    }
  },

  methods: {

    getCurrentUser(): void {
      api.get("users/myself").then(
          res => {
            this.currentUser = new User(...res.data)
            if (this.isMyAccount) {this.userData = res.data}
          },
          error => this.handleError(error)
      )
    },

    getUserData(): void {
      if (this.isMyAccount) return;

      api.get("users/"+this.accountUsername).then(
          res => this.userData = new User(...res.data),
          error => this.handleError(error)
      )
    },

    updateUserData(): void {
      api.patch("users/myself", this.userData).then(
          () => {this.$toast.add({ severity: 'success', summary: 'Success', detail: "Данные пользователя обновлены", life: 3000 });},
          error => this.handleError(error)
      )
    },

    handleError(error: any): void {
      let message = (error.response && error.response.data && error.response.data.detail) || error.response.data || error.toString();
      this.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
    },

    passwordHasBeenChanged(): void {
      this.$toast.add({ severity: 'success', summary: 'Success', detail: "Пароль был обновлен", life: 3000 });
    }
  }
})
</script>

<style scoped>

</style>