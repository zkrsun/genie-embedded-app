<template>
  <div class="pill-filter" role="tablist" :aria-label="label">
    <button
      v-for="item in items"
      :key="item"
      role="tab"
      class="pill"
      :class="{ active: modelValue === item, small }"
      :aria-selected="modelValue === item"
      @click="$emit('update:modelValue', item)"
    >
      {{ item }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  items:      { type: Array,  required: true },
  modelValue: { type: String, default: null },
  label:      { type: String, default: 'Filter' },
  small:      { type: Boolean, default: false },
})
defineEmits(['update:modelValue'])
</script>

<style scoped>
.pill-filter { display: flex; gap: 6px; flex-wrap: wrap; }

.pill {
  padding: 5px 16px;
  border-radius: 20px;
  border: 1px solid #d0cbc2;
  background: rgba(255, 255, 255, 0.65);
  font-family: inherit;
  font-size: 13px;
  font-weight: 500;
  color: #5c6070;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s, color 0.15s;
}
.pill.small { padding: 3px 12px; font-size: 12px; }
.pill:hover  { background: #ffffff; border-color: #b8b2a8; color: #1c1f26; }
.pill.active { background: #1c1f26; border-color: #1c1f26; color: #ffffff; }
</style>
