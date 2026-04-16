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
        <h1 class="home-title">Data Download</h1>
        <p class="home-subtitle">Select a Business Unit and Genie Space to start your analysis</p>
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
        <BuFilter :bu-list="buNames" v-model="activeBu" />

        <div v-if="currentSpaces.length" class="space-grid">
          <SpaceCard
            v-for="space in currentSpaces"
            :key="space.name"
            :space="space"
            :bu="activeBu"
            @select="onSelectSpace"
          />
        </div>
        <div v-else class="state-view">
          <p class="state-text">No spaces configured for {{ activeBu }}.</p>
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { store } from '../store.js'
import BuFilter  from '../components/BuFilter.vue'
import SpaceCard from '../components/SpaceCard.vue'
import naviIcon  from '../../icon/navi.svg'

const router   = useRouter()
const activeBu = ref(null)

const buNames = computed(() => store.buList.map(b => b.bu))

const currentSpaces = computed(() => {
  const entry = store.buList.find(b => b.bu === activeBu.value)
  return entry?.spaces ?? []
})

onMounted(async () => {
  // Only fetch once; subsequent visits to HomeView reuse cached data
  if (store.buList.length) {
    activeBu.value = store.buList[0].bu
    return
  }
  store.loading = true
  store.error   = null
  try {
    const res = await fetch('/api/all')
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    store.buList = await res.json()
    activeBu.value = store.buList[0]?.bu ?? null
  } catch (e) {
    store.error = `Failed to load data: ${e.message}`
  } finally {
    store.loading = false
  }
})

function onSelectSpace(space) {
  store.activeSpace = { ...space, bu: activeBu.value }
  router.push({ name: 'genie' })
}
</script>

<style scoped>
/* ── Page shell ── */
.home-page {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: linear-gradient(135deg, #efebe4 0%, #e4ddd4 40%, #eae3f0 75%, #e0eae8 100%);
  background-size: 300% 300%;
  animation: bgDrift 14s ease infinite;
  overflow: hidden;
  position: relative;
}

/* ── Animated gradient drift ── */
@keyframes bgDrift {
  0%   { background-position: 0%   0%;   }
  25%  { background-position: 100% 0%;   }
  50%  { background-position: 100% 100%; }
  75%  { background-position: 0%   100%; }
  100% { background-position: 0%   0%;   }
}

/* ── Floating orb layer ── */
.bg-canvas {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(70px);
}

.orb-1 {
  width: 380px; height: 380px;
  background: radial-gradient(circle, rgba(100, 160, 245, 0.22), transparent 70%);
  top: -100px; left: -100px;
  animation: floatA 13s ease-in-out infinite;
}

.orb-2 {
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(220, 160, 200, 0.2), transparent 70%);
  bottom: -60px; right: -60px;
  animation: floatB 17s ease-in-out infinite;
}

.orb-3 {
  width: 220px; height: 220px;
  background: radial-gradient(circle, rgba(120, 210, 190, 0.18), transparent 70%);
  top: 45%; left: 55%;
  animation: floatA 20s ease-in-out infinite 5s;
}

@keyframes floatA {
  0%, 100% { transform: translate(0,   0);    }
  33%       { transform: translate(28px, -22px); }
  66%       { transform: translate(-18px, 32px); }
}

@keyframes floatB {
  0%, 100% { transform: translate(0,   0);    }
  33%       { transform: translate(-30px, 20px); }
  66%       { transform: translate(22px, -28px); }
}

@media (prefers-reduced-motion: reduce) {
  .home-page { animation: none; }
  .orb       { animation: none; }
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
.home-header { text-align: center; }
.home-title    { font-size: 20px; font-weight: 600; color: #1c1f26; letter-spacing: -0.015em; }
.home-subtitle { font-size: 13px; color: #9aa0ad; margin-top: 3px; }

/* ── Space cards ── */
.space-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 12px;
  width: 100%;
  max-width: 960px;
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
.state-text  { font-size: 13px; color: #9aa0ad; }
.state-icon  { width: 32px; height: 32px; }
.error-icon  { color: #e5534b; }

/* ── Spinner ── */
.spinner {
  width: 20px; height: 20px;
  border: 2px solid #d8d3cb; border-top-color: #1b6feb;
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
  color: #9aa0ad;
  border-top: 1px solid #e2ddd5;
  background: transparent;
  position: relative;
  z-index: 1;
}
</style>
