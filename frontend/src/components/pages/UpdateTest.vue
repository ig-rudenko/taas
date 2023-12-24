<template>
  <Menu/>
  <Toast />

  <Container v-if="user">
    <CreateUpdateTest :create-mode="false" :test-id="testId" />
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
import {createNewUser, User} from "@/user";

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

  mounted() {
    if (!this.loggedIn) this.$router.push("/login")
  },

  computed: {
    loggedIn(): boolean {
      return this.$store.state.auth.status.loggedIn;
    },
    user(): User | null {
      return this.$store.state.auth.user
    },
    testId(): string {
      return this.$route.params.id
    }
  },

  methods: {
    handleError(error: any) {
      let message = (error.response && error.response.data && error.response.data.detail) || error.response.data || error.toString();
      this.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
    },

  }

}
</script>

<style scoped>

</style>