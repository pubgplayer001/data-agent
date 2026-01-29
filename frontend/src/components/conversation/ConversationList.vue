<template>
  <div class="d-flex flex-column h-100">
    <div class="p-2">
      <input
        v-model="filter"
        class="form-control form-control-sm"
        placeholder="Search conversations..."
        aria-label="Search conversations"
      />
    </div>

    <ul class="list-group list-group-flush overflow-auto flex-fill">
      <li
        v-for="conv in filtered"
        :key="conv.id"
        :class="['list-group-item list-group-item-action d-flex align-items-start', conv.id === active?.id ? 'active' : '']"
        @click="$emit('select', conv)"
        style="cursor: pointer;"
      >
        <div class="me-2">
          <div
            class="rounded bg-secondary text-white d-flex align-items-center justify-content-center"
            style="width:44px;height:44px;font-weight:700;"
          >
            {{ (conv.title || 'C').charAt(0).toUpperCase() }}
          </div>
        </div>

        <div class="flex-fill">
          <div class="d-flex justify-content-between">
            <div class="fw-semibold text-truncate" style="max-width: 60%;">{{ conv.title || 'Untitled' }}</div>
            <small class="text-muted ms-2">{{ conv.updatedAt ? formatTime(conv.updatedAt) : '' }}</small>
          </div>
          <div class="text-muted small text-truncate">{{ conv.lastText || '' }}</div>
        </div>
      </li>
      <li v-if="filtered.length === 0" class="list-group-item text-center text-muted">No conversations</li>
    </ul>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

defineProps(['conversations', 'active'])

const filter = ref('')
const filtered = computed(() => {
  const arr = Array.isArray(__props.conversations) ? __props.conversations : []
  if (!filter.value) return arr
  const q = filter.value.toLowerCase()
  return arr.filter(
    (c) => (c.title || '').toLowerCase().includes(q) || (c.lastText || '').toLowerCase().includes(q)
  )
})

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
.list-group-item.active {
  background: linear-gradient(90deg, rgba(79, 70, 229, 0.15), rgba(6, 182, 212, 0.06));
  color: #fff;
  border-left: 4px solid rgba(84, 105, 212, 0.9);
}
</style>