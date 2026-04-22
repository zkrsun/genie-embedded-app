<template>
  <iframe
    v-if="spaceUrl"
    :key="spaceUrl"
    :src="spaceUrl"
    allow="clipboard-write"
    sandbox="allow-scripts allow-same-origin allow-forms allow-downloads allow-modals allow-pointer-lock allow-presentation allow-storage-access-by-user-activation"
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
  if (!store.buList.length) {
    try {
      const res = await fetch('/api/all')
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      store.buList = await res.json()
    } catch {
      router.replace({ name: 'home' })
      return
    }
  }

  const { bu, domain, space: spaceCode } = route.params
  const buObj     = store.buList.find(b => b.name === bu)
  const domainObj = buObj?.domains.find(d => d.name === domain)
  const spaceObj  = domainObj?.spaces.find(s => s.code === spaceCode)

  if (!spaceObj) {
    router.replace({ name: 'home' })
    return
  }

  spaceUrl.value = spaceObj.url
  setActiveSpace({ ...spaceObj, bu, domain })
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
