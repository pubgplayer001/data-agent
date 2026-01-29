<template>
  <div class="chat">
    <header class="chat-header">
      <div class="head-left">
        <h3 class="title">{{ conversation?.title || 'New Conversation' }}</h3>
        <small class="sub">ID: {{ conversation?.id || '—' }}</small>
      </div>
      <div class="head-actions">
        <button class="btn" @click="$emit('refresh')">⟳ Refresh</button>
      </div>
    </header>

    <div ref="messagesContainer" class="messages" role="log" aria-live="polite">
      <div
        v-for="msg in messages"
        :key="msg.id"
        :class="['message', msg.role === 'user' ? 'user' : 'bot']"
      >
        <div class="bubble">
          <div class="msg-text">{{ msg.text }}</div>
          <div class="msg-meta">{{ formatTime(msg.timestamp || msg.id) }}</div>
        </div>
      </div>
    </div>

    <div class="input-area">
      <ChatInput @send="sendMessage" />
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import ChatInput from './ChatInput.vue'

const props = defineProps(['conversation'])

const messages = ref([])

watch(
  () => props.conversation,
  (newConv) => {
    // load existing messages or reset
    messages.value = Array.isArray(newConv?.messages) ? [...newConv.messages] : []
    // small delay then scroll
    nextTick(() => {
      scrollToBottom()
    })
  },
  { immediate: true }
)

const messagesContainer = ref(null)

watch(
  messages,
  async () => {
    await nextTick()
    scrollToBottom()
  },
  { deep: true }
)

const scrollToBottom = () => {
  const el = messagesContainer.value
  if (!el) return
  el.scrollTop = el.scrollHeight
}

const sendMessage = (text) => {
  const now = Date.now()
  messages.value.push({ id: now, role: 'user', text, timestamp: now })
  // dummy bot response
  const botNow = now + 1
  setTimeout(() => {
    messages.value.push({ id: botNow, role: 'bot', text: 'Dummy reply', timestamp: botNow })
  }, 220)
}

const formatTime = (t) => {
  try {
    const d = new Date(t)
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } catch {
    return ''
  }
}
</script>

<style scoped>
.chat {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: linear-gradient(180deg,#0b0c0d,#0f1113);
  color: #eaf2ff;
}

/* header */
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid rgba(255,255,255,0.03);
}
.title {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
}
.sub {
  display: block;
  margin-top: 2px;
  color: rgba(234,242,255,0.6);
  font-size: 12px;
}
.head-actions .btn {
  background: rgba(255,255,255,0.03);
  border: none;
  padding: 8px 10px;
  border-radius: 8px;
  color: inherit;
  cursor: pointer;
}

/* messages area */
.messages {
  flex: 1;
  padding: 18px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* message bubbles */
.message {
  display: flex;
}
.message.user {
  justify-content: flex-end;
}
.message.bot {
  justify-content: flex-start;
}

.bubble {
  max-width: 72%;
  padding: 10px 12px;
  border-radius: 12px;
  background: linear-gradient(180deg,#1f2933,#15181b);
  color: #eaf2ff;
  box-shadow: 0 4px 12px rgba(2,6,23,0.6);
}
.message.user .bubble {
  background: linear-gradient(180deg,#3b82f6,#2563eb);
  color: #fff;
}

/* text + meta */
.msg-text {
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 14px;
}
.msg-meta {
  margin-top: 6px;
  font-size: 11px;
  color: rgba(234,242,255,0.6);
  text-align: right;
}

/* input area */
.input-area {
  border-top: 1px solid rgba(255,255,255,0.03);
  padding: 12px;
  background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.00));
}

/* small responsive tweaks */
@media (max-width: 720px) {
  .bubble { max-width: 86%; }
  .chat-header { padding: 10px; }
}
</style>