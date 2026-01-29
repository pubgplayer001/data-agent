<template>
  <div ref="container" class="user-menu">
    <button
      class="user-button"
      type="button"
      @click="toggle"
      :aria-expanded="open"
      aria-haspopup="true"
    >
      <div class="user-avatar">
        <img
          v-if="user?.avatarUrl"
          :src="user.avatarUrl"
          :alt="user.name"
          class="avatar-image"
        />
        <div v-else class="avatar-placeholder">
          {{ getInitials(user?.name) }}
        </div>
      </div>
      <div class="user-info">
        <div class="user-name">{{ user?.name || 'Guest User' }}</div>
        <div class="user-email">{{ user?.email || 'Not logged in' }}</div>
      </div>
      <svg
        class="chevron"
        :class="{ open }"
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <polyline points="6 9 12 15 18 9"></polyline>
      </svg>
    </button>

    <!-- Dropdown Menu -->
    <transition name="dropdown">
      <div v-if="open" class="dropdown-menu">
        <div class="menu-header">
          <div class="menu-user-info">
            <div class="menu-user-name">{{ user?.name || 'Guest User' }}</div>
            <div class="menu-user-email">{{ user?.email || '' }}</div>
          </div>
        </div>

        <div class="menu-divider"></div>

        <div class="menu-items">
          <button class="menu-item" @click="handleProfile">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <span>Profile</span>
          </button>

          <button class="menu-item" @click="handleSettings">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M12 1v6m0 6v6M5.64 5.64l4.24 4.24m4.24 4.24l4.24 4.24M1 12h6m6 0h6M5.64 18.36l4.24-4.24m4.24-4.24l4.24-4.24"></path>
            </svg>
            <span>Settings</span>
          </button>

          <button class="menu-item" @click="handleHelp">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
            <span>Help & Support</span>
          </button>
        </div>

        <div class="menu-divider"></div>

        <div class="menu-items">
          <button class="menu-item danger" @click="logout">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
              <polyline points="16 17 21 12 16 7"></polyline>
              <line x1="21" y1="12" x2="9" y2="12"></line>
            </svg>
            <span>Logout</span>
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'

const open = ref(false)
const container = ref(null)
const router = useRouter()

let user = null
try {
  const raw = localStorage.getItem('user')
  user = raw ? JSON.parse(raw) : null
} catch {
  user = null
}

const toggle = () => {
  open.value = !open.value
}

const getInitials = (name) => {
  if (!name) return 'G'
  const parts = name.split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return name.substring(0, 2).toUpperCase()
}

const handleProfile = () => {
  open.value = false
  // Navigate to profile
  console.log('Navigate to profile')
}

const handleSettings = () => {
  open.value = false
  // Navigate to settings
  console.log('Navigate to settings')
}

const handleHelp = () => {
  open.value = false
  // Open help
  console.log('Open help')
}

const logout = () => {
  localStorage.clear()
  open.value = false
  router.push('/login')
}

const onClickOutside = (e) => {
  if (!container.value) return
  if (!container.value.contains(e.target)) {
    open.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', onClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', onClickOutside)
})
</script>

<style scoped>
.user-menu {
  position: relative;
  width: 100%;
}

.user-button {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition);
}

.user-button:hover {
  background: var(--bg-hover);
  border-color: var(--border-medium);
}

.user-avatar {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
}

.avatar-image {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-hover));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
}

.user-info {
  flex: 1;
  min-width: 0;
  text-align: left;
}

.user-name {
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-email {
  font-size: 12px;
  color: var(--text-tertiary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chevron {
  color: var(--text-tertiary);
  transition: transform var(--transition);
  flex-shrink: 0;
}

.chevron.open {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  bottom: 100%;
  left: 0;
  right: 0;
  margin-bottom: 8px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-medium);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  z-index: 100;
}

.menu-header {
  padding: 16px;
  background: var(--bg-tertiary);
  border-bottom: 1px solid var(--border-subtle);
}

.menu-user-name {
  font-weight: 600;
  font-size: 15px;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.menu-user-email {
  font-size: 13px;
  color: var(--text-secondary);
}

.menu-divider {
  height: 1px;
  background: var(--border-subtle);
  margin: 0;
}

.menu-items {
  padding: 8px;
}

.menu-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  background: none;
  border: none;
  color: var(--text-primary);
  font-size: 14px;
  cursor: pointer;
  border-radius: var(--radius-sm);
  transition: all var(--transition);
  text-align: left;
}

.menu-item:hover {
  background: var(--bg-hover);
}

.menu-item svg {
  color: var(--text-secondary);
  flex-shrink: 0;
}

.menu-item.danger {
  color: var(--danger);
}

.menu-item.danger svg {
  color: var(--danger);
}

.menu-item.danger:hover {
  background: rgba(239, 68, 68, 0.1);
}

/* Dropdown Animation */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all var(--transition);
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

.dropdown-enter-to,
.dropdown-leave-from {
  opacity: 1;
  transform: translateY(0);
}

/* Mobile */
@media (max-width: 768px) {
  .dropdown-menu {
    position: fixed;
    bottom: auto;
    top: auto;
    left: 50%;
    transform: translateX(-50%);
    width: calc(100vw - 32px);
    max-width: 360px;
    margin: 0;
  }

  .user-button {
    padding: 10px;
  }

  .user-avatar {
    width: 36px;
    height: 36px;
  }

  .user-name {
    font-size: 13px;
  }

  .user-email {
    font-size: 11px;
  }
}

@media (max-width: 480px) {
  .user-info {
    display: none;
  }

  .user-button {
    justify-content: center;
  }

  .chevron {
    display: none;
  }

  .dropdown-menu {
    width: calc(100vw - 24px);
  }
}
</style>