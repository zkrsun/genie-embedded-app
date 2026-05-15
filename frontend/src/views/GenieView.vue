<template>
  <div
    ref="wrapRef"
    class="genie-wrap"
    :class="{ 'with-pbi': showPbi, 'pbi-open': pbiOpen, resizing: isResizing }"
  >
    <!-- Collapsible PowerBI panel (test_pl only) — slides in from left, drag right edge to resize -->
    <section
      v-if="showPbi"
      class="pbi-panel"
      :class="{ open: pbiOpen }"
      :style="pbiPanelStyle"
    >
      <div v-show="pbiOpen" class="pbi-body">
        <div ref="pbiContainerRef" class="pbi-embed" />
        <div v-if="pbiLoading" class="pbi-overlay">
          <div class="spinner" />
        </div>
        <div v-else-if="pbiError" class="pbi-overlay pbi-error">
          {{ pbiError }}
        </div>
      </div>

      <div
        v-if="pbiOpen"
        class="pbi-resize-handle"
        role="separator"
        aria-orientation="vertical"
        aria-label="Drag to resize PowerBI panel"
        title="Drag to resize"
        @mousedown="startResize"
      >
        <span class="pbi-resize-grip" aria-hidden="true">
          <span /><span /><span />
        </span>
      </div>

      <button
        type="button"
        class="pbi-toggle"
        :aria-expanded="pbiOpen"
        :aria-label="pbiOpen ? 'Collapse PowerBI panel' : 'Expand PowerBI panel'"
        :title="pbiOpen ? 'Collapse' : 'Expand'"
        @click="togglePbi"
      >
        <img class="pbi-toggle-chart" src="/powerbi-icon.ico" alt="" aria-hidden="true" />
        <span class="pbi-toggle-label">Power BI</span>
        <span class="pbi-toggle-chevron" aria-hidden="true">
          <svg viewBox="0 0 16 16" :class="{ flipped: pbiOpen }">
            <path d="M6 4l4 4-4 4" stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </span>
      </button>
    </section>

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
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { store, setActiveSpace } from '../store.js'

const route    = useRoute()
const router   = useRouter()
const spaceUrl = ref(null)

const PBI_SPACES = ['test_pl', 'asia_th_pos']
const showPbi = computed(() => PBI_SPACES.includes(route.params.space))

const pbiOpen      = ref(false)
const pbiLoading   = ref(false)
const pbiError     = ref(null)
const pbiContainerRef = ref(null)
const wrapRef      = ref(null)
let pbiEmbed = null
let pbiLoaded = false

const pbiWidthPct = ref(75)
const isResizing  = ref(false)
const MIN_PCT = 20
const MAX_PCT = 92

const pbiPanelStyle = computed(() =>
  pbiOpen.value ? { width: pbiWidthPct.value + '%' } : null,
)

function togglePbi() {
  pbiOpen.value = !pbiOpen.value
}

let dragStartX = 0
let dragStartPct = 0
let dragWrapWidth = 0

function onResize(e) {
  if (!dragWrapWidth) return
  const deltaPct = ((e.clientX - dragStartX) / dragWrapWidth) * 100
  let next = dragStartPct + deltaPct
  if (next < MIN_PCT) next = MIN_PCT
  if (next > MAX_PCT) next = MAX_PCT
  pbiWidthPct.value = next
}

function stopResize() {
  isResizing.value = false
  document.removeEventListener('mousemove', onResize)
  document.removeEventListener('mouseup', stopResize)
  document.body.style.cursor = ''
  document.body.style.userSelect = ''
}

function startResize(e) {
  if (!wrapRef.value) return
  e.preventDefault()
  dragWrapWidth = wrapRef.value.clientWidth
  dragStartX = e.clientX
  dragStartPct = pbiWidthPct.value
  isResizing.value = true
  document.addEventListener('mousemove', onResize)
  document.addEventListener('mouseup', stopResize)
  document.body.style.cursor = 'col-resize'
  document.body.style.userSelect = 'none'
}

async function loadPbi() {
  if (pbiLoaded) return
  pbiLoading.value = true
  pbiError.value = null

  try {
    const res = await fetch(`/api/pbi/embed?space=${encodeURIComponent(route.params.space)}`)
    if (!res.ok) {
      const detail = await res.text()
      throw new Error(`HTTP ${res.status}: ${detail}`)
    }
    const cfg = await res.json()

    const pbiSdk = window.powerbi
    if (!pbiSdk || !pbiSdk.embed) {
      throw new Error('Power BI SDK is not loaded (window.powerbi missing)')
    }
    const models = (window['powerbi-client'] && window['powerbi-client'].models) || (window.powerbi && window.powerbi.models)

    const container = pbiContainerRef.value
    if (!container) throw new Error('PBI container not available')
    container.innerHTML = ''

    const embedConfiguration = {
      type: 'report',
      id: cfg.reportId,
      embedUrl: cfg.embedUrl,
      accessToken: cfg.accessToken,
      tokenType: models ? models.TokenType.Embed : 1,
      settings: {
        panes: {
          filters: { expanded: false, visible: true },
          pageNavigation: { visible: true },
        },
        background: models ? models.BackgroundType.Transparent : 1,
      },
    }

    pbiEmbed = pbiSdk.embed(container, embedConfiguration)
    pbiEmbed.on('loaded', () => { pbiLoading.value = false })
    pbiEmbed.off('error')
    pbiEmbed.on('error', (event) => {
      pbiError.value = (event && event.detail && (event.detail.message || event.detail.errorMsg)) || 'PowerBI embed error'
      pbiLoading.value = false
    })
    pbiLoaded = true
  } catch (err) {
    pbiError.value = err.message || String(err)
    pbiLoading.value = false
  }
}

