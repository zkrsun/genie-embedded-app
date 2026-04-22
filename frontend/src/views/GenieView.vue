<template>
  <iframe
    :key="store.activeSpace?.url"
    :src="store.activeSpace?.url"
    allow="clipboard-write"
    sandbox="allow-scripts allow-same-origin allow-forms allow-downloads allow-modals allow-pointer-lock allow-presentation allow-storage-access-by-user-activation"
    class="genie-frame"
    title="Genie Space"
  />
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { store } from '../store.js'

const router = useRouter()

onMounted(() => {
  console.log('[GenieView] activeSpace =', JSON.stringify(store.activeSpace))
  if (!store.activeSpace?.url) {
    console.warn('[GenieView] No active space URL — redirecting to home')
    router.replace({ name: 'home' })
  }
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
</style>
