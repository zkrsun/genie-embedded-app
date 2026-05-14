<template>
  <button :class="['btn', `btn-${variant}`, { 'btn-full-width': fullWidth }]">
    <slot></slot>
  </button>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'outline'].includes(value),
  },
  fullWidth: {
    type: Boolean,
    default: false,
  },
})
</script>

<style scoped>
.btn {
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius-md);
  border: none;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-base);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  position: relative;
  overflow: hidden;
  white-space: nowrap;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}
.btn::before {
  content: '';
  position: absolute;
  top: 50%; left: 50%;
  width: 0; height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}
.btn:active::before { width: 300px; height: 300px; }
.btn:focus-visible {
  outline: 2px solid var(--color-secondary);
  outline-offset: 3px;
  box-shadow: 0 0 0 4px var(--color-primary-light);
}
.btn:disabled { opacity: 0.5; cursor: not-allowed; pointer-events: none; }

.btn-primary {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-hover) 100%);
  color: #ffffff;
  box-shadow: var(--shadow-sm);
}
.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--color-primary-hover) 0%, var(--color-primary-dark) 100%);
  box-shadow: var(--shadow-primary);
  transform: translateY(-2px);
}
.btn-primary:active:not(:disabled) { transform: translateY(0); box-shadow: var(--shadow-sm); }

.btn-secondary {
  background: linear-gradient(135deg, var(--color-secondary) 0%, var(--color-secondary-hover) 100%);
  color: #ffffff;
  box-shadow: var(--shadow-sm);
}
.btn-secondary:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--color-secondary-hover) 0%, var(--color-primary-dark) 100%);
  box-shadow: var(--shadow-primary);
  transform: translateY(-2px);
}
.btn-secondary:active:not(:disabled) { transform: translateY(0); box-shadow: var(--shadow-sm); }

.btn-outline {
  background-color: transparent;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
  box-shadow: none;
}
.btn-outline:hover:not(:disabled) {
  background-color: var(--color-primary-light);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}
.btn-outline:active:not(:disabled) { transform: translateY(0); }

.btn-full-width { width: 100%; }
</style>
