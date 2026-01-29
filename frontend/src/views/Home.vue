<template>
  <div class="container-fluid vh-100 p-0">
    <div class="row g-0 h-100">
      <!-- Sidebar column: no inline width so Sidebar CSS controls width -->
      <div class="col-auto p-0">
        <Sidebar
          :conversations="conversations"
          :activeConversation="activeConversation"
          @select="selectConversation"
        />
      </div>

      <!-- Main area: fill rest -->
      <div class="col p-0 d-flex flex-column">
        <ChatWindow v-if="isLoggedIn" :conversation="activeConversation" />
        <div v-else class="d-flex align-items-center justify-content-center h-100">
          <div class="text-center p-4">
            <h2>Welcome</h2>
            <p>Please login to start chatting</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import ChatWindow from '@/components/chat/ChatWindow.vue'

const isLoggedIn = computed(() => !!localStorage.getItem('token'))

// dummy data for now
const conversations = ref([
  { id: 1, title: 'Project ideas', lastText: 'Kickoff notes', updatedAt: Date.now() - 1000 * 60 * 60 },
  { id: 2, title: 'Flask doubts', lastText: 'Routes issue', updatedAt: Date.now() - 1000 * 60 * 10 },
  { id: 3, title: 'Random chat', lastText: 'Hello!', updatedAt: Date.now() - 1000 * 60 * 2 }
])

const activeConversation = ref(conversations.value[0])

const selectConversation = (conv) => {
  activeConversation.value = conv
}
</script>

<style scoped>
/* ensure full height rows */
.row.h-100 { height: 100%; }
</style>
