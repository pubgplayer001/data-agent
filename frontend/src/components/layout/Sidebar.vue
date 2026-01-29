<template>
  <aside :class="['sidebar', { 'sidebar-open': isOpen }]">
    <!-- Sidebar Header -->
    <div class="sidebar-header">
      <div class="brand">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
          <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="url(#sidebarGrad)" stroke="currentColor" stroke-width="2"/>
          <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2"/>
          <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2"/>
          <defs>
            <linearGradient id="sidebarGrad" x1="2" y1="2" x2="22" y2="12">
              <stop offset="0%" stop-color="#3b82f6"/>
              <stop offset="100%" stop-color="#2563eb"/>
            </linearGradient>
          </defs>
        </svg>
        <span class="brand-text">Data Agent</span>
      </div>
      <button class="close-btn" @click="$emit('close')" aria-label="Close sidebar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>

    <!-- New Chat Button -->
    <div class="new-chat-section">
      <button class="new-chat-btn" @click="createNewChat">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        <span>New Chat</span>
      </button>
    </div>

    <!-- Conversation List -->
    <div class="conversations-container">
      <ConversationList
        :conversations="conversations"
        :active="activeConversation"
        @select="handleSelect"
      />
    </div>

    <!-- User Menu -->
    <div class="sidebar-footer">
      <UserMenu />
    </div>
  </aside>
</template>

<script setup>
import ConversationList from '@/components/conversation/ConversationList.vue'
import UserMenu from './UserMenu.vue'

defineProps({
  conversations: Array,
  activeConversation: Object,
  isOpen: Boolean
})

const emit = defineEmits(['select', 'close'])

const handleSelect = (conv) => {
  emit('select', conv)
}

const createNewChat = () => {
  // Emit event to parent to create new chat
  emit('close')
}
</script>

<style scoped>
.sidebar {
  width: 280px;
  height: 100vh;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 30;
  transition: transform var(--transition);
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  border-bottom: 1px solid var(--border-subtle);
  min-height: 64px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand svg {
  flex-shrink: 0;
  color: var(--accent-primary);
}

.brand-text {
  font-weight: 700;
  font-size: 16px;
  color: var(--text-primary);
}

.close-btn {
  display: none;
  background: none;
  border: none;
  color: var(--text-secondary);
  padding: 8px;
  cursor: pointer;
  border-radius: var(--radius-sm);
  transition: all var(--transition);
}

.close-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.new-chat-section {
  padding: 16px;
  border-bottom: 1px solid var(--border-subtle);
}

.new-chat-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: var(--accent-primary);
  color: white;
  border: none;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all var(--transition);
}

.new-chat-btn:hover {
  background: var(--accent-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.new-chat-btn:active {
  transform: translateY(0);
}

.conversations-container {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid var(--border-subtle);
  background: var(--bg-secondary);
}

/* Tablet and Mobile */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    transform: translateX(-100%);
    z-index: 50;
    box-shadow: var(--shadow-md);
  }

  .sidebar-open {
    transform: translateX(0);
  }

  .close-btn {
    display: flex;
  }

  .sidebar-header {
    min-height: 56px;
  }
}

/* Small Mobile */
@media (max-width: 480px) {
  .sidebar {
    width: 85vw;
    max-width: 320px;
  }

  .new-chat-btn {
    font-size: 13px;
    padding: 10px 14px;
  }
}
</style>