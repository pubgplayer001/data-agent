<template>
  <div class="chat-window">
    <!-- Chat Header -->
    <header class="chat-header">
      <div class="chat-info">
        <h2 class="chat-title">{{ conversation?.title || 'New Conversation' }}</h2>
        <p class="chat-meta">{{ messageCount }} messages</p>
      </div>
      <div class="chat-actions">
        <button class="action-btn" @click="$emit('refresh')" aria-label="Refresh">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="23 4 23 10 17 10"></polyline>
            <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
          </svg>
        </button>
        <button class="action-btn" @click="toggleOptions" aria-label="Options">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="1"></circle>
            <circle cx="12" cy="5" r="1"></circle>
            <circle cx="12" cy="19" r="1"></circle>
          </svg>
        </button>
      </div>
    </header>

    <!-- Messages Area -->
    <div ref="messagesContainer" class="messages-area" @scroll="handleScroll">
      <div class="messages-wrapper">
        <!-- Empty State -->
        <div v-if="messages.length === 0" class="empty-messages">
          <div class="empty-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </svg>
          </div>
          <h3>Start a conversation</h3>
          <p>Send a message to begin chatting with the AI assistant</p>
        </div>

        <!-- Messages -->
        <div
          v-for="(msg, index) in messages"
          :key="msg.id"
          :class="['message-group', msg.role]"
          :style="{ animationDelay: `${index * 50}ms` }"
        >
          <div v-if="msg.role === 'bot'" class="message-avatar">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="currentColor" stroke="currentColor" stroke-width="1.5"/>
              <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="1.5"/>
              <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="1.5"/>
            </svg>
          </div>
          <div class="message-content">
            <div class="message-bubble" v-html="msg.text"></div>
            <div class="message-time">{{ formatTime(msg.timestamp || msg.id) }}</div>
          </div>
        </div>

        <!-- Typing Indicator -->
        <div v-if="isTyping" class="message-group bot typing-indicator">
          <div class="message-avatar">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="currentColor" stroke="currentColor" stroke-width="1.5"/>
              <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="1.5"/>
              <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="1.5"/>
            </svg>
          </div>
          <div class="message-content">
            <div class="message-bubble typing">
              <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Scroll to Bottom Button -->
      <button 
        v-if="showScrollButton"
        class="scroll-to-bottom"
        @click="scrollToBottom"
        aria-label="Scroll to bottom"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <polyline points="19 12 12 19 5 12"></polyline>
        </svg>
      </button>
    </div>

    <!-- Chat Input -->
    <div class="chat-input-container">
      <ChatInput @send="sendMessage" />
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, computed } from 'vue'
import ChatInput from './ChatInput.vue'

const props = defineProps({
  conversation: Object
})

const messages = ref([])
const isTyping = ref(false)
const showScrollButton = ref(false)
const messagesContainer = ref(null)

const messageCount = computed(() => messages.value.length)

watch(
  () => props.conversation,
  (newConv) => {
    messages.value = Array.isArray(newConv?.messages) ? [...newConv.messages] : []
    nextTick(() => scrollToBottom())
  },
  { immediate: true }
)

watch(
  messages,
  async () => {
    await nextTick()
    scrollToBottom()
  },
  { deep: true }
)

const handleScroll = () => {
  if (!messagesContainer.value) return
  const { scrollTop, scrollHeight, clientHeight } = messagesContainer.value
  showScrollButton.value = scrollHeight - scrollTop - clientHeight > 200
}

const scrollToBottom = (smooth = false) => {
  if (!messagesContainer.value) return
  messagesContainer.value.scrollTo({
    top: messagesContainer.value.scrollHeight,
    behavior: smooth ? 'smooth' : 'auto'
  })
}

const sendMessage = (text, files) => {
  if (!text.trim() && files.length === 0) return

  const now = Date.now()
  messages.value.push({
    id: now,
    role: 'user',
    text: text || `Sent ${files.length} file(s)`,
    timestamp: now
  })

  // Simulate bot typing
  isTyping.value = true
  setTimeout(() => {
    isTyping.value = false
    const botNow = now + 1
    messages.value.push({
      id: botNow,
      role: 'bot',
      text: 'This is a sample response. In a real application, this would be generated by your AI backend.',
      timestamp: botNow
    })
  }, 1200)
}

