<template>
  <div class="layout">
    <!-- ── Navbar ── -->
    <header class="navbar">
      <div class="navbar-brand">
        <img class="brand-icon" :src="naviIcon" alt="Genie icon" />
        <span class="brand-name">DataNavi</span>
        <span class="brand-tagline">— Data made conversational</span>
      </div>

      <div class="spacer" />

      <!-- Primary navigation links -->
      <ul class="navbar-links" role="menubar">
        <li role="none">
          <RouterLink to="/" class="nav-link" role="menuitem" active-class="active" exact-active-class="active">
            <span class="nav-text">Home</span>
          </RouterLink>
        </li>
        <li role="none">
          <RouterLink to="/getting-started" class="nav-link" role="menuitem" active-class="active">
            <span class="nav-text">Getting Started</span>
          </RouterLink>
        </li>
        <li role="none">
          <a href="#" class="nav-link is-disabled" role="menuitem" @click.prevent aria-disabled="true">
            <span class="nav-text">Help</span>
            <span class="soon-badge">Soon</span>
          </a>
        </li>
        <li role="none">
          <RouterLink to="/catalog" class="nav-link" role="menuitem" active-class="active">
            <span class="nav-text">Catalog</span>
          </RouterLink>
        </li>
      </ul>
    </header>

    <!-- ── Page content ── -->
    <RouterView class="page-content" />
  </div>
</template>

<script setup>
import naviIcon from '../icon/navi.svg'
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
  background: var(--color-bg-light);
  color: var(--color-text-primary);
  -webkit-font-smoothing: antialiased;
}

.layout { display: flex; flex-direction: column; height: 100vh; }

/* ── Navbar ── */
.navbar {
  display: flex;
  align-items: center;
  padding: 0 24px 0 56px;
  height: 72px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
  flex-shrink: 0;
  gap: 12px;
  position: sticky;
  top: 0;
  z-index: 30;
}

.navbar-brand { display: flex; align-items: center; flex-shrink: 0; gap: 12px; }
.brand-icon   { display: block; width: 51px; height: 51px; border-radius: 10px; object-fit: contain; }
.brand-name   { font-size: 18px; font-weight: 600; color: var(--color-text-primary); letter-spacing: -0.01em; }
.brand-tagline { font-size: 13px; color: var(--color-text-tertiary); font-weight: 500; }

.spacer { flex: 1; }

/* Primary nav links */
.navbar-links {
  list-style: none;
  display: flex;
  align-items: center;
  gap: 4px;
}
.nav-link {
  display: flex;
  align-items: center;
  padding: 8px 14px;
  text-decoration: none;
  color: var(--color-text-secondary);
  font-weight: 500;
  font-size: 14px;
  border-radius: var(--radius-md);
  position: relative;
  transition: color var(--transition-base), background var(--transition-base), transform var(--transition-fast);
  white-space: nowrap;
}
.nav-link::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: var(--color-primary);
  transform: translateX(-50%);
  transition: width var(--transition-base);
}
.nav-link:hover {
  color: var(--color-primary);
  background: var(--color-primary-light);
  transform: translateY(-1px);
}
.nav-link.active {
  color: var(--color-primary);
  background: var(--color-primary-light);
}
.nav-link.active::before { width: 70%; }
.nav-text { line-height: 1.5; }

.nav-link.is-disabled {
  cursor: not-allowed;
  color: var(--color-text-tertiary);
}
.nav-link.is-disabled:hover {
  color: var(--color-text-tertiary);
  background: transparent;
  transform: none;
}
.soon-badge {
  margin-left: 6px;
  padding: 1px 7px;
  background: var(--color-warning-light);
  color: #a37500;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  border-radius: var(--radius-full);
  border: 1px solid #f3e2a8;
  line-height: 1.4;
}

/* Page content area */
.page-content { flex: 1; overflow: hidden; background: var(--color-bg-light); }
</style>
