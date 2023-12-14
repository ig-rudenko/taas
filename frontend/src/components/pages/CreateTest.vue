<template>
  <Menu :user="user"/>
  <Toast />

  <Container v-if="user">
    <CreateUpdateTest :create-mode="true" :user="user" />
  </Container>

  <Footer/>
  <ScrollTop/>

</template>

<script lang="ts">
import ScrollTop from "primevue/scrolltop";
import Toast from "primevue/toast";

import api from "@/services/api.js";
import Container from "@/components/Container.vue";
import CreateUpdateTest from "@/components/CreateUpdateTest.vue";
import Footer from "@/components/Footer.vue";
import Menu from "@/components/Menu.vue";
import {createNewUser, User} from "@/user.js";

export default {
  name: "CreateTest",
  components: {
    Footer,
    Container,
    CreateUpdateTest,
    Menu,
    ScrollTop,
    Toast,
  },

  data() {
    return {
      user: null as User
    }
  },

  mounted() {
    if (!this.loggedIn) this.$router.push("/login")
    this.getMyself()
  },

  computed: {
    loggedIn(): boolean {
      return this.$store.state.auth.status.loggedIn;
    },
  },

  methods: {
    getMyself(): void {
      api.get("users/myself").then(res => this.user = createNewUser(res.data), error => this.handleError(error))
    },

    handleError(error: any): void {
      let message = (error.response && error.response.data && error.response.data.detail) || error.response.data || error.toString();
      this.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
    },

  }

}
</script>

<style scoped>

</style>