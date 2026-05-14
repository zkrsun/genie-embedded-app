<template>
  <input
    type="text"
    :placeholder="placeholder"
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)"
    class="input"
  />
</template>

<script setup>
defineProps({
  placeholder: { type: String, default: '' },
  modelValue: { type: String, default: '' },
})
defineEmits(['update:modelValue'])
</script>

<style scoped>
.input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #eeeeee;
  border-radius: 8px;
  font-size: 16px;
  font-family: inherit;
  transition: all 0.3s;
}
.input::placeholder { color: #999999; }
.input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}
</style>
