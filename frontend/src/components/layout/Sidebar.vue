<template>
  <aside :class="['sidebar d-flex flex-column h-100 bg-white', { collapsed }]">
    <div class="top d-flex align-items-center p-3 border-bottom">
      <button
        class="btn btn-sm btn-outline-primary me-2"
        @click="toggle"
        :title="collapsed ? 'Expand' : 'Collapse'"
        aria-label="Toggle sidebar"
      >
        <i class="bi bi-list"></i>
      </button>

      <div v-if="!collapsed" class="d-flex align-items-center gap-2">
        <img src="@/assets/logo.svg" alt="logo" width="28" height="28" />
        <strong class="m-0">Data Agent</strong>
      </div>
    </div>

    <div class="flex-fill overflow-auto p-2">
      <ConversationList
        :conversations="conversations"
        :active="activeConversation"
        @select="$emit('select', $event)"
      />
    </div>

    <div class="p-3 border-top">
      <UserMenu />
    </div>
  </aside>
</template>

<script setup>
import { ref } from 'vue'
import ConversationList from '@/components/conversation/ConversationList.vue'
import UserMenu from './UserMenu.vue'

defineProps(['conversations', 'activeConversation'])
const collapsed = ref(false)

const toggle = () => {
  collapsed.value = !collapsed.value
}
</script>

<style scoped>
.sidebar {
  width: 280px;
  min-width: 72px;
  max-width: 320px;
  border-right: 1px solid #dee2e6;
  transition: width 0.3s ease;
  overflow: hidden;
}

.sidebar.collapsed {
  width: 72px;
}

.sidebar .top img {
  display: inline-block;
}

.sidebar.collapsed strong,
.sidebar.collapsed .top .brand-text {
  display: none;
}
</style>