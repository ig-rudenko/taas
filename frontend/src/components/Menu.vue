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
import themeSwitch from "@/theming.js";

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

        if (this.user && this.user.is_superuser) {
          data.push({
            label: 'Пользователи',
            icon: 'pi pi-user',
            command: () => this.$router.push('/users')
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

      data.push(
          {
            label: "",
            icon: () => themeSwitch.current.includes("light")?"pi pi-moon":"pi pi-sun",
            command: () => this.toggleTheme()
          }
      )

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

    toggleTheme() {
      this.$primevue.changeTheme(themeSwitch.current, themeSwitch.other, "theme-link", (e) => {})
      themeSwitch.newTheme(themeSwitch.other)
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