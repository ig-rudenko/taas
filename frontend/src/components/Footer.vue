<template>

  <div class="footer">
    <Divider/>

    <div class="flex justify-content-center my-5 align-items-center">
      <div class="mr-5">
        Tests as a Service
      </div>
      <a href="https://github.com/ig-rudenko/taas" class="text-black-alpha-90" target="_blank">
        <i class="pi pi-github" style="font-size: 2.5rem"/>
      </a>
    </div>

  </div>

</template>

<script>
import Divider from "primevue/divider";

export default {
  name: "Footer",
  components: {
    Divider,
  }
}
</script>

<style>

.footer {
  flex: 0 0 auto;
}
</style>