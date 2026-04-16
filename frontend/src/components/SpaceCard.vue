<template>
  <button class="space-card" @click="$emit('select', space)">
    <div class="card-icon-wrap">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <ellipse cx="12" cy="6" rx="8" ry="3"/>
        <path d="M4 6v4c0 1.657 3.582 3 8 3s8-1.343 8-3V6"/>
        <path d="M4 10v4c0 1.657 3.582 3 8 3s8-1.343 8-3v-4"/>
      </svg>
    </div>

    <div class="card-body">
      <div class="card-name">{{ space.name }}</div>
      <div class="card-bu">{{ bu }}</div>
    </div>

    <svg class="card-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <line x1="5" y1="12" x2="19" y2="12"/>
      <polyline points="12 5 19 12 12 19"/>
    </svg>
  </button>
</template>

<script setup>
defineProps({
  space: { type: Object, required: true },  // { name, url }
  bu:    { type: String, required: true },
})
defineEmits(['select'])
</script>

<style scoped>
/* Matches Databricks Genie space card style */
.space-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px 20px;
  background: #ffffff;
  border: 1px solid #e2ddd5;
  border-radius: 8px;
  cursor: pointer;
  text-align: left;
  font-family: inherit;
  width: 100%;
  transition: box-shadow 0.18s, border-color 0.18s, transform 0.12s;
}
.space-card:hover {
  border-color: #b8b2a8;
  box-shadow: 0 2px 12px rgba(28, 31, 38, 0.08);
  transform: translateY(-1px);
}
.space-card:active { transform: translateY(0); box-shadow: none; }

.card-icon-wrap {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  background: #eef4ff;
  color: #1b6feb;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.card-icon-wrap svg { width: 19px; height: 19px; }

.card-body  { flex: 1; min-width: 0; }
.card-name  { font-size: 14px; font-weight: 600; color: #1c1f26; }
.card-bu    { font-size: 11px; color: #9aa0ad; margin-top: 2px; text-transform: uppercase; letter-spacing: 0.06em; }

.card-arrow { width: 15px; height: 15px; color: #c8c3bb; flex-shrink: 0; transition: color 0.15s, transform 0.15s; }
.space-card:hover .card-arrow { color: #1b6feb; transform: translateX(3px); }
</style>
