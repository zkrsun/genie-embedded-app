<template>
  <div class="catalog-root detail-page">
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>Loading...</p>
    </div>

    <div v-else-if="dataset" class="dataset-detail">
      <div class="detail-header">
        <div class="header-left">
          <router-link to="/catalog" class="back-link">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="19" y1="12" x2="5" y2="12"/>
              <polyline points="12 19 5 12 12 5"/>
            </svg>
            Back to Catalog
          </router-link>
          <h1>{{ dataset.title }}</h1>
          <div class="dataset-meta">
            <span class="category-badge">{{ dataset.category.name }}</span>
            <span class="update-time">Updated {{ formatDate(dataset.updated_at) }}</span>
          </div>
        </div>
      </div>

      <div class="detail-container">
        <div class="detail-main">
          <section class="section">
            <h2>Description</h2>
            <p class="description">{{ dataset.description }}</p>
          </section>

          <section class="section preview-section" ref="previewSection">
            <DataPreview
              :dataset-id="Number(route.params.id)"
              @columns-loaded="handleColumnsLoaded"
            />
          </section>

          <section class="section">
            <h2>Statistics</h2>
            <div class="stats-grid">
              <div class="stat-item">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="12" y1="20" x2="12" y2="10"/>
                  <line x1="18" y1="20" x2="18" y2="4"/>
                  <line x1="6" y1="20" x2="6" y2="16"/>
                </svg>
                <span class="stat-label">Rows</span>
                <span class="stat-value">{{ formatNumber(dataset.row_count) }}</span>
              </div>
              <div class="stat-item">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                  <line x1="9" y1="3" x2="9" y2="21"/>
                  <line x1="15" y1="3" x2="15" y2="21"/>
                </svg>
                <span class="stat-label">Columns</span>
                <span class="stat-value">{{ formatNumber(dataset.col_count) }}</span>
              </div>
              <div class="stat-item">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="7 10 12 15 17 10"/>
                  <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
                <span class="stat-label">Downloads</span>
                <span class="stat-value">{{ formatNumber(dataset.download_count) }}</span>
              </div>
            </div>
          </section>

          <section class="section">
            <h2>Metadata</h2>
            <table class="metadata-table">
              <tbody>
                <tr><td class="label">Dataset ID</td><td>{{ dataset.id }}</td></tr>
                <tr><td class="label">Category</td><td>{{ dataset.category.name }}</td></tr>
                <tr><td class="label">Created</td><td>{{ formatDateTime(dataset.created_at) }}</td></tr>
                <tr><td class="label">Updated</td><td>{{ formatDateTime(dataset.updated_at) }}</td></tr>
                <tr v-if="dataset.tags">
                  <td class="label">Tags</td>
                  <td>
                    <span v-for="tag in dataset.tags.split(',')" :key="tag" class="tag">
                      {{ tag.trim() }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </section>
        </div>

        <div class="detail-sidebar">
          <div class="sidebar-card">
            <h3>Download Data</h3>
            <p class="sidebar-desc">Available in CSV, Excel, JSON formats</p>
            <DownloadButton
              :dataset-id="Number(route.params.id)"
              :dataset-title="dataset.title"
              :selected-columns="selectedColumns"
            />
          </div>

          <div class="sidebar-card">
            <h3>Quick Navigation</h3>
            <button @click="scrollToPreview" class="btn btn-secondary btn-block">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
              View Data Preview
            </button>
          </div>

          <div class="sidebar-card info-card">
            <h3>Instructions</h3>
            <ul class="info-list">
              <li>Data preview shows the first 10 records by default</li>
              <li>Use pagination to view more data</li>
              <li>Download available in CSV, Excel, JSON formats</li>
              <li>Excel format supports up to 100,000 rows</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="not-found">
      <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      <h2>Dataset Not Found</h2>
      <p>Please check the URL or go back to browse other datasets</p>
      <router-link to="/catalog" class="btn btn-primary">Back to Catalog</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getDatasetDetail } from '../../utils/catalogApi'
import DataPreview    from '../../components/catalog/DataPreview.vue'
import DownloadButton from '../../components/catalog/DownloadButton.vue'

const route = useRoute()
const dataset = ref(null)
const loading = ref(true)
const selectedColumns = ref([])
const previewSection = ref(null)

onMounted(async () => {
  try {
    const res = await getDatasetDetail(route.params.id)
    dataset.value = res.data
  } catch (error) {
    console.error('Failed to load dataset:', error)
  } finally {
    loading.value = false
  }
})

const handleColumnsLoaded = (columns) => { selectedColumns.value = columns }

