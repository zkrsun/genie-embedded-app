<template>
  <div class="layout">
    <!-- ── Navbar ── -->
    <header class="navbar">
      <div class="navbar-brand">
        <img class="brand-icon" :src="naviIcon" alt="Genie icon" />
      </div>

      <!-- Breadcrumb shown when inside a Genie space -->
      <nav v-if="route.name === 'genie'" class="breadcrumb" aria-label="breadcrumb">
        <RouterLink class="back-link" :to="{ name: 'home' }">Data Download</RouterLink>
        <span class="bc-sep">›</span>
        <span class="bc-current">{{ store.activeSpace?.name }}</span>
        <span class="bc-sep">·</span>
        <span class="bc-bu">{{ store.activeSpace?.bu }}</span>
      </nav>

      <div class="spacer" />

      <!-- Action buttons -->
      <div class="navbar-actions">
        <RouterLink
          :to="{ name: 'home' }"
          class="nav-btn"
          :class="{ 'nav-btn--active': route.name === 'home' || route.name === 'genie' }"
        >
          <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <ellipse cx="12" cy="7" rx="8" ry="3"/>
            <path d="M4 7v5c0 1.657 3.582 3 8 3s8-1.343 8-3V7"/>
            <path d="M4 12v5c0 1.657 3.582 3 8 3s8-1.343 8-3v-5"/>
          </svg>
          Data Download
        </RouterLink>

        <button class="nav-btn nav-btn--analysis" @click="openAnalysis">
          <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
          </svg>
          Analysis
          <svg class="btn-icon-ext" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
            <polyline points="15 3 21 3 21 9"/>
            <line x1="10" y1="14" x2="21" y2="3"/>
          </svg>
        </button>
      </div>
    </header>

    <!-- ── Page content ── -->
    <RouterView class="page-content" />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { store } from './store.js'
import naviIcon from '../icon/navi.svg'

const route = useRoute()

function openAnalysis() {
  window.open('https://open-data-center-2205520462893510.10.azure.databricksapps.com/', '_blank')
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

/*
 * Design token reference — Databricks "one" page palette
 * bg-page:    #EFEBE4  warm cream
 * bg-surface: #FFFFFF
 * border:     #E2DDD5  warm grey
 * text-1:     #1C1F26  near-black
 * text-2:     #5C6070  medium
 * text-3:     #9AA0AD  muted
 * accent:     #1B6FEB  Databricks blue
 */

*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: #efebe4;
  color: #1c1f26;
  -webkit-font-smoothing: antialiased;
}

.layout { display: flex; flex-direction: column; height: 100vh; }

/* ── Navbar ── */
.navbar {
  display: flex;
  align-items: center;
  padding: 0 24px;
  height: 48px;
  background: #ffffff;
  border-bottom: 1px solid #e2ddd5;
  flex-shrink: 0;
  gap: 12px;
}

.navbar-brand { display: flex; align-items: center; flex-shrink: 0; }
.brand-icon   { display: block; width: 26px; height: 26px; border-radius: 6px; object-fit: contain; }

.spacer { flex: 1; }

/* Breadcrumb */
.breadcrumb { display: flex; align-items: center; gap: 6px; }
.back-link {
  font-size: 13px; font-weight: 500; color: #5c6070;
  text-decoration: none;
  transition: color 0.15s;
}
.back-link:hover { color: #1c1f26; }
.bc-sep     { color: #c8c3bb; font-size: 14px; }
.bc-current { font-size: 13px; font-weight: 600; color: #1c1f26; }
.bc-bu      { font-size: 11px; color: #9aa0ad; text-transform: uppercase; letter-spacing: 0.06em; }

/* Action buttons */
.navbar-actions { display: flex; align-items: center; gap: 8px; }

.nav-btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 0 13px; height: 32px;
  border: 1px solid #d8d3cb; border-radius: 6px;
  background: #ffffff;
  font-family: inherit; font-size: 13px; font-weight: 500; color: #5c6070;
  cursor: pointer; white-space: nowrap; text-decoration: none;
  transition: background 0.15s, color 0.15s, border-color 0.15s;
}
.nav-btn:hover         { background: #f5f2ee; color: #1c1f26; border-color: #c0bab1; }
.nav-btn--active       { background: #1c1f26; color: #ffffff;  border-color: #1c1f26; }
.nav-btn--active:hover { background: #2e3240; border-color: #2e3240; }
.nav-btn--analysis     { background: #1b6feb; color: #ffffff;  border-color: #1b6feb; }
.nav-btn--analysis:hover { background: #1558cc; border-color: #1558cc; }

.btn-icon     { width: 14px; height: 14px; flex-shrink: 0; }
.btn-icon-ext { width: 12px; height: 12px; flex-shrink: 0; opacity: 0.7; }

/* Page content area */
.page-content { flex: 1; overflow: hidden; background: #efebe4; }
</style>
