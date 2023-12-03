<template>
  <div class="card">
    <Menubar :model="menuItems">
      <template #start>
        TaaS
      </template>
      <template #end>

      </template>
    </Menubar>
  </div>
</template>

<script>
import Menubar from "primevue/menubar";

export default {
  name: "Home",
  components: {
    Menubar,
  },
  data() {
    return {}
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