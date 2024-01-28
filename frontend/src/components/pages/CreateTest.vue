<template>
  <Menu/>
  <Toast />

  <Container v-if="user">
    <CreateUpdateTest :create-mode="true"/>
  </Container>

  <Footer/>
  <ScrollTop/>

</template>

<script lang="ts">
import ScrollTop from "primevue/scrolltop";
import Toast from "primevue/toast";

import Container from "@/components/Container.vue";
import CreateUpdateTest from "@/components/CreateUpdateTest.vue";
import Footer from "@/components/Footer.vue";
import Menu from "@/components/Menu.vue";
import {User} from "@/user.js";

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
  },

}
</script>

<style scoped>

</style>