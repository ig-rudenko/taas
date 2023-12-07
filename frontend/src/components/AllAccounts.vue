<template>
  <Menu :user="userData"/>
  <Toast/>

  <Container>
    <div class="flex flex-wrap justify-content-center">
      <div v-for="user in users" class="p-3">
        <UserDetail :user-data="user" :show-link="true" />
      </div>
    </div>

  </Container>

</template>

<script>
import Toast from "primevue/toast";

import Menu from "@/components/Menu.vue";
import api from "@/services/api.js";
import UserDetail from "@/components/UserDetail.vue";
import Container from "@/components/Container.vue";

export default {
  name: "AllAccounts",
  components: {
    Container,
    UserDetail,
    Menu,
    Toast,
  },

  data() {
    return {
      users: null,
      userData: null,
    }
  },

  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },

  },

  mounted() {
    if (!this.loggedIn) this.$router.push("/login")
    this.getMyself()
    this.getAllUsersList()
  },

  methods: {

    getMyself() {
      api.get("users/myself").then(res => this.userData = res.data, error => this.handleError(error))
    },

    getAllUsersList() {
      api.get("users/").then(
          res => {
            this.users = res.data
          },
          error => this.handleError(error)
      )
    },

    handleError(error) {
      let message = (error.response && error.response.data && error.response.data.detail) || error.response.data || error.toString();
      this.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
    }

  }
}
</script>

<style scoped>

</style>