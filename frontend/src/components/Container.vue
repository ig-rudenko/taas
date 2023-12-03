<template>
  <div class="flex justify-content-center">
    <div class="main-container">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "Container"
}
</script>

<style scoped>
.main-container {
  width: 50%
}

@media (width < 1111px) {
  .main-container {
    width: 100%
  }
}
</style>