<template>
  <router-view/>
</template>
<script>

import themeSwitch from "@/theming.js";

export default {
  name: "App",
  mounted() {
    this.$primevue.changeTheme(themeSwitch.other, themeSwitch.current, "theme-link", () => {})
  }
}

</script>