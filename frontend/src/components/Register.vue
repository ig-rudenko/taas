<template>
  <Menu/>
  <Toast/>

  <div class="flex justify-content-center">
    <div class="register border-round border-1 border-200 p-4 mt-5">
      <h2 class="flex justify-content-center">Регистрация</h2>
      <div>
        <div class="flex flex-column gap-2 m-2">
          <label for="username">Username</label>
          <InputText id="username" v-model="user.username" :class="{'p-invalid': !userValid.username}"/>
        </div>
        <div class="flex flex-column gap-2 m-2">
          <label for="password">Email</label>
          <InputText id="password" v-model="user.email" :class="{'p-invalid': !userValid.email}" type="email"/>
        </div>
        <div class="flex flex-column gap-2 m-2">
          <label for="password">Password</label>
          <Password id="password" v-model="user.password" :class="{'p-invalid': !userValid.password}" :input-style="{width: '100%'}"/>
        </div>
        <div class="flex justify-content-center">
          <Button class="m-2" icon="pi pi-user" @click="handleRegister" label="Регистрация" style="width: 100%" />
        </div>
        <div class="cursor-pointer m-2" @click="$router.push('/login')">Уже есть аккаунт</div>
      </div>
    </div>
  </div>
</template>

<script>

import Button from "primevue/button";
import InputText from "primevue/inputtext";
import Password from "primevue/password";
import Toast from 'primevue/toast';

import Menu from "@/components/Menu.vue";

export default {
  components: {
    Button,
    Menu,
    InputText,
    Password,
    Toast,
  },

  data() {
    return {
      user: {  // #
        username: "",
        email: "",
        password: "",
      },
      userValid: {
        username: true,
        email: true,
        password: true,
      }
    };
  },

  computed: {  // #
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },
  },
  mounted() {  // #
    if (this.loggedIn) {
      this.$router.push("/");
    }
  },

  methods: {
    validate() {
      this.userValid.username = this.user.username.length > 0
      this.userValid.email = this.user.email.length > 0 && this.user.email.includes("@")
      this.userValid.password = this.user.password.length > 0
      return this.userValid.username && this.userValid.password
    },

    handleRegister() {
      if (!this.validate()) return;

      this.$store.dispatch("auth/register", this.user).then(
          (data) => {
            this.$router.push("/login")
          },
          (error) => {
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
  width: 530px;
  margin: auto;
}
</style>