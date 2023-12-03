<template>
  <div class="card">
    <Menubar :model="menuItems">
      <template #start>
        <div class="mx-3">TaaS</div>
      </template>
    </Menubar>
  </div>
</template>

<script>
import Menubar from "primevue/menubar";
import api from "@/services/api.js";

export default {
  name: "Home",
  components: {
    Menubar,
  },

  props: {
    user: {required: false, type: Object, default: null},
  },

  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },
    menuItems() {
      let data = [
        {
          label: 'Главная',
          icon: 'pi pi-home',
          command: () => this.$router.push('/')
        },
        {
          label: 'Тесты',
          icon: 'pi pi-th-large',
          command: () => this.$router.push('/tests')
        },
      ]

      if (this.loggedIn) {

        if (this.user && this.user.can_create_tests) {
          data.push({
            label: 'Создать тест',
            icon: 'pi pi-check-circle',
            command: () => this.$router.push('/create')
          })
        }
        data.push({
          label: 'Аккаунт',
          icon: 'pi pi-user',
          command: () => this.$router.push('/account')
        },
        {
          label: 'Выйти',
          icon: 'pi pi-sign-out',
          command: () => this.logout()
        });

      } else {
        data.push({
          label: 'Войти',
          icon: 'pi pi-user',
          command: () => this.$router.push('/login')
        });
      }

      return data
    }
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
    },
    logout() {  // #
      this.$store.dispatch("auth/logout").then(
          () => {
            this.$router.push("/login");
          },
      );
    },
  }
}
</script>

<style scoped>

</style>