const scrollToPreview = () => {
  if (previewSection.value) previewSection.value.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const formatDate = (dateStr) =>
  new Date(dateStr).toLocaleDateString('en-US', { year: 'numeric', month: '2-digit', day: '2-digit' })
const formatDateTime = (dateStr) =>
  new Date(dateStr).toLocaleString('en-US', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
const formatNumber = (num) => num ? new Intl.NumberFormat('en-US').format(num) : '0'
</script>

<style scoped>
.detail-page {
  min-height: 100%;
  height: 100%;
  overflow-y: auto;
  padding: 2rem;
  background: #f9f9fb;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 6rem 2rem;
  color: #666666;
}
.loading-spinner {
  width: 40px; height: 40px;
  border: 3px solid #eeeeee;
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}
@keyframes spin { to { transform: rotate(360deg); } }

.detail-header { max-width: 1400px; margin: 0 auto 2rem; }
.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #666666;
  text-decoration: none;
  font-size: 14px;
  margin-bottom: 1rem;
  transition: color 0.2s;
}
.back-link:hover { color: var(--color-primary); }
.detail-header h1 { margin: 0 0 0.75rem; font-size: 32px; font-weight: 700; color: #1a1a1a; }
.dataset-meta { display: flex; align-items: center; gap: 1rem; }
.category-badge {
  display: inline-block;
  background: var(--color-primary);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
}
.update-time { color: #666666; font-size: 14px; }

.detail-container {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}
.detail-main { display: flex; flex-direction: column; gap: 1.5rem; }

.section { background: white; border: 1px solid #eeeeee; border-radius: 12px; padding: 1.5rem; }
.section h2 { margin: 0 0 1rem; font-size: 18px; font-weight: 600; color: #1a1a1a; }
.description { color: #333333; line-height: 1.7; margin: 0; }

.preview-section { padding: 0; overflow: hidden; }
.preview-section :deep(.data-preview) { border: none; border-radius: 0; }

.stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  background: #f9f9fb;
  padding: 1.25rem;
  border-radius: 8px;
  text-align: center;
}
.stat-item svg { color: var(--color-primary); }
.stat-label { font-size: 13px; color: #666666; }
.stat-value { font-size: 20px; font-weight: 600; color: #1a1a1a; }

.metadata-table { width: 100%; border-collapse: collapse; }
.metadata-table tr { border-bottom: 1px solid #eeeeee; }
.metadata-table tr:last-child { border-bottom: none; }
.metadata-table td { padding: 0.875rem 0; }
.metadata-table .label { font-weight: 500; color: #666666; width: 120px; }

.tag {
  display: inline-block;
  background: #f0f0f0;
  color: #666666;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  margin-right: 0.5rem;
  margin-bottom: 0.25rem;
  font-size: 13px;
}

.detail-sidebar { display: flex; flex-direction: column; gap: 1.5rem; }
.sidebar-card { background: white; border: 1px solid #eeeeee; border-radius: 12px; padding: 1.5rem; }
.sidebar-card h3 { margin: 0 0 0.5rem; font-size: 16px; font-weight: 600; color: #1a1a1a; }
.sidebar-desc { margin: 0 0 1rem; font-size: 13px; color: #666666; }
.btn-block { display: flex; align-items: center; justify-content: center; gap: 0.5rem; width: 100%; }
.btn { padding: 0.75rem 1.5rem; border-radius: 8px; border: none; font-size: 15px; font-weight: 500; cursor: pointer; }
.btn-primary { background: var(--color-primary); color: #fff; }
.btn-secondary { background: var(--color-secondary); color: #fff; }
.info-card { background: #f9f9fb; border: 1px dashed #dddddd; }
.info-list { margin: 0; padding: 0 0 0 1.25rem; font-size: 13px; color: #666666; line-height: 1.8; }

.not-found {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 6rem 2rem;
  text-align: center;
}
.not-found svg { color: #cccccc; margin-bottom: 1.5rem; }
.not-found h2 { margin: 0 0 0.5rem; font-size: 24px; color: #1a1a1a; }
.not-found p { margin: 0 0 1.5rem; color: #666666; }

@media (max-width: 1024px) {
  .detail-container { grid-template-columns: 1fr; }
  .detail-sidebar { order: -1; flex-direction: row; flex-wrap: wrap; }
  .sidebar-card { flex: 1; min-width: 250px; }
}
@media (max-width: 768px) {
  .detail-page { padding: 1rem; }
  .detail-header h1 { font-size: 24px; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .sidebar-card { min-width: 100%; }
}
</style>
