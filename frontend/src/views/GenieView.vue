<template>
  <iframe
    v-if="spaceUrl"
    :key="spaceUrl"
    :src="spaceUrl"
    allow="clipboard-write"
    sandbox="allow-scripts allow-same-origin allow-forms allow-downloads allow-modals allow-pointer-lock allow-presentation allow-storage-access-by-user-activation allow-popups allow-popups-to-escape-sandbox"
    class="genie-frame"
    title="Genie Space"
  />
  <div v-else class="loading-view">
    <div class="spinner" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { store, setActiveSpace } from '../store.js'

const route    = useRoute()
const router   = useRouter()
const spaceUrl = ref(null)

onMounted(async () => {
  if (!store.spaces.length) {
    try {
      const res = await fetch('/api/all')
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      store.spaces = await res.json()
    } catch {
      router.replace({ name: 'home' })
      return
    }
  }

  const spaceObj = store.spaces.find(s => s.code === route.params.space)
  if (!spaceObj) {
    router.replace({ name: 'home' })
    return
  }

  spaceUrl.value = spaceObj.url
  setActiveSpace(spaceObj)

  fetch('/api/log/space-access', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ space_code: spaceObj.code }),
    keepalive: true,
  }).catch(() => {})
})
</script>

<style scoped>
.genie-frame {
  display: block;
  width: 100%;
  height: 100%;
  border: none;
  background: #ffffff;
}
.loading-view {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}
.spinner {
  width: 20px; height: 20px;
  border: 2px solid #d8d3cb; border-top-color: #1b6feb;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
