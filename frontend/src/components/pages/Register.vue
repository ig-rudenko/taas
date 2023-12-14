<template>
  <Menu/>
  <Toast/>

  <Container>
    <div class="register border-round border-1 border-200 p-4 mt-5">
      <h2 class="flex justify-content-center">Регистрация</h2>
      <div>
        <div class="flex flex-column gap-2 m-2">
          <label for="username">Username</label>
          <InputText id="username" v-model="user.username" :class="{'p-invalid': !user.valid.username}"/>
        </div>
        <div class="flex flex-column gap-2 m-2">
          <label for="password">Email</label>
          <InputText id="password" v-model="user.email" :class="{'p-invalid': !user.valid.email}" type="email"/>
        </div>
        <div class="flex flex-column gap-2 m-2">
          <label for="password">Password</label>
          <Password id="password" v-model="user.password" :class="{'p-invalid': !user.valid.password}" :input-style="{width: '100%'}"/>
        </div>
        <div class="flex justify-content-center">
          <Button class="m-2" icon="pi pi-user" @click="handleRegister" label="Регистрация" style="width: 100%" />
        </div>
        <div class="cursor-pointer m-2" @click="$router.push('/login')">Уже есть аккаунт</div>
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

import {RegisterUser} from "@/types";

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
      user: new RegisterUser(),
    };
  },

  computed: {  // #
    loggedIn(): boolean {
      return this.$store.state.auth.status.loggedIn;
    },
  },
  mounted() {  // #
    if (this.loggedIn) {
      this.$router.push("/");
    }
  },

  methods: {

    handleRegister(): void {
      if (!this.user.isValid) return;

      this.$store.dispatch("auth/register", this.user).then(
          () => this.$router.push("/login"),
          error => {
            console.log(error)
            let message = (error.response && error.response.data && error.response.data.detail) || error.message || error.toString();
            this.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
          }
      );
    },

  },
};
</script>

<style scoped>

.register {
  max-width: 530px;
  margin: auto;
}
</style>