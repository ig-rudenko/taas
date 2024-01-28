<template>
  <Menu/>
  <Toast/>

  <Container v-if="user">

    <UserDetail :user="user" />

    <div v-if="isMyAccount" class="mt-2">
      <div class="m-3 ml-2">
        <ChangePasswordForm @error="e => handleError(e)" @change="passwordHasBeenChanged" />
      </div>

      <div class="flex flex-wrap">
        <div class="flex flex-column gap-2 m-2">
          <label for="username">First Name</label>
          <InputText id="first_name" v-model="user.firstName"/>
        </div>
        <div class="flex flex-column gap-2 m-2">
          <label for="username">Surname</label>
          <InputText id="surname" v-model="user.surname"/>
        </div>
        <div class="flex flex-column gap-2 m-2">
          <label for="username">Last Name</label>
          <InputText id="last_name" v-model="user.lastName"/>
        </div>
      </div>
      <Button class="m-2" label="Обновить" @click="updateUserData" />
    </div>

    <UsersTestsList :userID="user._id" />

    <PassedTestsList v-if="user" :userID="user._id"/>

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

import {createNewUser, User} from "@/user.js";
import {AxiosError, AxiosResponse} from "axios";
import {HandleError} from "@/helper";

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
      user: null as User,
      showPassedTests: true,
      showChangePasswordModal: false,
    }
  },

  mounted() {
    if (!this.loggedIn && this.isMyAccount) this.$router.push("/login")
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

    getUserData(): void {
      api.get("users/"+this.accountUsername).then(
          (res: AxiosResponse) => this.user = createNewUser(res.data),
          (error: AxiosError<any>) => HandleError(this, error),
      )
    },

    updateUserData(): void {
      api.patch("users/myself", this.user).then(
          () => this.$toast.add({ severity: 'success', summary: 'Success', detail: "Данные пользователя обновлены", life: 3000 }),
          (error: AxiosError<any>) => HandleError(this, error)
      )
    },

    passwordHasBeenChanged(): void {
      this.$toast.add({ severity: 'success', summary: 'Success', detail: "Пароль был обновлен", life: 3000 });
    }
  }
})
</script>

<style scoped>

</style>