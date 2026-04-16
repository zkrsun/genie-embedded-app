<template>
  <div class="bu-filter" role="tablist" aria-label="Business Unit">
    <button
      v-for="bu in buList"
      :key="bu"
      role="tab"
      class="bu-pill"
      :class="{ active: modelValue === bu }"
      :aria-selected="modelValue === bu"
      @click="$emit('update:modelValue', bu)"
    >
      {{ bu }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  buList:     { type: Array,  required: true },
  modelValue: { type: String, default: null },
})
defineEmits(['update:modelValue'])
</script>

<style scoped>
.bu-filter { display: flex; gap: 6px; flex-wrap: wrap; }

/* Matches Databricks "For you | Dashboards | Genie spaces | Apps" pills */
.bu-pill {
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
.bu-pill:hover  { background: #ffffff; border-color: #b8b2a8; color: #1c1f26; }
.bu-pill.active { background: #1c1f26; border-color: #1c1f26; color: #ffffff; }
</style>
