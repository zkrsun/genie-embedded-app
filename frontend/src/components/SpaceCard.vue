<template>
  <button class="space-card" @click="$emit('select', space)">
    <div class="card-header">
      <div class="card-icon-wrap">
        <!-- Custom multi-path icon -->
        <svg v-if="iconConfig.paths" :viewBox="iconConfig.viewBox">
          <path
            v-for="(p, i) in iconConfig.paths"
            :key="i"
            :d="p.d"
            :fill="p.fill"
            :fill-rule="p.fillRule"
            :clip-rule="p.clipRule"
            :opacity="p.opacity"
          />
        </svg>
        <!-- Default single-path icon -->
        <svg v-else :viewBox="iconConfig.viewBox" fill="none" stroke="currentColor" stroke-width="1.5">
          <path :d="iconConfig.path" />
        </svg>
      </div>
    </div>

    <div class="card-body">
      <div class="card-name">{{ space.name }}</div>
      <p v-if="space.description" class="card-desc">{{ space.description }}</p>
    </div>

    <div class="card-footer">
      <span class="card-hits">
        <svg class="hit-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M13 2 4 14h7l-1 8 9-12h-7Z"/>
        </svg>
        <strong>{{ hitsLabel }}</strong>&nbsp;hits in last 30 days
      </span>
      <span class="card-open">
        Open
        <svg class="card-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="5" y1="12" x2="19" y2="12"/>
          <polyline points="12 5 19 12 12 19"/>
        </svg>
      </span>
    </div>
  </button>
</template>

<script setup>
import { computed } from 'vue'
import { getCategoryIconConfig } from '../config/categoryConfig.js'

const props = defineProps({
  space: { type: Object, required: true },  // { name, code, url, description, icon_code, access_count }
})
defineEmits(['select'])

const iconConfig = computed(() => getCategoryIconConfig(props.space.icon_code))

const hitsLabel = computed(() => {
  const n = props.space.access_count ?? 0
  if (n < 1000) return String(n)
  if (n < 1_000_000) return (n / 1000).toFixed(n < 10_000 ? 1 : 0) + 'K'
  return (n / 1_000_000).toFixed(1) + 'M'
})
</script>

<style scoped>
.space-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 18px 20px 14px;
  background: var(--color-bg-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  text-align: left;
  font-family: inherit;
  width: 100%;
  min-height: 168px;
  transition: box-shadow var(--transition-base), border-color var(--transition-base), transform var(--transition-fast);
}
.space-card:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}
.space-card:active { transform: translateY(0); box-shadow: var(--shadow-sm); }

.card-header { display: flex; align-items: center; }

.card-icon-wrap {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  background: var(--color-primary-light);
  color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.card-icon-wrap svg { width: 22px; height: 22px; }

.card-body  { flex: 1; min-width: 0; }
.card-name  { font-size: 15px; font-weight: 600; color: var(--color-text-primary); }
.card-desc  {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-top: 6px;
  line-height: 1.5;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  font-size: 12px;
  font-weight: 500;
  border-top: 1px solid var(--color-border-light);
  padding-top: 10px;
}
.card-hits {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: var(--color-text-secondary);
}
.card-hits strong { color: var(--color-text-primary); font-weight: 600; }
.hit-icon { width: 12px; height: 12px; color: var(--color-primary); flex-shrink: 0; }

.card-open {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: var(--color-primary);
  letter-spacing: 0.02em;
  transition: gap var(--transition-base);
}
.card-arrow { width: 14px; height: 14px; transition: transform var(--transition-base); }
.space-card:hover .card-open  { gap: 6px; }
.space-card:hover .card-arrow { transform: translateX(2px); }
</style>
