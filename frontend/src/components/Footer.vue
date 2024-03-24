<template>

  <div class="footer">
    <Divider/>

    <div class="flex justify-content-center my-5 align-items-center">
      <div class="mr-5">&copy; 2023-2024</div>
      <div class="mr-5">
        Tests as a Service
      </div>
      <a href="https://github.com/ig-rudenko/taas" class="no-decoration" target="_blank">
        <i class="pi pi-github" style="font-size: 2.5rem"/>
      </a>
    </div>

  </div>

</template>

<script lang="ts" setup>
import Divider from "primevue/divider";
</script>

<style>

.footer {
  flex: 0 0 auto;
}

.no-decoration {
  text-decoration: none;
}
</style>