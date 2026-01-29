<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div id="app-root">
    <RouterView />
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg-primary: #0a0a0a;
  --bg-secondary: #151515;
  --bg-tertiary: #1f1f1f;
  --bg-elevated: #252525;
  --bg-hover: #2a2a2a;
  
  --text-primary: #ffffff;
  --text-secondary: #a3a3a3;
  --text-tertiary: #737373;
  
  --accent-primary: #3b82f6;
  --accent-hover: #2563eb;
  --accent-light: rgba(59, 130, 246, 0.15);
  
  --border-subtle: rgba(255, 255, 255, 0.06);
  --border-medium: rgba(255, 255, 255, 0.1);
  
  --success: #22c55e;
  --danger: #ef4444;
  
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.5);
  
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  
  --transition: 200ms cubic-bezier(0.4, 0, 0.2, 1);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body, #app {
  height: 100%;
  font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  overflow: hidden;
}

#app-root {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: var(--bg-elevated);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--bg-hover);
}

::selection {
  background: var(--accent-primary);
  color: white;
}

:focus-visible {
  outline: 2px solid var(--accent-primary);
  outline-offset: 2px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
  from { opacity: 0; transform: translateX(-12px); }
  to { opacity: 1; transform: translateX(0); }
}
</style>