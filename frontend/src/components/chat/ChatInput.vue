<template>
  <form @submit.prevent="onSubmit" class="chat-input-form">
    <!-- File Previews -->
    <div v-if="files.length > 0" class="file-previews">
      <div
        v-for="(file, index) in files"
        :key="index"
        class="file-chip"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path>
          <polyline points="13 2 13 9 20 9"></polyline>
        </svg>
        <span class="file-name">{{ truncateFilename(file.name) }}</span>
        <button
          type="button"
          class="file-remove"
          @click="removeFile(index)"
          aria-label="Remove file"
        >
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
    </div>

    <!-- Input Area -->
    <div class="input-wrapper">
      <!-- Attach Button -->
      <label class="attach-btn" :title="files.length ? filesLabel : 'Attach files'">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path>
        </svg>
        <input
          type="file"
          @change="onFileChange"
          multiple
          accept="*/*"
          ref="fileInput"
          aria-label="Attach files"
        />
      </label>

      <!-- Text Input -->
      <div class="textarea-container">
        <textarea
          v-model="text"
          ref="textarea"
          rows="1"
          class="message-input"
          :placeholder="placeholder"
          @keydown="onKeydown"
          @input="autoResize"
          aria-label="Message input"
        ></textarea>
      </div>

      <!-- Send Button -->
      <button
        type="submit"
        class="send-btn"
        :disabled="!canSend"
        :class="{ active: canSend }"
        aria-label="Send message"
      >
        <svg v-if="!canSend" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="22" y1="2" x2="11" y2="13"></line>
          <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
        </svg>
        <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
          <line x1="22" y1="2" x2="11" y2="13" stroke="white" stroke-width="2"></line>
          <polygon points="22 2 15 22 11 13 2 9 22 2" fill="white"></polygon>
        </svg>
      </button>
    </div>

    <!-- Character Count (optional) -->
    <div v-if="text.length > 1000" class="char-count" :class="{ warning: text.length > 2000 }">
      {{ text.length }} / 3000
    </div>
  </form>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'

const emit = defineEmits(['send'])

const placeholder = 'Type a message...'
const text = ref('')
const files = ref([])
const textarea = ref(null)
const fileInput = ref(null)

const canSend = computed(() => text.value.trim().length > 0 || files.value.length > 0)
const filesLabel = computed(() => files.value.map(f => f.name).join(', '))

const onFileChange = (e) => {
  const newFiles = Array.from(e.target.files || [])
  if (newFiles.length) {
    files.value = [...files.value, ...newFiles]
  }
  if (fileInput.value) {
    fileInput.value.value = ''
  }
  nextTick(() => textarea.value?.focus())
}

const removeFile = (index) => {
  files.value.splice(index, 1)
}

const truncateFilename = (name) => {
  if (name.length <= 30) return name
  const ext = name.split('.').pop()
  const nameWithoutExt = name.substring(0, name.lastIndexOf('.'))
  return `${nameWithoutExt.substring(0, 20)}...${ext}`
}

const autoResize = () => {
  nextTick(() => {
    if (!textarea.value) return
    textarea.value.style.height = 'auto'
    const newHeight = Math.min(textarea.value.scrollHeight, 180)
    textarea.value.style.height = `${newHeight}px`
  })
}

const onKeydown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    onSubmit()
  }
}

const onSubmit = () => {
  if (!canSend.value) return

  emit('send', text.value.trim(), files.value.length ? [...files.value] : [])

  // Reset
  text.value = ''
  files.value = []

  nextTick(() => {
    if (textarea.value) {
      textarea.value.style.height = 'auto'
      textarea.value.focus()
    }
  })
}

// Auto-focus on mount
nextTick(() => {
  textarea.value?.focus()
})
</script>

<style scoped>
.chat-input-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}

.file-previews {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.file-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  font-size: 13px;
  color: var(--text-secondary);
  max-width: 200px;
}

.file-chip svg:first-child {
  color: var(--accent-primary);
  flex-shrink: 0;
}

.file-name {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-remove {
  background: none;
  border: none;
  color: var(--text-tertiary);
  padding: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all var(--transition);
  flex-shrink: 0;
}

.file-remove:hover {
  background: var(--bg-hover);
  color: var(--danger);
}

.input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  background: var(--bg-tertiary);
  border: 2px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 8px 12px;
  transition: border-color var(--transition);
}

.input-wrapper:focus-within {
  border-color: var(--accent-primary);
}

.attach-btn {
  position: relative;
  background: none;
  border: none;
  color: var(--text-secondary);
  padding: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  transition: all var(--transition);
  flex-shrink: 0;
}

.attach-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.attach-btn input[type="file"] {
  position: absolute;
  width: 1px;
  height: 1px;
  opacity: 0;
  pointer-events: none;
}

.textarea-container {
  flex: 1;
  min-width: 0;
}

.message-input {
  width: 100%;
  min-height: 24px;
  max-height: 180px;
  background: transparent;
  border: none;
  color: var(--text-primary);
  font-size: 15px;
  line-height: 1.6;
  resize: none;
  outline: none;
  font-family: inherit;
  padding: 0;
}

.message-input::placeholder {
  color: var(--text-tertiary);
}

.send-btn {
  background: var(--bg-elevated);
  border: none;
  color: var(--text-tertiary);
  padding: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  transition: all var(--transition);
  flex-shrink: 0;
  width: 40px;
  height: 40px;
}

.send-btn:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.send-btn.active {
  background: var(--accent-primary);
  color: white;
}

.send-btn.active:hover:not(:disabled) {
  background: var(--accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.send-btn.active:active {
  transform: translateY(0);
}

.char-count {
  font-size: 11px;
  color: var(--text-tertiary);
  text-align: right;
  padding: 0 4px;
}

.char-count.warning {
  color: var(--warning);
}

/* Mobile Optimizations */
@media (max-width: 768px) {
  .input-wrapper {
    gap: 8px;
    padding: 6px 10px;
  }

  .message-input {
    font-size: 16px; /* Prevents zoom on iOS */
  }

  .attach-btn, .send-btn {
    width: 36px;
    height: 36px;
    padding: 8px;
  }

  .attach-btn svg, .send-btn svg {
    width: 18px;
    height: 18px;
  }

  .file-chip {
    padding: 6px 10px;
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .file-previews {
    gap: 6px;
  }

  .file-chip {
    max-width: 160px;
  }

  .input-wrapper {
    border-radius: var(--radius-md);
  }
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  * {
    transition: none !important;
    animation: none !important;
  }
}
</style>