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
} catch {
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
  <div ref="container" class="w-100">
    <div class="d-flex align-items-center gap-2">
      <button
        class="btn btn-sm btn-outline-light d-flex align-items-center gap-2 w-100"
        type="button"
        @click="toggle"
        :aria-expanded="open"
        aria-haspopup="true"
      >
        <img :src="user?.avatarUrl || logo" alt="avatar" class="rounded" style="width:36px;height:36px;object-fit:cover" />
        <div class="text-start flex-fill" v-if="user && !$attrs.class?.includes('collapsed')">
          <div class="fw-semibold small mb-0">{{ user.name }}</div>
          <div class="small text-muted">{{ user.email }}</div>
        </div>
        <div v-else class="text-start flex-fill small">Guest</div>
      </button>
    </div>

    <div v-if="open" class="card mt-2 w-100 shadow-sm">
      <div class="card-body p-2">
        <div class="fw-bold">{{ user?.name || 'Guest User' }}</div>
        <div class="text-muted small mb-2">{{ user?.email || '' }}</div>
        <div class="d-grid">
          <button class="btn btn-sm btn-danger" @click="logout">
            <i class="bi bi-box-arrow-right"></i> Logout
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.03); }
</style>