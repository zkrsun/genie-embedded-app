<template>
  <div class="catalog-root categories-page">
    <section class="page-header">
      <div class="container">
        <h1 class="page-title">Data categories</h1>
        <p class="page-subtitle">
          {{ categories.length }} categories in order of API calls over 6 months
        </p>
      </div>
    </section>

    <section class="categories-content">
      <div class="container">
        <div v-if="loading" class="loading-grid">
          <div v-for="i in 12" :key="`skeleton-${i}`" class="category-card-skeleton">
            <div class="skeleton skeleton-icon"></div>
            <div class="skeleton skeleton-title"></div>
            <div class="skeleton skeleton-stats"></div>
          </div>
        </div>

        <div v-else class="categories-grid">
          <div
            v-for="(category, index) in sortedCategories"
            :key="category.id"
            class="category-card"
            @click="handleCategoryClick(category.name)"
          >
            <div class="category-icon-wrapper">
              <svg class="category-icon" :viewBox="getCategoryIconConfig(category.name).viewBox" aria-hidden="true">
                <template v-if="getCategoryIconConfig(category.name).paths">
                  <path
                    v-for="(p, idx) in getCategoryIconConfig(category.name).paths"
                    :key="idx"
                    :d="p.d"
                    :fill="p.fill || 'currentColor'"
                    :fill-rule="p.fillRule"
                    :clip-rule="p.clipRule"
                  />
                </template>
                <path v-else :d="getCategoryIconConfig(category.name).path" fill="currentColor"/>
              </svg>
            </div>
            <div class="category-info">
              <h3 class="category-name">{{ category.name }}</h3>
              <div class="category-stats">
                <div class="stat-item">
                  <span class="stat-value">{{ formatLargeNumber(getCategoryApiCalls(index)) }}</span>
                  <span class="stat-label">API Calls</span>
                </div>
                <div class="stat-item">
                  <span class="stat-value">{{ formatLargeNumber(getCategoryDownloads(index)) }}</span>
                  <span class="stat-label">downloads</span>
                </div>
              </div>
            </div>
            <div class="category-arrow">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
        </div>

        <div v-if="!loading && categories.length === 0" class="empty-state">
          <p>No categories found.</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getAllCategories } from '../../utils/catalogApi'
import { getCategoryIconConfig } from '../../config/categoryConfig'

const router = useRouter()
const categories = ref([])
const loading = ref(true)

const mockApiCallsData = [
  840300000, 523000000, 312000000, 156000000, 89000000,
  45000000, 28000000, 15000000, 8300000, 4800000,
  2100000, 980000, 540000, 320000, 180000,
]
const mockDownloadsData = [
  132100, 98500, 76300, 54200, 42100,
  38900, 28700, 21500, 16800, 12400,
  9800, 7200, 5100, 3800, 2500,
]

const sortedCategories = computed(() => {
  return [...categories.value].sort((a, b) => {
    const indexA = categories.value.indexOf(a)
    const indexB = categories.value.indexOf(b)
    return getCategoryApiCalls(indexB) - getCategoryApiCalls(indexA)
  })
})

onMounted(async () => {
  try {
    loading.value = true
    const response = await getAllCategories()
    categories.value = response.data || []
  } catch (error) {
    console.error('Failed to load categories:', error)
  } finally {
    loading.value = false
  }
})

const handleCategoryClick = (categoryName) =>
  router.push({ name: 'catalog-search', query: { category: categoryName } })

const getCategoryApiCalls = (index) =>
  mockApiCallsData[index] ?? Math.floor(Math.random() * 100000) + 1000
const getCategoryDownloads = (index) =>
  mockDownloadsData[index] ?? Math.floor(Math.random() * 10000) + 100

const formatLargeNumber = (num) => {
  if (!num) return '0'
  if (num >= 1e9) return (num / 1e9).toFixed(1) + 'B'
  if (num >= 1e6) return (num / 1e6).toFixed(1) + 'M'
  if (num >= 1e3) return (num / 1e3).toFixed(1) + 'K'
  return num.toString()
}
</script>

<style scoped>
.categories-page {
  min-height: 100%;
  height: 100%;
  overflow-y: auto;
  background: var(--color-bg-light);
}
.page-header { background: white; padding: 3rem 1rem; border-bottom: 1px solid var(--color-border); }
.container { max-width: 1000px; margin: 0 auto; padding: 0 1rem; }
.page-title { font-size: clamp(28px, 5vw, 40px); font-weight: 700; color: var(--color-text-primary); margin: 0 0 0.5rem; }
.page-subtitle { font-size: 16px; color: var(--color-text-secondary); margin: 0; }

.categories-content { padding: 2rem 1rem 4rem; }
.categories-grid { display: flex; flex-direction: column; gap: 1rem; }
.category-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.5rem;
  background: white;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-base);
}
.category-card:hover { border-color: var(--color-primary); box-shadow: var(--shadow-md); transform: translateX(4px); }
.category-icon-wrapper {
  flex-shrink: 0;
  width: 56px; height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-light);
  border-radius: var(--radius-md);
}
.category-icon { width: 36px; height: 36px; color: var(--color-primary); }
.category-info { flex: 1; min-width: 0; }
.category-name { font-size: 18px; font-weight: 600; color: var(--color-text-primary); margin: 0 0 0.5rem; }
.category-stats { display: flex; gap: 2rem; }
.stat-item { display: flex; align-items: baseline; gap: 0.5rem; }
.stat-value { font-size: 16px; font-weight: 600; color: var(--color-text-primary); }
.stat-label { font-size: 13px; color: var(--color-text-tertiary); }
.category-arrow { flex-shrink: 0; color: var(--color-text-tertiary); transition: all var(--transition-base); }
.category-card:hover .category-arrow { color: var(--color-primary); transform: translateX(4px); }

.loading-grid { display: flex; flex-direction: column; gap: 1rem; }
.category-card-skeleton {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.5rem;
  background: white;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
}
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-sm);
}
.skeleton-icon  { width: 56px; height: 56px; border-radius: var(--radius-md); flex-shrink: 0; }
.skeleton-title { width: 200px; height: 24px; margin-bottom: 0.5rem; }
.skeleton-stats { width: 180px; height: 16px; }
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.empty-state { text-align: center; padding: 4rem 2rem; color: var(--color-text-secondary); }

@media (max-width: 640px) {
  .page-header { padding: 2rem 1rem; }
  .category-card { padding: 1rem; gap: 1rem; }
  .category-icon-wrapper { width: 48px; height: 48px; }
  .category-icon { width: 28px; height: 28px; }
  .category-name { font-size: 16px; }
  .category-stats { flex-direction: column; gap: 0.25rem; }
  .stat-item { gap: 0.25rem; }
  .stat-value { font-size: 14px; }
  .stat-label { font-size: 12px; }
}
</style>