const formatTime = (timestamp) => {
  try {
    const d = new Date(timestamp)
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } catch {
    return ''
  }
}

const toggleOptions = () => {
  // Handle options menu
}
</script>

<style scoped>
.chat-window {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--bg-primary);
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-subtle);
  min-height: 72px;
}

.chat-info {
  flex: 1;
  min-width: 0;
}

.chat-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 4px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chat-meta {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0;
}

.chat-actions {
  display: flex;
  gap: 8px;
  margin-left: 16px;
}

.action-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  padding: 10px;
  cursor: pointer;
  border-radius: var(--radius-sm);
  transition: all var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.messages-area {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  position: relative;
  background: var(--bg-primary);
}

.messages-wrapper {
  padding: 24px;
  max-width: 900px;
  margin: 0 auto;
}

.empty-messages {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 64px 24px;
  min-height: 400px;
}

.empty-icon {
  color: var(--text-tertiary);
  margin-bottom: 24px;
  opacity: 0.5;
}

.empty-messages h3 {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.empty-messages p {
  font-size: 14px;
  color: var(--text-secondary);
  max-width: 320px;
}

.message-group {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  animation: fadeIn 0.3s ease both;
}

.message-group.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-hover));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
}

.message-content {
  flex: 1;
  min-width: 0;
  max-width: 75%;
}

.message-group.user .message-content {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.message-bubble {
  padding: 12px 16px;
  border-radius: var(--radius-lg);
  font-size: 15px;
  line-height: 1.6;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.message-group.bot .message-bubble {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-subtle);
}

.message-group.user .message-bubble {
  background: var(--accent-primary);
  color: white;
}

.message-time {
  font-size: 11px;
  color: var(--text-tertiary);
  margin-top: 6px;
  padding: 0 4px;
}

.typing-indicator .message-bubble {
  padding: 16px 20px;
}

.typing-dots {
  display: flex;
  gap: 6px;
  align-items: center;
}

.typing-dots span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--text-tertiary);
  animation: typingBounce 1.4s infinite;
}

.typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typingBounce {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.6;
  }
  30% {
    transform: translateY(-8px);
    opacity: 1;
  }
}

.scroll-to-bottom {
  position: absolute;
  bottom: 24px;
  right: 24px;
  width: 44px;
  height: 44px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-medium);
  border-radius: 50%;
  color: var(--text-primary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-md);
  transition: all var(--transition);
  z-index: 10;
}

.scroll-to-bottom:hover {
  background: var(--bg-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.chat-input-container {
  border-top: 1px solid var(--border-subtle);
  background: var(--bg-secondary);
  padding: 16px 24px;
}

/* Tablet */
@media (max-width: 1024px) {
  .messages-wrapper {
    padding: 20px;
  }

  .message-content {
    max-width: 80%;
  }
}

/* Mobile */
@media (max-width: 768px) {
  .chat-header {
    padding: 12px 16px;
    min-height: 64px;
  }

  .chat-title {
    font-size: 16px;
  }

  .chat-meta {
    font-size: 12px;
  }

  .messages-wrapper {
    padding: 16px;
  }

  .message-content {
    max-width: 85%;
  }

  .message-bubble {
    font-size: 14px;
    padding: 10px 14px;
  }

  .message-avatar {
    width: 32px;
    height: 32px;
  }

  .message-avatar svg {
    width: 16px;
    height: 16px;
  }

  .chat-input-container {
    padding: 12px 16px;
  }

  .scroll-to-bottom {
    bottom: 16px;
    right: 16px;
    width: 40px;
    height: 40px;
  }

  .empty-messages {
    padding: 48px 16px;
  }
}

/* Small Mobile */
@media (max-width: 480px) {
  .message-content {
    max-width: 90%;
  }

  .chat-actions {
    gap: 4px;
  }

  .action-btn {
    padding: 8px;
  }
}
</style>