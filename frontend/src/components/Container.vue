<template>
  <div id="content" class="flex justify-content-center">
    <div class="main-container">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.main-container {
  width: 80%;
  margin-bottom: 2rem;
}

#content {
  display: block;
  flex: 1 0 auto;
}

@media (width < 1111px) {
  .main-container {
    width: 100%;
    padding: 0.5rem;
  }
}
</style>