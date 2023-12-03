<template>
  <Menu/>
  <Toast/>

  <Container>
    <div class="login border-round border-1 border-200 p-4 mt-5">
      <h2 class="flex justify-content-center">Пожалуйста, войдите</h2>
      <div>
        <div class="flex flex-column gap-2 m-2">
          <label for="username">Username</label>
          <InputText id="username" :class="{'p-invalid': !userValid.username}"
                     v-model="user.username" @keydown.enter="handleLogin"/>
        </div>
        <div class="flex flex-column gap-2 m-2">
          <label for="password">Password</label>
          <InputText id="password" type="password" :class="{'p-invalid': !userValid.password}" :input-style="{width: '100%'}"
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

<script>

import Button from "primevue/button";
import InputText from "primevue/inputtext";
import Password from "primevue/password";
import Toast from 'primevue/toast';

import Menu from "@/components/Menu.vue";
import Footer from "@/components/Footer.vue";
import Container from "@/components/Container.vue";

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
      user: {
        username: "",
        password: "",
      },
      userValid: {
        username: true,
        password: true,
      }
    };
  },
  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },
  },
  created() {
    if (this.loggedIn) {
      this.$router.push("/");
    }
  },
  methods: {

    validate() {
      this.userValid.username = this.user.username.length > 0
      this.userValid.password = this.user.password.length > 0
      return this.userValid.username && this.userValid.password
    },

    handleLogin() {
      if (!this.validate()) return;

      this.$store.dispatch("auth/login", this.user).then(
          () => {
            this.$router.push("/");
          },
          error => {
            this.$toast.add({ severity: 'error', summary: 'Error', detail: 'Неверный логин или пароль', life: 3000 });
          }
      );
    },

  },
};
</script>

<style>

.login {
  width: 530px;
  margin: auto;
}

</style>