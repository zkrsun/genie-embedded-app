<template>
  <select :value="modelValue" @change="$emit('update:modelValue', $event.target.value)" class="select">
    <option v-for="option in options" :key="option.value" :value="option.value">
      {{ option.label }}
    </option>
  </select>
</template>

<script setup>
defineProps({
  options: { type: Array, required: true },
  modelValue: { type: [String, Number], default: '' },
})
defineEmits(['update:modelValue'])
</script>

<style scoped>
.select {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #eeeeee;
  border-radius: 8px;
  font-size: 16px;
  background-color: #ffffff;
  cursor: pointer;
  transition: all 0.3s;
}
.select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}
.select:hover { border-color: #d4d4d4; }
</style>
