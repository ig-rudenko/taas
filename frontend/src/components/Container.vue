<template>
  <div id="content" class="flex justify-content-center">
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
  width: 60%;
  margin-bottom: 2rem;
}

#content {
  display: block;
  flex: 1 0 auto;
}

@media (width < 1111px) {
  .main-container {
    width: 100%
  }
}
</style>