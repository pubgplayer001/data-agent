<template>
  <div class="d-flex flex-column h-100">
    <header class="d-flex align-items-center justify-content-between border-bottom p-3">
      <div>
        <h5 class="mb-0">{{ conversation?.title || 'New Conversation' }}</h5>
        <small class="text-muted">ID: {{ conversation?.id || '—' }}</small>
      </div>
      <div>
        <button class="btn btn-sm btn-outline-secondary" @click="$emit('refresh')"><i class="bi bi-arrow-repeat"></i> Refresh</button>
      </div>
    </header>

    <div ref="messagesContainer" class="flex-fill overflow-auto p-3 d-flex flex-column gap-2" role="log" aria-live="polite">
      <div
        v-for="msg in messages"
        :key="msg.id"
        :class="['d-flex w-100', msg.role === 'user' ? 'justify-content-end' : 'justify-content-start']"
      >
        <div :class="['p-2 rounded', msg.role === 'user' ? 'bg-primary text-white' : 'bg-light text-dark']" style="max-width:72%;">
          <div class="mb-1" v-html="msg.text"></div>
          <div class="text-muted small text-end">{{ formatTime(msg.timestamp || msg.id) }}</div>
        </div>
      </div>
    </div>

    <div class="border-top p-3">
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
    messages.value = Array.isArray(newConv?.messages) ? [...newConv.messages] : []
    nextTick(() => scrollToBottom())
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
/* ensure chat window full height in its column */
</style>