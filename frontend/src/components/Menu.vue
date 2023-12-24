<template>
  <div class="card">
    <Menubar :model="menuItems">
      <template #start>
        <div class="mx-3">TaaS</div>
      </template>
    </Menubar>
  </div>
</template>

<script lang="ts">
import Menubar from "primevue/menubar";
import themeSwitch from "@/theming";
import {User} from "@/user";


export default {
  name: "Home",
  components: {
    Menubar,
  },

  data() {
    return {
      themeIcon: themeSwitch.current.includes("light")?"pi pi-moon":"pi pi-sun"
    }
  },

  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },

    user(): User | null {
      return this.$store.state.auth.user
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

        if (this.user && this.user.canCreateTests) {
          data.push({
            label: 'Создать тест',
            icon: 'pi pi-check-circle',
            command: () => this.$router.push('/create')
          })
        }

        if (this.user && this.user.isSuperuser) {
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
            icon: this.themeIcon,
            command: () => this.toggleTheme()
          }
      )

      return data
    }
  },

  methods: {
    toggleTheme() {
      this.$primevue.changeTheme(themeSwitch.current, themeSwitch.other, "theme-link", () => {})
      themeSwitch.toggle()
      this.changeThemeIcon()
    },

    changeThemeIcon() {
      this.themeIcon = themeSwitch.current.includes("light")?"pi pi-moon":"pi pi-sun"
    },

    logout() {  // #
      this.$store.dispatch("auth/logout").then(
          () => this.$router.push("/login"),
      );
    },
  }
}
</script>

<style scoped>

</style>