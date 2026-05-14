<template>
  <div class="search-box">
    <input
      type="text"
      :placeholder="placeholder"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      @keyup.enter="$emit('search')"
      class="search-input"
    />
    <button @click="$emit('search')" class="search-button" aria-label="Search">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"/>
        <line x1="21" y1="21" x2="16.65" y2="16.65"/>
      </svg>
    </button>
  </div>
</template>

<script setup>
defineProps({
  placeholder: { type: String, default: 'Search datasets...' },
  modelValue: { type: String, default: '' },
})
defineEmits(['update:modelValue', 'search'])
</script>

<style scoped>
.search-box {
  display: flex;
  align-items: center;
  background: #ffffff;
  border: 1px solid #eeeeee;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
}
.search-box:focus-within {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-primary);
}
.search-input {
  flex: 1;
  border: none;
  padding: 0.75rem 1rem;
  font-size: 16px;
  outline: none;
}
.search-input::placeholder { color: #999999; }
.search-button {
  background: none;
  border: none;
  padding: 0 1rem;
  cursor: pointer;
  color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.3s;
}
.search-button:hover { opacity: 0.8; }
</style>
