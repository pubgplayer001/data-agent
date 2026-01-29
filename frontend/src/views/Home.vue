<template>
  <div class="app-layout">
    <Sidebar
      v-if="isLoggedIn"
      :conversations="conversations"
      :activeConversation="activeConversation"
      @select="selectConversation"
    />

    <main class="main-area">
      <ChatWindow
        v-if="isLoggedIn"
        :conversation="activeConversation"
      />
      <div v-else class="logged-out">
        <h2>Welcome</h2>
        <p>Please login to start chatting</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import ChatWindow from '@/components/chat/ChatWindow.vue'

const isLoggedIn = computed(() => !!localStorage.getItem('token'))

// dummy data for now
const conversations = ref([
  { id: 1, title: 'Project ideas' },
  { id: 2, title: 'Flask doubts' },
  { id: 3, title: 'Random chat' }
])

const activeConversation = ref(conversations.value[0])

const selectConversation = (conv) => {
  activeConversation.value = conv
}
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  background: #f7f7f8;
}

.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
}

</style>
