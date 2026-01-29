<template>
  <div class="conversation-list">
    <div class="search" v-if="conversations && conversations.length">
      <input
        v-model="filter"
        placeholder="Search conversations..."
        aria-label="Search conversations"
      />
    </div>

    <ul class="list" v-if="conversations && conversations.length">
      <li
        v-for="conv in filtered"
        :key="conv.id"
        :class="{ active: conv.id === active?.id }"
        @click="$emit('select', conv)"
      >
        <div class="item-left">
          <div class="avatar">{{ (conv.title || 'C').charAt(0).toUpperCase() }}</div>
        </div>
        <div class="item-body">
          <div class="title">{{ conv.title || 'Untitled' }}</div>
          <div class="meta">{{ conv.lastText || '' }}</div>
        </div>
        <div class="item-right">
          <small class="time">{{ conv.updatedAt ? formatTime(conv.updatedAt) : '' }}</small>
        </div>
      </li>
    </ul>

    <div v-else class="empty">No conversations yet</div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

defineProps(['conversations', 'active'])

const filter = ref('')
const filtered = computed(() => {
  if (!filter.value) return (Array.isArray(__props.conversations) ? __props.conversations : [])
  const q = filter.value.toLowerCase()
  return (Array.isArray(__props.conversations) ? __props.conversations : []).filter(
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
.conversation-list {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
}

.search {
  padding: 10px 12px;
  border-bottom: 1px solid rgba(255,255,255,0.02);
}
.search input {
  width: 100%;
  padding: 8px 10px;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.04);
  background: rgba(255,255,255,0.02);
  color: #eaf2ff;
}
.search input::placeholder {
  color: rgba(230,238,248,0.5);
}

/* list scroll area */
.list {
  list-style: none;
  margin: 0;
  padding: 8px;
  overflow-y: auto;
  height: calc(100% - 56px);
}

li {
  display: flex;
  gap: 10px;
  align-items: center;
  padding: 10px;
  cursor: pointer;
  border-radius: 8px;
  transition: background 120ms ease, transform 80ms ease;
}
li:hover {
  background: rgba(255,255,255,0.02);
  transform: translateY(-1px);
}
li.active {
  background: linear-gradient(90deg, rgba(64,75,125,0.12), rgba(64,75,125,0.06));
  border-left: 3px solid rgba(84,105,212,0.9);
}

/* avatar */
.avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg,#243b55,#141e30);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  font-weight: 700;
  color: #fff;
}

/* item text */
.item-body {
  flex: 1;
  min-width: 0;
}
.title {
  font-weight: 600;
  font-size: 14px;
  color: #f4f7fb;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.meta {
  font-size: 12px;
  color: rgba(235,242,255,0.6);
  margin-top: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* right area */
.item-right {
  margin-left: 8px;
  text-align: right;
}
.time {
  color: rgba(235,242,255,0.5);
  font-size: 11px;
}

/* empty state */
.empty {
  padding: 18px;
  color: rgba(235,242,255,0.6);
  text-align: center;
}
</style>