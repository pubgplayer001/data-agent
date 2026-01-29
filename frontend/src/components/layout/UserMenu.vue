<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import logo from '@/assets/logo.svg'

const open = ref(false)
const router = useRouter()

let user = null
try {
  const raw = localStorage.getItem('user')
  user = raw ? JSON.parse(raw) : null
} catch (e) {
  user = null
}

const container = ref(null)

const toggle = () => {
  open.value = !open.value
}

const logout = () => {
  localStorage.clear()
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

<template>
  <div ref="container" class="user-menu" @keydown.escape="open = false">
    <button
      class="avatar-btn"
      @click="toggle"
      :aria-expanded="open"
      aria-haspopup="true"
    >
      <img
        v-if="user?.avatarUrl"
        :src="user.avatarUrl"
        alt="User avatar"
        class="user-avatar"
      />
      <img v-else :src="logo" alt="Logo" class="user-avatar" />

      <div class="user-info">
        <span class="user-name">{{ user?.name || 'Guest' }}</span>
        <small class="user-email" v-if="user?.email">{{ user.email }}</small>
      </div>

      <span class="chev" :class="{ open: open }" aria-hidden="true">▾</span>
    </button>

    <transition name="fade">
      <div v-if="open" class="dropdown" role="menu">
        <div class="profile">
          <p class="name">{{ user?.name || 'Guest User' }}</p>
          <p class="email" v-if="user?.email">{{ user.email }}</p>
        </div>

        <div class="actions">
          <button class="btn logout" @click="logout">Logout</button>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.user-menu {
  position: relative;
  display: flex;
  align-items: center;
  padding: 8px 12px;
  gap: 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.04);
}

/* Avatar button */
.avatar-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  background: transparent;
  border: none;
  padding: 6px 8px;
  border-radius: 8px;
  cursor: pointer;
  color: #e6e6e6;
  transition: background 150ms ease;
}
.avatar-btn:focus {
  outline: 2px solid rgba(84, 105, 212, 0.25);
  outline-offset: 2px;
  background: rgba(255,255,255,0.02);
}

/* Avatar image */
.user-avatar {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.05);
  background: #111;
}

/* Name and email in compact view */
.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  line-height: 1;
}
.user-name {
  font-weight: 600;
  font-size: 14px;
  color: #fff;
}
.user-email {
  font-size: 12px;
  color: #bcbcbc;
}

/* Chevron */
.chev {
  margin-left: 8px;
  font-size: 14px;
  color: #cfcfcf;
  transform-origin: center;
  transition: transform 150ms ease;
}
.chev.open {
  transform: rotate(180deg);
}

/* Dropdown */
.dropdown {
  position: absolute;
  right: 8px;
  top: calc(100% + 8px);
  min-width: 200px;
  background: linear-gradient(180deg, rgba(25,25,25,0.98), rgba(20,20,20,0.98));
  border-radius: 10px;
  padding: 12px;
  box-shadow: 0 6px 24px rgba(0,0,0,0.6);
  border: 1px solid rgba(255,255,255,0.03);
  z-index: 50;
  color: #eaeaea;
}

/* Profile block inside dropdown */
.profile .name {
  margin: 0;
  font-weight: 700;
  font-size: 15px;
}
.profile .email {
  margin: 4px 0 8px;
  font-size: 13px;
  color: #bdbdbd;
}

/* Actions */
.actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}
.btn {
  padding: 8px 12px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
}
.btn.logout {
  background: #ef4444;
  color: white;
  transition: transform 90ms ease, filter 90ms ease;
}
.btn.logout:hover {
  filter: brightness(0.95);
  transform: translateY(-1px);
}

/* Transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 160ms ease, transform 160ms ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

/* Responsive tweaks */
@media (max-width: 520px) {
  .user-info { display: none; }
  .dropdown { right: 6px; left: 6px; min-width: unset; }
}
</style>