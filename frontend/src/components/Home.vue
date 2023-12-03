<template>
  <Menu :user="userData"/>

  <Footer/>

</template>

<script>

import Footer from "@/components/Footer.vue";
import Menu from "@/components/Menu.vue";
import api from "@/services/api.js";

export default {
  name: "Home",
  components: {
    Footer,
    Menu,
  },
  data() {
    return {
      userData: null,
    }
  },

  mounted() {
    if (this.loggedIn) this.getMyself();
  },

  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },
  },

  methods: {
    getMyself() {
      api.get("user/myself").then(
          res => this.userData = res.data,
          error => {
            let message = (error.response && error.response.data && error.response.data.detail) || error.response.data || error.toString();
            this.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
          }
      )
    }
  }
}
</script>

<style scoped>
</style>