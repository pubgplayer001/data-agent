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

const toggle = () => (open.value = !open.value)
const logout = () => {
  localStorage.clear()
  router.push('/login')
}

const container = ref(null)
const onClickOutside = (e) => {
  if (!container.value) return
  if (!container.value.contains(e.target)) open.value = false
}

onMounted(() => document.addEventListener('click', onClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', onClickOutside))
</script>

<template>
  <div ref="container" class="dropdown w-100">
    <button
      class="btn btn-sm btn-outline-light dropdown-toggle w-100 d-flex align-items-center gap-2"
      type="button"
      @click="toggle"
    >
      <img
        :src="user?.avatarUrl || logo"
        alt="avatar"
        style="width:28px;height:28px;border-radius:6px"
      />
      <div class="text-start flex-fill" v-if="user">
        <div class="fw-semibold small mb-0">{{ user.name }}</div>
        <div class="small text-muted">{{ user.email }}</div>
      </div>
      <div v-else class="text-start flex-fill small">Guest</div>
    </button>

    <ul v-if="open" class="dropdown-menu show w-100 mt-1 p-2">
      <li class="px-2 py-1">
        <div class="fw-bold">{{ user?.name || 'Guest User' }}</div>
        <div class="text-muted small">{{ user?.email || '' }}</div>
      </li>
      <li><hr class="dropdown-divider"></li>
      <li class="px-2">
        <button class="btn btn-sm btn-danger w-100" @click="logout">
          <i class="bi bi-box-arrow-right"></i> Logout
        </button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
/* minimal; relies on Bootstrap */
</style>