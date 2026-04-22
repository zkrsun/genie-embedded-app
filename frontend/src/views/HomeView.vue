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
        <!-- Level 1: BU -->
        <BuFilter :items="buNames" v-model="activeBu" label="Business Unit" />

        <!-- Level 2: Domain (hidden when BU = All) -->
        <BuFilter
          v-if="activeBu !== 'All'"
          :items="domainNames"
          v-model="activeDomain"
          label="Domain"
          :small="true"
        />

        <!-- Level 3: Spaces -->
        <div v-if="currentSpaces.length" class="space-grid">
          <SpaceCard
            v-for="space in currentSpaces"
            :key="space.code"
            :space="space"
            :bu="space._bu"
            :domain="space._domain"
            @select="onSelectSpace"
          />
        </div>
        <div v-else class="state-view">
          <p class="state-text">
            No spaces configured for
            {{ activeBu === 'All' ? 'any BU' : activeBu }}
            <template v-if="activeBu !== 'All' && activeDomain !== 'All'"> / {{ activeDomain }}</template>.
          </p>
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
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { store } from '../store.js'
import BuFilter  from '../components/BuFilter.vue'
import SpaceCard from '../components/SpaceCard.vue'
import naviIcon  from '../../icon/navi.svg'

const router      = useRouter()
const route       = useRoute()
const activeBu     = ref('All')
const activeDomain = ref('All')

const ALL = 'All'

// Level 1: BU names — "All" first, then each BU
const buNames = computed(() => [ALL, ...store.buList.map(b => b.name)])

// Level 2: domains of the selected BU
const currentDomains = computed(() => {
  if (activeBu.value === ALL) return []
  const bu = store.buList.find(b => b.name === activeBu.value)
  return bu?.domains ?? []
})
// "All" + domain names; hidden entirely when BU = All
const domainNames = computed(() => [ALL, ...currentDomains.value.map(d => d.name)])

// Level 3: spaces annotated with their BU and domain names for the card subtitle
const currentSpaces = computed(() => {
  if (activeBu.value === ALL) {
    return store.buList.flatMap(b =>
      b.domains.flatMap(d =>
        d.spaces.map(s => ({ ...s, _bu: b.name, _domain: d.name }))
      )
    )
  }
  const bu = store.buList.find(b => b.name === activeBu.value)
  if (!bu) return []
  if (activeDomain.value === ALL) {
    return bu.domains.flatMap(d =>
      d.spaces.map(s => ({ ...s, _bu: bu.name, _domain: d.name }))
    )
  }
  const domain = bu.domains.find(d => d.name === activeDomain.value)
  return (domain?.spaces ?? []).map(s => ({ ...s, _bu: bu.name, _domain: domain.name }))
})

// When BU changes, reset domain to "All"
watch(activeBu, () => {
  activeDomain.value = ALL
})

async function _applyQuery() {
  const qBu     = route.query.bu     ?? ALL
  const qDomain = route.query.domain ?? ALL
  activeBu.value = qBu
  // wait for watch(activeBu) to fire and reset domain, then override
  await nextTick()
  activeDomain.value = qDomain
}

onMounted(async () => {
  if (store.buList.length) {
    await _applyQuery()
    return
  }
  store.loading = true
  store.error   = null
  try {
    const res = await fetch('/api/all')
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    store.buList = await res.json()
    await _applyQuery()
  } catch (e) {
    store.error = `Failed to load data: ${e.message}`
  } finally {
    store.loading = false
  }
})

function onSelectSpace(space) {
  router.push({ name: 'genie', params: { bu: space._bu, domain: space._domain, space: space.code } })
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
