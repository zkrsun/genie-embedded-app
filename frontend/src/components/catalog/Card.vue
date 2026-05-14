<template>
  <div class="card" :class="{ 'card-hover': hoverable }">
    <slot></slot>
  </div>
</template>

<script setup>
defineProps({
  hoverable: { type: Boolean, default: true },
})
</script>

<style scoped>
.card {
  background: #ffffff;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 1.75rem;
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
}
.card::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 4px; height: 100%;
  background: linear-gradient(180deg, var(--color-primary), var(--color-secondary));
  transform: scaleY(0);
  transform-origin: top;
  transition: transform var(--transition-base);
}
.card-hover:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-lg);
  transform: translateY(-4px);
}
.card-hover:hover::before { transform: scaleY(1); }
</style>
