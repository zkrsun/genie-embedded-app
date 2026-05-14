<template>
  <div class="catalog-root search-page">
    <div v-if="!loading && searchResults.length === 0" class="container">
      <div class="no-results">
        <img src="/no-result-theme.svg" alt="No results" class="no-results-icon" />
        <p class="no-results-title">No results found</p>
        <p class="no-results-hint">Check your spelling, expand your search, or use a more generic term.</p>
        <p class="categories-title">How about these categories?</p>
        <div class="categories-section">
          <router-link
            v-for="category in categories"
            :key="category.id"
            :to="`/catalog/search?q=&category=${category.name}`"
            class="category-suggestion"
          >
            <svg class="category-suggestion-icon" :viewBox="getCategoryIconConfig(category.name).viewBox" aria-hidden="true">
              <template v-if="getCategoryIconConfig(category.name).paths">
                <path
                  v-for="(p, idx) in getCategoryIconConfig(category.name).paths"
                  :key="idx"
                  :d="p.d"
                  :fill="p.fill || 'currentColor'"
                />
              </template>
              <path v-else :d="getCategoryIconConfig(category.name).path" fill="currentColor"/>
            </svg>
            <span>{{ category.name }}</span>
          </router-link>
        </div>
      </div>
    </div>

    <div v-else class="search-layout" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <!-- Left: dataset list -->
      <aside class="datasets-sidebar">
        <div class="sidebar-header">
          <div class="sidebar-header-content">
            <h2 v-if="searchQuery">Results for "{{ searchQuery }}"</h2>
            <h2 v-else>All Datasets</h2>
            <span class="result-count">{{ totalResults }} datasets</span>
          </div>
          <button
            class="sidebar-toggle-btn"
            @click="toggleSidebar"
            :aria-label="isSidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
            type="button"
          >
            <svg :class="{ rotated: isSidebarCollapsed }" width="16" height="16" viewBox="0 0 24 24" fill="none">
              <path d="M15 18l-6-6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span class="toggle-label">{{ isSidebarCollapsed ? 'Expand' : 'Collapse' }}</span>
          </button>
        </div>

        <div v-if="loading" class="loading-list">
          <div class="loading-spinner"></div>
        </div>

        <div v-else class="datasets-list">
          <div
            v-for="dataset in searchResults"
            :key="dataset.id"
            class="dataset-item"
            :class="{ active: selectedDataset?.id === dataset.id }"
            @click="selectDataset(dataset)"
          >
            <div class="item-header">
              <h3>{{ dataset.title }}</h3>
              <span class="category-tag">{{ dataset.category.name }}</span>
            </div>
            <p class="item-description">{{ dataset.description }}</p>
            <div class="item-meta">
              <span>{{ formatDate(dataset.updated_at) }}</span>
              <span>{{ formatNumber(dataset.row_count) }} rows</span>
            </div>
          </div>
        </div>
      </aside>

      <!-- Right: detail -->
      <main class="detail-content">
        <div v-if="!selectedDataset && !loading" class="empty-detail">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
          </svg>
          <p>Select a dataset to view details</p>
        </div>

        <div v-else-if="selectedDataset" class="detail-view">
          <div class="detail-header">
            <div class="header-info">
              <div class="breadcrumb">
                <span class="category-badge">
                  <svg class="category-icon" :viewBox="getCategoryIconConfig(selectedDataset.category.name).viewBox">
                    <template v-if="getCategoryIconConfig(selectedDataset.category.name).paths">
                      <path
                        v-for="(p, idx) in getCategoryIconConfig(selectedDataset.category.name).paths"
                        :key="idx"
                        :d="p.d"
                        :fill="p.fill || 'currentColor'"
                      />
                    </template>
                    <path v-else :d="getCategoryIconConfig(selectedDataset.category.name).path" fill="currentColor"/>
                  </svg>
                  {{ selectedDataset.category.name }}
                </span>
                <span class="separator">·</span>
                <span class="update-time">Updated {{ formatDate(selectedDataset.updated_at) }}</span>
              </div>
              <h1>{{ selectedDataset.title }}</h1>
            </div>
            <div class="header-actions">
              <DownloadButton
                :dataset-id="selectedDataset.id"
                :dataset-title="selectedDataset.title"
              />
            </div>
          </div>

          <div class="detail-section description-section">
            <p>{{ selectedDataset.description }}</p>
          </div>

          <div class="stats-bar">
            <div class="stat">
              <span class="stat-value">{{ formatNumber(selectedDataset.row_count) }}</span>
              <span class="stat-label">Rows</span>
            </div>
            <div class="stat">
              <span class="stat-value">{{ formatNumber(selectedDataset.col_count) }}</span>
              <span class="stat-label">Columns</span>
            </div>
            <div class="stat">
              <span class="stat-value">{{ formatNumber(selectedDataset.download_count) }}</span>
              <span class="stat-label">Downloads</span>
            </div>
          </div>

          <div class="detail-section">
            <div class="section-header">
              <h2>Data Explorer</h2>
            </div>
            <div class="data-explorer">
              <DataPreview
                :dataset-id="selectedDataset.id"
                :key="selectedDataset.id"
                @columns-loaded="handleColumnsLoaded"
              />
            </div>
          </div>

          <div class="detail-section">
            <div class="section-header">
              <h2>Column Legend</h2>
            </div>
            <div class="column-legend">
              <div v-if="datasetColumns.length === 0" class="no-columns">
                Loading column information...
              </div>
              <table v-else class="legend-table">
                <thead>
                  <tr>
                    <th>Column Name</th>
                    <th>Type</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="column in datasetColumns" :key="column.name">
                    <td class="column-name">{{ column.name }}</td>
                    <td class="column-type">
                      <span class="type-badge">{{ column.type }}</span>
                    </td>
                    <td class="column-desc">{{ column.description || '-' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div v-if="selectedDataset.tags" class="detail-section">
            <div class="section-header">
              <h2>Tags</h2>
            </div>
            <div class="tags-list">
              <span v-for="tag in selectedDataset.tags.split(',')" :key="tag" class="tag">
                {{ tag.trim() }}
              </span>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { searchDatasets, getAllCategories } from '../../utils/catalogApi'
import { getCategoryIconConfig } from '../../config/categoryConfig'
import DataPreview    from '../../components/catalog/DataPreview.vue'
import DownloadButton from '../../components/catalog/DownloadButton.vue'

const route = useRoute()

const searchResults = ref([])
const totalResults  = ref(0)
const loading       = ref(false)
const isSidebarCollapsed = ref(false)
const selectedDataset = ref(null)
const datasetColumns  = ref([])
const categories      = ref([])

const searchQuery = computed(() => route.query.q || '')

const fetchCategories = async () => {
  try {
    const res = await getAllCategories()
    categories.value = res.data || []
  } catch (error) {
    console.error('Failed to fetch categories:', error)
  }
}

const getFiltersFromUrl = () => {
  const parsePipeSeparated = (param) => {
    if (!param) return undefined
    if (Array.isArray(param)) return param.join('|').split('|').filter(Boolean)
    return param.split('|').filter(Boolean)
  }
  return {
    category: parsePipeSeparated(route.query.category),
    team:     parsePipeSeparated(route.query.team),
    topic:    parsePipeSeparated(route.query.topic),
  }
}

const selectDataset = (dataset) => {
  selectedDataset.value = dataset
  if (dataset.column_descriptions && Array.isArray(dataset.column_descriptions)) {
    datasetColumns.value = dataset.column_descriptions.map((col) => ({
      name: col.name,
      type: col.type || 'unknown',
      description: col.description || '',
    }))
  } else {
    datasetColumns.value = []
  }
}

const handleColumnsLoaded = (columns) => {
  if (datasetColumns.value.length === 0 && columns.length > 0) {
    datasetColumns.value = columns.map((name) => ({ name, type: 'string', description: '' }))
  }
}

const toggleSidebar = () => { isSidebarCollapsed.value = !isSidebarCollapsed.value }

const performSearch = async () => {
  loading.value = true
  selectedDataset.value = null
  datasetColumns.value = []
  try {
    const filters = getFiltersFromUrl()
    const res = await searchDatasets(searchQuery.value, filters)
    searchResults.value = res.data.datasets
    totalResults.value  = res.data.total
    if (searchResults.value.length > 0) selectDataset(searchResults.value[0])
  } catch (error) {
    console.error('Search failed:', error)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateStr) =>
  new Date(dateStr).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
const formatNumber = (num) => num ? new Intl.NumberFormat('en-US').format(num) : '0'

watch(() => route.query, () => { performSearch() }, { immediate: true, deep: true })
onMounted(() => { fetchCategories() })
</script>

<style scoped>
.search-page {
  height: 100%;
  background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
  overflow-y: auto;
}

.container { max-width: 1200px; margin: 0 auto; padding: 2rem; }

.no-results-icon { width: 180px; height: auto; margin-bottom: 1.5rem; }
.no-results {
  text-align: center;
  padding: 2.5rem 1.5rem 4rem;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-radius: 16px;
  box-shadow: 0 16px 32px rgba(15, 23, 42, 0.12);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  animation: float-in 0.4s ease both;
}
.no-results-title { font-size: 1.5rem; font-weight: 600; color: #0f172a; margin-bottom: 0.5rem; }
.no-results-hint { font-size: 0.875rem; font-weight: 500; color: #64748b; }
.categories-title { font-size: 1rem; font-weight: 500; color: #0f172a; margin: 3rem 0 1rem; }
.categories-section { display: flex; flex-wrap: wrap; justify-content: center; gap: 0.75rem; max-width: 800px; margin: 0 auto; }
.category-suggestion {
  padding: 0.625rem 1.25rem;
  border-radius: var(--radius-full, 9999px);
  border: 1px solid rgba(255, 255, 255, 0.6);
  background: rgba(255, 255, 255, 0.7);
  color: #0f172a;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
  text-decoration: none;
}
.category-suggestion-icon { width: 20px; height: 20px; flex-shrink: 0; }
.category-suggestion:hover {
  background: rgba(240, 247, 255, 0.9);
  border-color: rgba(91, 194, 220, 0.4);
  color: var(--color-primary);
  transform: translateY(-2px);
}

.search-layout { display: flex; min-height: 100%; }

.datasets-sidebar {
  width: 360px;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.7);
  border-right: 1px solid rgba(255, 255, 255, 0.6);
  display: flex;
  flex-direction: column;
  height: 100%;
  position: sticky;
  top: 0;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  transition: width 0.25s ease;
  overflow: hidden;
}
.sidebar-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}
.sidebar-header-content { display: flex; flex-direction: column; gap: 0.15rem; transition: opacity 0.2s ease; }
.sidebar-toggle-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.6rem;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.6);
  background: rgba(255, 255, 255, 0.6);
  color: #0f172a;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.08);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  transition: all 0.2s ease;
}
.sidebar-toggle-btn:hover { box-shadow: 0 12px 22px rgba(15, 23, 42, 0.12); transform: translateY(-1px); }
.sidebar-toggle-btn svg { transition: transform 0.2s ease; }
.sidebar-toggle-btn svg.rotated { transform: rotate(180deg); }
.sidebar-toggle-btn .toggle-label { white-space: nowrap; }

.search-layout.sidebar-collapsed .datasets-sidebar { width: 72px; }
.search-layout.sidebar-collapsed .sidebar-header-content { opacity: 0; pointer-events: none; width: 0; overflow: hidden; }
.search-layout.sidebar-collapsed .sidebar-toggle-btn .toggle-label { display: none; }
.search-layout.sidebar-collapsed .sidebar-header { justify-content: center; }
.search-layout.sidebar-collapsed .datasets-list { opacity: 0; transform: translateX(-8px); pointer-events: none; }

.sidebar-header h2 { font-size: 16px; font-weight: 600; margin: 0 0 0.25rem; color: #0f172a; }
.result-count { font-size: 13px; color: #64748b; }

.datasets-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.75rem;
  transition: opacity 0.2s ease, transform 0.2s ease;
  will-change: opacity, transform;
}
.dataset-item {
  padding: 1rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  background: rgba(255, 255, 255, 0.7);
  box-shadow: 0 10px 20px rgba(15, 23, 42, 0.08);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  animation: float-in 0.35s ease both;
  margin-bottom: 0.25rem;
}
.dataset-item:hover {
  background: rgba(255, 255, 255, 0.8);
  border-color: rgba(91, 194, 220, 0.25);
  box-shadow: 0 10px 22px rgba(15, 23, 42, 0.08);
}
.dataset-item.active {
  background: rgba(91, 194, 220, 0.18);
  border: 1px solid rgba(91, 194, 220, 0.35);
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.12);
}

.item-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 0.75rem; margin-bottom: 0.5rem; }
.item-header h3 { font-size: 14px; font-weight: 600; margin: 0; color: var(--color-text-primary); line-height: 1.4; }

.category-tag {
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.7);
  color: #475569;
  border: 1px solid rgba(148, 163, 184, 0.3);
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}
.item-description {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin: 0 0 0.5rem;
  line-height: 1.5;
  display: -webkit-box;
  line-clamp: 2;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.item-meta { display: flex; gap: 1rem; font-size: 12px; color: var(--color-text-tertiary); }

.loading-list { display: flex; justify-content: center; padding: 3rem; }
.loading-spinner {
  width: 32px; height: 32px;
  border: 3px solid #eee;
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.detail-content { flex: 1; overflow-y: auto; min-height: 100%; background: transparent; }
.empty-detail {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 400px;
  color: var(--color-text-tertiary);
}
.empty-detail svg { opacity: 0.3; margin-bottom: 1rem; }
.empty-detail p { font-size: 14px; margin: 0; }

.detail-view { padding: 2rem; max-width: 1200px; margin: 0 auto; animation: float-in 0.35s ease both; }
.detail-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 2rem; margin-bottom: 1.5rem; }
.header-info { flex: 1; }
.breadcrumb { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.75rem; }
.category-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: white;
  color: var(--color-text-primary);
  padding: 0.5rem 1rem;
  border-radius: var(--radius-full);
  border: 1px solid var(--color-border);
  font-size: 14px;
  font-weight: 550;
}
.category-badge .category-icon { width: 20px; height: 20px; flex-shrink: 0; }
.separator { color: var(--color-text-tertiary); }
.update-time { font-size: 13px; color: var(--color-text-tertiary); }
.detail-header h1 { font-size: 28px; font-weight: 700; margin: 0; color: #0f172a; line-height: 1.3; }
.header-actions { flex-shrink: 0; }
.description-section p { font-size: 15px; color: #475569; line-height: 1.7; margin: 0; }

.stats-bar {
  display: flex;
  gap: 2rem;
  padding: 1.25rem 1.5rem;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-radius: 12px;
  margin: 1.5rem 0;
  box-shadow: 0 14px 28px rgba(15, 23, 42, 0.12);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
}
.stat { display: flex; flex-direction: column; }
.stat-value { font-size: 20px; font-weight: 600; color: #0f172a; }
.stat-label { font-size: 12px; color: #64748b; margin-top: 0.25rem; }

.detail-section { margin-top: 2rem; }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.section-header h2 { font-size: 18px; font-weight: 600; margin: 0; color: #0f172a; }

.data-explorer, .column-legend {
  background: rgba(255, 255, 255, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.1);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
}
.data-explorer :deep(.data-preview) { border: none; border-radius: 0; }
.no-columns { padding: 2rem; text-align: center; color: #64748b; font-size: 14px; }

.legend-table { width: 100%; border-collapse: collapse; }
.legend-table th, .legend-table td {
  padding: 0.875rem 1rem;
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}
.legend-table th {
  background: rgba(255, 255, 255, 0.8);
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.legend-table tr:last-child td { border-bottom: none; }
.legend-table tr:hover td { background: rgba(255, 255, 255, 0.85); }
.column-name {
  font-family: 'SF Mono', Monaco, 'Courier New', monospace;
  font-size: 13px;
  font-weight: 500;
  color: #0f172a;
}
.column-type { width: 120px; }
.type-badge {
  display: inline-block;
  background: rgba(91, 194, 220, 0.18);
  color: #0f172a;
  border: 1px solid rgba(91, 194, 220, 0.3);
  padding: 0.25rem 0.625rem;
  border-radius: 4px;
  font-family: 'SF Mono', Monaco, 'Courier New', monospace;
  font-size: 12px;
}
.column-desc { font-size: 13px; color: #475569; }

.tags-list { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.tag {
  background: rgba(255, 255, 255, 0.75);
  color: #475569;
  border: 1px solid rgba(148, 163, 184, 0.3);
  padding: 0.375rem 0.875rem;
  border-radius: 999px;
  font-size: 12px;
}

@keyframes float-in {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
  .dataset-item, .detail-view, .no-results { animation: none; }
}

@media (max-width: 1024px) {
  .search-layout { flex-direction: column; }
  .datasets-sidebar { width: 100%; height: auto; max-height: 40vh; position: static; border-right: none; border-bottom: 1px solid var(--color-border); }
  .detail-view { padding: 1.5rem; }
  .stats-bar { flex-wrap: wrap; gap: 1rem; }
}
@media (max-width: 640px) {
  .detail-header { flex-direction: column; gap: 1rem; }
  .header-actions { width: 100%; }
  .detail-header h1 { font-size: 22px; }
}
</style>
