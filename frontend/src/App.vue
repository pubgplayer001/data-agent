<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="min-vh-100 d-flex flex-column">
    <RouterView />
  </div>
</template>

<style>
/* ensure full height app root */
html, body, #app {
  height: 100%;
  margin: 0;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

* {
  box-sizing: border-box;
}

/* ensure top-level layout fills available space */
.app-layout,
.app-layout > * {
  height: 100%;
}

/* ensure main content stretches when used without .app-layout present */
.main-area {
  min-height: 100%;
  display: flex;
  flex-direction: column;
}

/* small helper to avoid accidental body scroll while keeping content scrollable where intended */
body {
  overflow: hidden;
}
#app > * {
  height: 100%;
  overflow: hidden;
}
</style>
