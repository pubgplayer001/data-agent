<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div id="app-root" class="vh-100 d-flex flex-column bg-light text-dark">
    <RouterView />
  </div>
</template>

<style>
/* Global styles for light theme */
html, body, #app {
  height: 100%;
  margin: 0;
  font-family: 'Arial', sans-serif;
  background: #f8f9fa; /* Light background */
  color: #212529; /* Dark text */
}

* {
  box-sizing: border-box;
}

.app-layout,
.app-layout > * {
  height: 100%;
}

.main-area {
  min-height: 100%;
  display: flex;
  flex-direction: column;
}

body {
  overflow: hidden;
}

#app > * {
  height: 100%;
  overflow: hidden;
}
</style>
