<template>
  <div class="conversation-list">
    <!-- Search Bar -->
    <div class="search-container">
      <div class="search-wrapper">
        <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input
          v-model="filter"
          class="search-input"
          placeholder="Search conversations..."
          aria-label="Search conversations"
        />
        <button 
          v-if="filter" 
          class="clear-btn" 
          @click="filter = ''"
          aria-label="Clear search"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
    </div>

    <!-- Conversations -->
    <div class="conversations">
      <div
        v-for="(conv, index) in filtered"
        :key="conv.id"
        :class="['conversation-item', { active: conv.id === active?.id }]"
        @click="$emit('select', conv)"
        :style="{ animationDelay: `${index * 50}ms` }"
      >
        <div class="conversation-avatar">
          {{ getInitial(conv.title) }}
        </div>
        <div class="conversation-content">
          <div class="conversation-header">
            <div class="conversation-title">{{ conv.title || 'Untitled' }}</div>
            <div class="conversation-time">{{ formatTime(conv.updatedAt) }}</div>
          </div>
          <div class="conversation-preview">{{ conv.lastText || 'No messages yet' }}</div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filtered.length === 0" class="empty-state">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <p>{{ filter ? 'No conversations found' : 'No conversations yet' }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  conversations: Array,
  active: Object
})

const filter = ref('')

const filtered = computed(() => {
  const arr = Array.isArray(props.conversations) ? props.conversations : []
  if (!filter.value) return arr
  const q = filter.value.toLowerCase()
  return arr.filter(
    (c) => (c.title || '').toLowerCase().includes(q) || (c.lastText || '').toLowerCase().includes(q)
  )
})

const getInitial = (title) => {
  return (title || 'C').charAt(0).toUpperCase()
}

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const now = Date.now()
  const diff = now - timestamp
  
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  
  if (seconds < 60) return 'Just now'
  if (minutes < 60) return `${minutes}m ago`
  if (hours < 24) return `${hours}h ago`
  if (days < 7) return `${days}d ago`
  
  const date = new Date(timestamp)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}
</script>

<style scoped>
.conversation-list {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.search-container {
  padding: 12px 16px;
}

.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 12px;
  color: var(--text-tertiary);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 10px 36px 10px 36px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-size: 14px;
  transition: all var(--transition);
}

.search-input:focus {
  outline: none;
  border-color: var(--accent-primary);
  background: var(--bg-elevated);
}

.search-input::placeholder {
  color: var(--text-tertiary);
}

.clear-btn {
  position: absolute;
  right: 8px;
  background: none;
  border: none;
  color: var(--text-tertiary);
  padding: 6px;
  cursor: pointer;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition);
}

.clear-btn:hover {
  background: var(--bg-hover);
  color: var(--text-secondary);
}

.conversations {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 0 12px 12px;
}

.conversation-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition);
  margin-bottom: 4px;
  animation: slideIn 0.3s ease both;
  position: relative;
}

.conversation-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 0;
  background: var(--accent-primary);
  border-radius: 0 2px 2px 0;
  transition: height var(--transition);
}

.conversation-item:hover {
  background: var(--bg-hover);
}

.conversation-item.active {
  background: var(--accent-light);
}

.conversation-item.active::before {
  height: 70%;
}

.conversation-avatar {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-hover));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
}

.conversation-content {
  flex: 1;
  min-width: 0;
}

.conversation-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
  gap: 8px;
}

.conversation-title {
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.conversation-time {
  font-size: 11px;
  color: var(--text-tertiary);
  white-space: nowrap;
  flex-shrink: 0;
}

.conversation-preview {
  font-size: 13px;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.conversation-item.active .conversation-title {
  color: var(--accent-primary);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  text-align: center;
  color: var(--text-tertiary);
}

.empty-state svg {
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state p {
  font-size: 14px;
}

/* Mobile Optimizations */
@media (max-width: 768px) {
  .conversation-item {
    padding: 14px 12px;
    margin-bottom: 6px;
  }

  .conversation-avatar {
    width: 44px;
    height: 44px;
    font-size: 18px;
  }

  .conversation-title {
    font-size: 15px;
  }

  .conversation-preview {
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .search-input {
    font-size: 16px; /* Prevents zoom on iOS */
  }

  .conversation-item {
    padding: 12px;
  }
}
</style>