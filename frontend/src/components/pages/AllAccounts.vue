<template>
  <Menu/>
  <Toast/>

  <Container>
    <div class="flex flex-wrap justify-content-center">
      <div v-for="user in users" class="p-3">
        <UserDetail :user="user" :show-link="true" />
      </div>
    </div>

  </Container>

</template>

<script lang="ts">
import Toast from "primevue/toast";

import Menu from "@/components/Menu.vue";
import api from "@/services/api.js";
import UserDetail from "@/components/UserDetail.vue";
import Container from "@/components/Container.vue";
import {createNewUser, User} from "@/user";

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
      users: null as Array<User>,
    }
  },

  computed: {
    loggedIn(): boolean {
      return this.$store.state.auth.status.loggedIn;
    },

  },

  mounted() {
    if (!this.loggedIn) this.$router.push("/login")
    this.getAllUsersList()
  },

  methods: {

    getAllUsersList(): void {
      api.get("users/").then(
          res => this.users = this.getUsersList(res.data),
          error => this.handleError(error)
      )
    },

    handleError(error: any): void {
      let message = (error.response && error.response.data && error.response.data.detail) || error.response.data || error.toString();
      this.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
    },

    getUsersList(usersData: Array<any>): Array<User> {
      let res: Array<User> = []
      for (const user of usersData) {
        res.push(createNewUser(user))
      }
      return res
    }

  }
}
</script>

<style scoped>

</style>