<template>
  <Menu/>
  <Toast/>

  <Container>
    <div class="login border-round border-1 border-200 p-4 mt-5">
      <h2 class="flex justify-content-center">Пожалуйста, войдите</h2>
      <div>
        <div class="flex flex-column gap-2 m-2">
          <label for="username">Username</label>
          <InputText autofocus id="username" :class="{'p-invalid': !user.valid.username}"
                     v-model="user.username" @keydown.enter="handleLogin"/>
        </div>
        <div class="flex flex-column gap-2 m-2">
          <label for="password">Password</label>
          <InputText id="password" type="password" :class="{'p-invalid': !user.valid.password}" :input-style="{width: '100%'}"
                     v-model="user.password" @keydown.enter="handleLogin"/>
        </div>
        <div class="flex justify-content-center">
          <Button class="m-2" icon="pi pi-user" @click="handleLogin" label="Войти" style="width: 100%" />
        </div>
        <div class="cursor-pointer m-2" @click="$router.push('/register')">Нет аккаунта</div>
      </div>
    </div>
  </Container>

  <Footer/>

</template>

<script lang="ts">

import Button from "primevue/button";
import InputText from "primevue/inputtext";
import Password from "primevue/password";
import Toast from 'primevue/toast';

import Menu from "@/components/Menu.vue";
import Footer from "@/components/Footer.vue";
import Container from "@/components/Container.vue";
import {LoginUser} from "@/user";

export default {
  components: {
    Container,
    Footer,
    Button,
    Menu,
    InputText,
    Password,
    Toast,
  },

  data() {
    return {
      user: new LoginUser(),
    };
  },
  computed: {
    loggedIn(): boolean {
      return this.$store.state.auth.status.loggedIn;
    },
  },
  created() {
    if (this.loggedIn) {
      this.$router.push("/");
    }
  },
  methods: {
    handleLogin() {
      if (!this.user.isValid) return;

      this.$store.dispatch("auth/login", this.user).then(
          () => this.$router.push("/"),
          () => this.$toast.add({ severity: 'error', summary: 'Error', detail: 'Неверный логин или пароль', life: 3000 })
      );
    },

  },
};
</script>

<style>

.login {
  max-width: 530px;
  margin: auto;
}

</style>