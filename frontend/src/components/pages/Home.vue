<template>
  <Toast />
  <Menu/>

    <div class="flex flex-wrap align-items-center justify-content-center">
      <div class="m-3 text-center">
        <h1>Test as a Service</h1>
        <p>Создавайте свои тесты и проходите другие!</p>
      </div>
      <div>
        <img class="border-round-2xl image" src="../../assets/main-img.png" alt="main-img"/>
      </div>
    </div>

  <Footer/>

</template>

<script lang="ts">
import Toast from "primevue/toast";

import Footer from "@/components/Footer.vue";
import Menu from "@/components/Menu.vue";
import api from "@/services/api.js";
import Container from "@/components/Container.vue";
import {createNewUser, User} from "@/user";

export default {
  name: "Home",
  components: {
    Container,
    Footer,
    Menu,
    Toast,
  },
}
</script>

<style scoped>
.image {
  margin: 2rem;
  width: 450px;
}

@media (width < 500px) {
  .image {
    width: 300px;
  }

}
</style>