watch(pbiOpen, async (open) => {
  if (open && showPbi.value) {
    await nextTick()
    loadPbi()
  }
})

watch(() => route.params.space, () => {
  if (pbiEmbed) {
    try { pbiEmbed.reset() } catch (_) {}
    pbiEmbed = null
  }
  pbiLoaded = false
  pbiError.value = null
  pbiOpen.value = false
})

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

onUnmounted(() => {
  if (pbiEmbed) {
    try { pbiEmbed.reset() } catch (_) {}
    pbiEmbed = null
  }
  document.removeEventListener('mousemove', onResize)
  document.removeEventListener('mouseup', stopResize)
})
</script>

<style scoped>
.genie-wrap {
  position: relative;
  display: flex;
  flex-direction: row;
  height: 100%;
  width: 100%;
  background: var(--color-bg-light);
}
.genie-frame {
  display: block;
  flex: 1;
  min-width: 0;
  height: 100%;
  border: none;
  background: var(--color-bg-white);
}
.loading-view {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}
.spinner {
  width: 24px;
  height: 24px;
  border: 2.5px solid var(--color-primary-light);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── PowerBI panel ───────────────────────────────────────────────────── */
.pbi-panel {
  flex-shrink: 0;
  background: var(--color-bg-white);
  display: flex;
  flex-direction: row;
  transition: width var(--transition-slow);
  width: 48px;
  height: 100%;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}
.pbi-panel.open {
  box-shadow: var(--shadow-md);
}
.genie-wrap.resizing .pbi-panel { transition: none; }
.genie-wrap.resizing .pbi-embed,
.genie-wrap.resizing .genie-frame { pointer-events: none; }

.pbi-body {
  flex: 1;
  min-width: 0;
  position: relative;
  overflow: hidden;
  background: var(--color-bg-white);
}
.pbi-embed { width: 100%; height: 100%; }

/* ── Resize handle ───────────────────────────────────────────────────── */
.pbi-resize-handle {
  flex-shrink: 0;
  width: 8px;
  height: 100%;
  cursor: col-resize;
  background: transparent;
  border-left: 1px solid var(--color-border);
  border-right: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background var(--transition-fast), border-color var(--transition-fast);
  position: relative;
}
.pbi-resize-grip {
  display: flex;
  flex-direction: column;
  gap: 3px;
  opacity: 0.45;
  transition: opacity var(--transition-fast);
}
.pbi-resize-grip span {
  width: 2px;
  height: 2px;
  border-radius: 50%;
  background: var(--color-text-tertiary);
}
.pbi-resize-handle:hover {
  background: var(--color-primary-light);
  border-left-color: var(--color-primary);
  border-right-color: var(--color-primary);
}
.pbi-resize-handle:hover .pbi-resize-grip { opacity: 1; }
.pbi-resize-handle:hover .pbi-resize-grip span { background: var(--color-primary); }
.genie-wrap.resizing .pbi-resize-handle {
  background: var(--color-primary);
  border-color: var(--color-primary);
}
.genie-wrap.resizing .pbi-resize-grip span { background: var(--color-bg-white); opacity: 1; }

/* ── Toggle button (vertical sidebar) ────────────────────────────────── */
.pbi-toggle {
  flex-shrink: 0;
  width: 48px;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 14px;
  padding: 20px 0;
  background: var(--color-bg-white);
  border: none;
  border-left: 1px solid var(--color-border);
  cursor: pointer;
  color: var(--color-text-secondary);
  transition: background var(--transition-base), color var(--transition-base);
  font-family: inherit;
  position: relative;
}
.pbi-toggle::before {
  content: '';
  position: absolute;
  inset: 0 auto 0 0;
  width: 3px;
  background: var(--color-primary);
  opacity: 0;
  transition: opacity var(--transition-base);
}
.pbi-toggle:hover {
  background: var(--color-primary-light);
  color: var(--color-primary-dark);
}
.pbi-toggle:hover::before { opacity: 1; }
.pbi-toggle:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: -2px;
}
.pbi-toggle-chart {
  width: 24px;
  height: 24px;
  display: block;
  object-fit: contain;
}
.pbi-toggle-label {
  writing-mode: vertical-rl;
  transform: rotate(180deg);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--color-text-primary);
}
.pbi-toggle-chevron {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: var(--radius-full);
  background: var(--color-bg-subtle);
  color: var(--color-text-secondary);
  transition: background var(--transition-base), color var(--transition-base);
}
.pbi-toggle:hover .pbi-toggle-chevron {
  background: var(--color-primary);
  color: var(--color-bg-white);
}
.pbi-toggle-chevron svg {
  width: 12px;
  height: 12px;
  transition: transform var(--transition-base);
}
.pbi-toggle-chevron svg.flipped {
  transform: rotate(180deg);
}

/* ── Overlays ────────────────────────────────────────────────────────── */
.pbi-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(2px);
  z-index: 5;
}
.pbi-error {
  color: var(--color-error);
  background: var(--color-error-light);
  font-size: 14px;
  font-weight: 500;
  padding: 24px 32px;
  border-radius: var(--radius-md);
  text-align: center;
  max-width: 80%;
  border: 1px solid rgba(239, 68, 68, 0.2);
}
</style>
