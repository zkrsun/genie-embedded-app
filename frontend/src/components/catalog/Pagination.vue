<template>
  <div class="pagination" v-if="totalPages > 1">
    <button class="page-btn" :disabled="currentPage === 1" @click="goToPage(1)" title="First page">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="11 17 6 12 11 7"></polyline>
        <polyline points="18 17 13 12 18 7"></polyline>
      </svg>
    </button>
    <button class="page-btn" :disabled="currentPage === 1" @click="goToPage(currentPage - 1)" title="Previous page">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="15 18 9 12 15 6"></polyline>
      </svg>
    </button>
    <template v-for="page in displayedPages" :key="page">
      <span v-if="page === '...'" class="page-ellipsis">...</span>
      <button v-else class="page-btn page-number" :class="{ active: page === currentPage }" @click="goToPage(page)">
        {{ page }}
      </button>
    </template>
    <button class="page-btn" :disabled="currentPage === totalPages" @click="goToPage(currentPage + 1)" title="Next page">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="9 18 15 12 9 6"></polyline>
      </svg>
    </button>
    <button class="page-btn" :disabled="currentPage === totalPages" @click="goToPage(totalPages)" title="Last page">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="13 17 18 12 13 7"></polyline>
        <polyline points="6 17 11 12 6 7"></polyline>
      </svg>
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: { type: Number, required: true },
  totalPages:  { type: Number, required: true },
  totalCount:  { type: Number, required: true },
})
const emit = defineEmits(['page-change'])

const displayedPages = computed(() => {
  const pages = []
  const current = props.currentPage
  const total = props.totalPages
  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    pages.push(1)
    if (current > 3) pages.push('...')
    const start = Math.max(2, current - 1)
    const end = Math.min(total - 1, current + 1)
    for (let i = start; i <= end; i++) pages.push(i)
    if (current < total - 2) pages.push('...')
    pages.push(total)
  }
  return pages
})

const goToPage = (page) => {
  if (page !== props.currentPage && page >= 1 && page <= props.totalPages) {
    emit('page-change', page)
  }
}
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #eeeeee;
}
.page-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  padding: 0 0.25rem;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  background: white;
  color: #666666;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.page-btn svg { width: 12px; height: 12px; }
.page-btn:hover:not(:disabled) { border-color: var(--color-primary); color: var(--color-primary); }
.page-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.page-btn.active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: white;
}
.page-ellipsis { padding: 0 0.25rem; color: #999999; }

@media (max-width: 640px) {
  .pagination { flex-wrap: wrap; justify-content: center; }
}
</style>
