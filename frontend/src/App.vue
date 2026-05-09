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
        <RouterLink
          class="bc-bu"
          :to="{ name: 'home', query: { bu: store.activeSpace?.bu } }"
        >{{ store.activeSpace?.bu }}</RouterLink>
        <span class="bc-sep">·</span>
        <RouterLink
          class="bc-domain"
          :to="{ name: 'home', query: { bu: store.activeSpace?.bu, domain: store.activeSpace?.domain } }"
        >{{ store.activeSpace?.domain }}</RouterLink>
      </nav>

      <div class="spacer" />
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
.bc-bu,.bc-domain {
  font-size: 11px; color: #9aa0ad; text-transform: uppercase; letter-spacing: 0.06em;
  text-decoration: none; transition: color 0.15s; cursor: pointer;
}
.bc-bu:hover,.bc-domain:hover { color: #1c1f26; }

/* Page content area */
.page-content { flex: 1; overflow: hidden; background: #efebe4; }
</style>
