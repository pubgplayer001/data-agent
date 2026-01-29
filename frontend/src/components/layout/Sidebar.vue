<template>
  <div class="d-flex flex-column h-100">
    <div class="d-flex align-items-center gap-2 p-3 border-bottom">
      <button
        class="btn btn-sm btn-outline-light"
        @click="collapsed = !collapsed"
        :title="collapsed ? 'Expand' : 'Collapse'"
      >
        <i class="bi bi-list"></i>
      </button>
      <div v-if="!collapsed" class="d-flex align-items-center gap-2 ms-2">
        <img src="@/assets/logo.svg" alt="logo" style="width:28px;height:28px" />
        <strong>Data Agent</strong>
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
      <div v-if="isLoggedIn" class="d-flex align-items-center gap-2">
        <UserMenu class="flex-grow-1" />
        <button class="btn btn-sm btn-danger" @click="logout">
          <i class="bi bi-box-arrow-right"></i> Logout
        </button>
      </div>

      <div v-else class="d-flex gap-2">
        <button class="btn btn-sm btn-outline-light flex-fill" @click="goLogin">Login</button>
        <button class="btn btn-sm btn-primary flex-fill" @click="goRegister">Create account</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import ConversationList from '@/components/conversation/ConversationList.vue'
import UserMenu from './UserMenu.vue'

defineProps(['conversations', 'activeConversation'])
const collapsed = ref(false)

const router = useRouter()
const isLoggedIn = computed(() => !!localStorage.getItem('token'))

const goLogin = () => router.push('/login')
const goRegister = () => router.push('/register')
const logout = () => {
  localStorage.clear()
  router.push('/login')
}
</script>

<style scoped>
/* keep sidebar full height inside its column */
</style>