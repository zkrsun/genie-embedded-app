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
          <a href="#" class="nav-link is-disabled" role="menuitem" @click.prevent aria-disabled="true">
            <span class="nav-text">Catalog</span>
            <span class="soon-badge">Soon</span>
          </a>
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
  background: #efebe4;
  color: #1c1f26;
  -webkit-font-smoothing: antialiased;
}

.layout { display: flex; flex-direction: column; height: 100vh; }

/* ── Navbar ── */
.navbar {
  display: flex;
  align-items: center;
  padding: 0 24px 0 56px;
  height: 72px;
  background: #ffffff;
  border-bottom: 1px solid #e2ddd5;
  flex-shrink: 0;
  gap: 12px;
}

.navbar-brand { display: flex; align-items: center; flex-shrink: 0; gap: 12px; }
.brand-icon   { display: block; width: 51px; height: 51px; border-radius: 10px; object-fit: contain; }
.brand-name   { font-size: 18px; font-weight: 600; color: #1c1f26; letter-spacing: -0.01em; }
.brand-tagline { font-size: 13px; color: #9aa0ad; font-weight: 500; }

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
  color: #5c6070;
  font-weight: 500;
  font-size: 14px;
  border-radius: 8px;
  position: relative;
  transition: color 0.15s, background 0.15s, transform 0.12s;
  white-space: nowrap;
}
.nav-link::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: #1b6feb;
  transform: translateX(-50%);
  transition: width 0.18s ease;
}
.nav-link:hover {
  color: #1c1f26;
  background: #f4f1ea;
  transform: translateY(-1px);
}
.nav-link.active {
  color: #1b6feb;
  background: #eef4ff;
}
.nav-link.active::before { width: 70%; }
.nav-text { line-height: 1.5; }

.nav-link.is-disabled {
  cursor: not-allowed;
  color: #9aa0ad;
}
.nav-link.is-disabled:hover {
  color: #9aa0ad;
  background: transparent;
  transform: none;
}
.soon-badge {
  margin-left: 6px;
  padding: 1px 7px;
  background: #fff4d6;
  color: #a37500;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  border-radius: 9999px;
  border: 1px solid #f3e2a8;
  line-height: 1.4;
}

/* Page content area */
.page-content { flex: 1; overflow: hidden; background: #efebe4; }
</style>
