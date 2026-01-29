<template>
  <form @submit.prevent="send">
    <input v-model="text" placeholder="Type..." />
    <input type="file" />
    <button>Send</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
const emit = defineEmits(['send'])

const text = ref('')

const send = () => {
  if (!text.value) return
  emit('send', text.value)
  text.value = ''
}
</script>
