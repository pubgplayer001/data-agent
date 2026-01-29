<template>
  <form @submit.prevent="onSubmit" class="d-flex flex-column">
    <div class="d-flex gap-2 align-items-end">
      <textarea
        v-model="text"
        ref="ta"
        rows="1"
        class="form-control"
        :placeholder="placeholder"
        style="resize: none; min-height: 48px; max-height: 220px;"
      ></textarea>

      <div class="d-flex flex-column gap-2">
        <label class="btn btn-outline-secondary btn-sm mb-1" :title="files.length ? filesLabel : 'Attach file'">
          <i class="bi bi-paperclip"></i>
          <input type="file" @change="onFileChange" multiple style="display:none" />
        </label>

        <button type="submit" class="btn btn-primary btn-sm" :disabled="!canSend">
          <i class="bi bi-send"></i> Send
        </button>
      </div>
    </div>

    <div v-if="files.length" class="mt-2 d-flex flex-wrap gap-2">
      <div v-for="(f, i) in files" :key="i" class="badge bg-light text-dark d-inline-flex align-items-center gap-2">
        <span class="small">{{ f.name }}</span>
        <button type="button" class="btn-close btn-close-white ms-2" aria-label="Remove" @click="removeFile(i)"></button>
      </div>
    </div>
  </form>
</template>

<script setup>
import { ref, watch, nextTick, computed } from 'vue'

const emit = defineEmits(['send'])
const placeholder = 'Type a message — press Enter to send, Shift+Enter for newline'

const text = ref('')
const files = ref([])

const ta = ref(null)

const canSend = computed(() => text.value.trim().length > 0 || files.value.length > 0)

const filesLabel = computed(() => files.value.map(f => f.name).join(', '))

const onFileChange = (e) => {
  const list = Array.from(e.target.files || [])
  if (list.length) files.value = files.value.concat(list)
  e.target.value = ''
  nextTick(() => ta.value && ta.value.focus())
}

const removeFile = (idx) => {
  files.value.splice(idx, 1)
}

const onSubmit = () => {
  if (!canSend.value) return
  emit('send', text.value.trim(), files.value.length ? [...files.value] : [])
  text.value = ''
  files.value = []
  nextTick(() => {
    if (ta.value) {
      ta.value.style.height = 'auto'
      ta.value.focus()
    }
  })
}

const onKeydown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    onSubmit()
  }
}

watch(text, () => {
  nextTick(() => {
    if (!ta.value) return
    ta.value.style.height = 'auto'
    ta.value.style.height = Math.min(220, ta.value.scrollHeight) + 'px'
  })
})
</script>

<style scoped>
/* minimal component scoped styles; Bootstrap handles layout */
</style>
