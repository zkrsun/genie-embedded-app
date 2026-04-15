<template>
  <div class="layout">
    <header class="navbar">
      <div class="navbar-brand">
        <img class="brand-icon" :src="naviIcon" alt="Genie icon" />
      </div>

      <nav class="navbar-tabs" role="navigation" aria-label="Genie spaces">
        <button
          v-for="space in spaces"
          :key="space.name"
          class="tab"
          :class="{ active: activeSpace?.name === space.name }"
          :aria-current="activeSpace?.name === space.name ? 'page' : undefined"
          @click="activeSpace = space"
        >
          {{ space.name }}
        </button>
      </nav>
    </header>

    <main class="content">
      <iframe
        v-if="activeSpace"
        :key="activeSpace.name"
        :src="activeSpace.url"
        allow="clipboard-write"
        class="genie-frame"
        title="Genie Space"
      />
      <div v-else-if="error" class="state-view">
        <svg class="state-icon error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        <p class="state-text">{{ error }}</p>
      </div>
      <div v-else class="state-view">
        <div class="spinner"></div>
        <p class="state-text">Loading spaces…</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import naviIcon from '../icon/navi.svg'

const spaces      = ref([])
const activeSpace = ref(null)
const error       = ref(null)

onMounted(async () => {
  try {
    const res = await fetch('/api/spaces')
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    spaces.value = await res.json()
    activeSpace.value = spaces.value[0] ?? null
    if (!activeSpace.value) error.value = 'No spaces configured. Check GENIE_SPACE_* env vars in app.yaml.'
  } catch (e) {
    error.value = `Failed to load spaces: ${e.message}`
  }
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: #f8fafc;
  color: #1e293b;
  -webkit-font-smoothing: antialiased;
}

.layout { display: flex; flex-direction: column; height: 100vh; }

/* ── Navbar ── */
.navbar {
  display: flex;
  align-items: center;
  padding: 0 24px;
  height: 52px;
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  flex-shrink: 0;
  gap: 16px;
}

.navbar-brand { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }

.brand-icon {
  display: block;
  width: 28px; height: 28px;
  border-radius: 7px;
  object-fit: contain;
}

.brand-name { font-size: 15px; font-weight: 600; color: #0f172a; letter-spacing: -0.01em; }

/* ── Tabs ── */
.navbar-tabs { display: flex; align-items: stretch; height: 100%; gap: 2px; }

.tab {
  position: relative; display: flex; align-items: center;
  padding: 0 16px; height: 100%;
  border: none; background: transparent;
  color: #64748b; font-family: inherit; font-size: 13px; font-weight: 500;
  cursor: pointer; white-space: nowrap;
  transition: color 0.15s;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
}
.tab:hover         { color: #1e293b; }
.tab.active        { color: #2563eb; border-bottom-color: #2563eb; font-weight: 600; }
.tab:focus-visible { outline: 2px solid #2563eb; outline-offset: -2px; border-radius: 3px; }

/* ── Content ── */
.content { flex: 1; overflow: hidden; background: #ffffff; }

.genie-frame { width: 100%; height: 100%; border: none; display: block; }

/* ── State views ── */
.state-view {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 12px; height: 100%; background: #f8fafc;
}
.state-text { font-size: 13px; color: #94a3b8; }
.state-icon { width: 32px; height: 32px; }
.error-icon { color: #f87171; }

/* ── Spinner ── */
.spinner {
  width: 22px; height: 22px;
  border: 2px solid #e2e8f0; border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) { .spinner { animation: none; } }
</style>
