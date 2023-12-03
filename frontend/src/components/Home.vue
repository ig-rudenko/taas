<template>
  <Menu/>

</template>

<script>

import Menu from "@/components/Menu.vue";

export default {
  name: "Home",
  components: {
    Menu,
  },
  data() {
    return {}
  },
  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },
  }
}
</script>

<style scoped>

</style>