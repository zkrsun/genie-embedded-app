<template>
  <iframe
    :key="store.activeSpace?.url"
    :src="store.activeSpace?.url"
    allow="clipboard-write"
    class="genie-frame"
    title="Genie Space"
  />
</template>

<script setup>
import { store } from '../store.js'
</script>

<style scoped>
.genie-frame {
  display: block;
  width: 100%;
  height: 100%;
  border: none;
  /* Prevent parent background bleeding through the transparent iframe body */
  background: #ffffff;
}
</style>
