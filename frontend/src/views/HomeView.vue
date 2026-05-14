<template>
  <div class="home-page">
    <!-- Animated background canvas (decorative) -->
    <div class="bg-canvas" aria-hidden="true">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
    </div>

    <div class="home-body">

      <!-- Hero logo -->
      <div class="hero">
        <img class="hero-logo" :src="naviIcon" alt="Data Navi" />
      </div>

      <!-- Title -->
      <div class="home-header">
        <h1 class="home-title">Data Navi</h1>
        <p class="home-subtitle">DataNavi is a multi-agent conversational agent you can ask any question on SBF data. Think of it like a <strong class="subtitle-highlight">ChatGPT for internal data</strong>.</p>
      </div>

      <!-- Loading state -->
      <div v-if="store.loading" class="state-view">
        <div class="spinner" />
        <p class="state-text">Loading…</p>
      </div>

      <!-- Error state -->
      <div v-else-if="store.error" class="state-view">
        <svg class="state-icon error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="8" x2="12" y2="12"/>
          <line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        <p class="state-text">{{ store.error }}</p>
      </div>

      <!-- Content -->
      <template v-else>
        <div v-if="store.spaces.length" class="space-grid">
          <SpaceCard
            v-for="space in store.spaces"
            :key="space.code"
            :space="space"
            @select="onSelectSpace"
          />
        </div>
        <div v-else class="state-view">
          <p class="state-text">No spaces configured.</p>
        </div>
      </template>

    </div>

    <!-- Bottom disclaimer -->
    <footer class="disclaimer">
      Always review the accuracy of responses.
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'
import { store } from '../store.js'
import SpaceCard from '../components/SpaceCard.vue'
import naviIcon  from '../../icon/navi.svg'

const router = useRouter()

onMounted(async () => {
  if (store.spaces.length) {
    store.loading = false
    return
  }
  store.loading = true
  store.error   = null
  try {
    const res = await fetch('/api/all')
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    store.spaces = await res.json()
  } catch (e) {
    store.error = `Failed to load data: ${e.message}`
  } finally {
    store.loading = false
  }
})

function onSelectSpace(space) {
  router.push({ name: 'genie', params: { space: space.code } })
}
</script>

<style scoped>
/* ── Page shell ── */
.home-page {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 50%, #f0f9ff 100%);
  overflow: hidden;
  position: relative;
}

/* ── Floating orb layer ── */
.bg-canvas {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}
.orb { position: absolute; border-radius: 50%; filter: blur(70px); }
.orb-1 {
  width: 380px; height: 380px;
  background: radial-gradient(circle, rgba(91, 194, 220, 0.25), transparent 70%);
  top: -100px; left: -100px;
  animation: floatA 13s ease-in-out infinite;
}
.orb-2 {
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.18), transparent 70%);
  bottom: -60px; right: -60px;
  animation: floatB 17s ease-in-out infinite;
}
.orb-3 {
  width: 220px; height: 220px;
  background: radial-gradient(circle, rgba(14, 165, 233, 0.18), transparent 70%);
  top: 45%; left: 55%;
  animation: floatA 20s ease-in-out infinite 5s;
}

@keyframes floatA {
  0%, 100% { transform: translate(0, 0); }
  33%      { transform: translate(28px, -22px); }
  66%      { transform: translate(-18px, 32px); }
}
@keyframes floatB {
  0%, 100% { transform: translate(0, 0); }
  33%      { transform: translate(-30px, 20px); }
  66%      { transform: translate(22px, -28px); }
}
@media (prefers-reduced-motion: reduce) {
  .orb { animation: none; }
}

/* ── Scrollable body ── */
.home-body {
  flex: 1;
  overflow-y: auto;
  padding: 48px 52px 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  position: relative;
  z-index: 1;
}

/* ── Hero logo ── */
.hero { display: flex; justify-content: center; }
.hero-logo {
  width: 120px;
  height: 120px;
  object-fit: contain;
  border-radius: 20px;
}

/* ── Title ── */
.home-header { text-align: center; max-width: 720px; }
.home-title {
  font-size: clamp(28px, 4vw, 36px);
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: -0.02em;
  margin: 0 0 8px;
}
.home-subtitle {
  font-size: 16px;
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin: 0;
}
.subtitle-highlight { color: var(--color-text-primary); font-weight: 700; }

/* ── Space cards ── */
.space-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  width: 100%;
  max-width: 1100px;
}

/* ── State views ── */
.state-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 40px 0;
}
.state-text  { font-size: 13px; color: var(--color-text-tertiary); }
.state-icon  { width: 32px; height: 32px; }
.error-icon  { color: var(--color-error); }

/* ── Spinner ── */
.spinner {
  width: 20px; height: 20px;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) { .spinner { animation: none; } }

/* ── Bottom disclaimer ── */
.disclaimer {
  flex-shrink: 0;
  text-align: center;
  padding: 10px 0 14px;
  font-size: 12px;
  color: var(--color-text-secondary);
  border-top: 1px solid var(--color-border);
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  position: relative;
  z-index: 1;
}
</style>
