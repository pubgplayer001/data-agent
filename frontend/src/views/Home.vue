<template>
  <div class="home-layout">
    <!-- Mobile Header -->
    <header class="mobile-header">
      <button 
        class="menu-toggle" 
        @click="toggleSidebar"
        aria-label="Toggle menu"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      </button>
      <div class="header-title">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="url(#gradient)" stroke="currentColor" stroke-width="2"/>
          <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2"/>
          <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2"/>
          <defs>
            <linearGradient id="gradient" x1="2" y1="2" x2="22" y2="12">
              <stop offset="0%" stop-color="#3b82f6"/>
              <stop offset="100%" stop-color="#2563eb"/>
            </linearGradient>
          </defs>
        </svg>
        <span>Data Agent</span>
      </div>
      <div class="header-actions">
        <button class="icon-btn" @click="startNewChat" aria-label="New chat">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </button>
      </div>
    </header>

    <!-- Overlay for mobile sidebar -->
    <div 
      v-if="sidebarOpen" 
      class="sidebar-overlay"
      @click="toggleSidebar"
    ></div>

    <!-- Sidebar -->
    <Sidebar
      :conversations="conversations"
      :activeConversation="activeConversation"
      :isOpen="sidebarOpen"
      @select="selectConversation"
      @close="closeSidebar"
    />
    
    <!-- Main Content -->
    <main class="main-content">
      <ChatWindow 
        v-if="isLoggedIn" 
        :conversation="activeConversation"
        @newChat="startNewChat"
      />
      <div v-else class="welcome-screen">
        <div class="welcome-content">
          <div class="welcome-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="url(#welcomeGrad)" stroke="currentColor" stroke-width="1.5"/>
              <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="1.5"/>
              <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="1.5"/>
              <defs>
                <linearGradient id="welcomeGrad" x1="2" y1="2" x2="22" y2="12">
                  <stop offset="0%" stop-color="#3b82f6"/>
                  <stop offset="100%" stop-color="#2563eb"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <h1>Welcome to Data Agent</h1>
          <p>Please login to start your conversation</p>
          <button class="login-btn" @click="goToLogin">
            Sign In
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import ChatWindow from '@/components/chat/ChatWindow.vue'

const isLoggedIn = computed(() => !!localStorage.getItem('token'))

const sidebarOpen = ref(false)

const conversations = ref([
  { 
    id: 1, 
    title: 'Project Planning Q1', 
    lastText: 'Let\'s finalize the roadmap...', 
    updatedAt: Date.now() - 1000 * 60 * 60,
    messages: [
      { id: 1, role: 'user', text: 'Can you help me plan our Q1 projects?', timestamp: Date.now() - 1000 * 60 * 120 },
      { id: 2, role: 'bot', text: 'I\'d be happy to help! Let\'s start by identifying your key objectives.', timestamp: Date.now() - 1000 * 60 * 119 }
    ]
  },
  { 
    id: 2, 
    title: 'API Integration Help', 
    lastText: 'Check the authentication headers', 
    updatedAt: Date.now() - 1000 * 60 * 10,
    messages: [
      { id: 1, role: 'user', text: 'I\'m having issues with the API integration', timestamp: Date.now() - 1000 * 60 * 15 },
      { id: 2, role: 'bot', text: 'Let me help you debug. Can you share the error message?', timestamp: Date.now() - 1000 * 60 * 14 }
    ]
  },
  { 
    id: 3, 
    title: 'Data Analysis Query', 
    lastText: 'Here\'s the visualization you requested', 
    updatedAt: Date.now() - 1000 * 60 * 2,
    messages: []
  }
])

const activeConversation = ref(conversations.value[0])

const selectConversation = (conv) => {
  activeConversation.value = conv
  closeSidebar()
}

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const closeSidebar = () => {
  sidebarOpen.value = false
}

const startNewChat = () => {
  const newId = Math.max(...conversations.value.map(c => c.id)) + 1
  const newConv = {
    id: newId,
    title: 'New Conversation',
    lastText: '',
    updatedAt: Date.now(),
    messages: []
  }
  conversations.value.unshift(newConv)
  activeConversation.value = newConv
  closeSidebar()
}

const goToLogin = () => {
  // router.push('/login')
  alert('Navigate to login page')
}

// Close sidebar on window resize to desktop
const handleResize = () => {
  if (window.innerWidth >= 768) {
    sidebarOpen.value = false
  }
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.home-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  position: relative;
  background: var(--bg-primary);
}

/* Mobile Header */
.mobile-header {
  display: none;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-subtle);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 40;
  height: 56px;
}

.menu-toggle {
  background: none;
  border: none;
  color: var(--text-primary);
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: var(--radius-sm);
  transition: background var(--transition);
}

.menu-toggle:hover {
  background: var(--bg-hover);
}

.header-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 16px;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.icon-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: var(--radius-sm);
  transition: all var(--transition);
}

.icon-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

/* Sidebar Overlay */
.sidebar-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  z-index: 45;
  backdrop-filter: blur(4px);
  animation: fadeIn 0.2s ease;
}

/* Main Content */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  background: var(--bg-primary);
}

/* Welcome Screen */
.welcome-screen {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 24px;
  animation: fadeIn 0.4s ease;
}

.welcome-content {
  text-align: center;
  max-width: 400px;
}

.welcome-icon {
  margin: 0 auto 24px;
  width: 64px;
  height: 64px;
  color: var(--accent-primary);
  animation: fadeIn 0.6s ease 0.2s both;
}

.welcome-content h1 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 12px;
  background: linear-gradient(135deg, var(--text-primary) 0%, var(--text-secondary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: fadeIn 0.6s ease 0.3s both;
}

.welcome-content p {
  color: var(--text-secondary);
  font-size: 16px;
  margin-bottom: 32px;
  animation: fadeIn 0.6s ease 0.4s both;
}

.login-btn {
  background: var(--accent-primary);
  color: white;
  border: none;
  padding: 12px 32px;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  transition: all var(--transition);
  animation: fadeIn 0.6s ease 0.5s both;
}

.login-btn:hover {
  background: var(--accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3);
}

/* Tablet and Mobile */
@media (max-width: 768px) {
  .mobile-header {
    display: flex;
  }

  .sidebar-overlay {
    display: block;
  }

  .main-content {
    margin-top: 56px;
  }

  .welcome-content h1 {
    font-size: 24px;
  }

  .welcome-content p {
    font-size: 14px;
  }
}

/* Small Mobile */
@media (max-width: 480px) {
  .header-title span {
    font-size: 14px;
  }

  .welcome-content {
    padding: 0 16px;
  }

  .welcome-icon {
    width: 48px;
    height: 48px;
  }

  .welcome-icon svg {
    width: 48px;
    height: 48px;
  }

  .welcome-content h1 {
    font-size: 20px;
  }
}
</style>