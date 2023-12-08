<template>
  <Menu :user="userData"/>
  <Toast />

  <Container v-if="userData">
    <CreateUpdateTest :create-mode="false" :test-id="testId" :user-data="userData" />
  </Container>

  <Footer/>
  <ScrollTop/>

</template>

<script>
import ScrollTop from "primevue/scrolltop";
import Toast from "primevue/toast";

import api from "@/services/api.js";
import Container from "@/components/Container.vue";
import CreateUpdateTest from "@/components/CreateUpdateTest.vue";
import Footer from "@/components/Footer.vue";
import Menu from "@/components/Menu.vue";

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
      userData: null
    }
  },

  mounted() {
    if (!this.loggedIn) this.$router.push("/login")
    this.getMyself()
  },

  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },
    testId() {
      return this.$route.params.id
    }
  },

  methods: {
    getMyself() {
      api.get("users/myself").then(res => this.userData = res.data, error => this.handleError(error))
    },

    handleError(error) {
      let message = (error.response && error.response.data && error.response.data.detail) || error.response.data || error.toString();
      this.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
    },

  }

}
</script>

<style scoped>

</style>