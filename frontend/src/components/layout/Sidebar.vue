<template>
  <aside :class="{ collapsed }" class="sidebar">
    <div class="top">
      <button
        class="toggle"
        :aria-expanded="!collapsed"
        :title="collapsed ? 'Expand' : 'Collapse'"
        @click="collapsed = !collapsed"
      >
        <span class="hamburger">☰</span>
      </button>

      <div v-if="!collapsed" class="brand">
        <img src="@/assets/logo.svg" alt="logo" class="brand-logo" />
        <h1 class="brand-title">Data Agent</h1>
      </div>
    </div>

    <div class="list-wrap">
      <ConversationList
        v-if="!collapsed"
        :conversations="conversations"
        :active="activeConversation"
        @select="$emit('select', $event)"
      />

      <ConversationList
        v-else
        :conversations="conversations"
        :active="activeConversation"
        @select="$emit('select', $event)"
      />
    </div>

    <div class="bottom">
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
</script>

<style scoped>
.sidebar {
  width: 260px;
  background: linear-gradient(180deg,#0f1113 0%, #17191c 100%);
  color: #e6eef8;
  display: flex;
  flex-direction: column;
  min-height: 0;
  border-right: 1px solid rgba(255,255,255,0.04);
}

.sidebar.collapsed {
  width: 72px;
}

.top {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-bottom: 1px solid rgba(255,255,255,0.03);
}

.toggle {
  background: transparent;
  border: none;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  color: inherit;
}
.toggle:focus {
  outline: 2px solid rgba(84,105,212,0.22);
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
}
.brand-logo {
  width: 30px;
  height: 30px;
  opacity: 0.95;
}
.brand-title {
  font-size: 14px;
  margin: 0;
  font-weight: 700;
  letter-spacing: 0.2px;
  color: #f5f7fb;
}

/* make list take remaining space and be scrollable */
.list-wrap {
  flex: 1;
  overflow: hidden;
}

/* bottom area keeps user menu anchored */
.bottom {
  padding: 10px;
  border-top: 1px solid rgba(255,255,255,0.02);
}

/* collapsed state tweaks */
.sidebar.collapsed .brand,
.sidebar.collapsed .brand-title {
  display: none;
}
</style>