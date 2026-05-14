<template>
  <div class="data-preview">
    <div class="preview-toolbar">
      <div class="toolbar-left">
        <h3 class="preview-title">Data Preview</h3>
        <span v-if="metadata" class="column-count">
          {{ metadata.columns.length }} columns
          <template v-if="metadata.row_count">
            , {{ formatNumber(metadata.row_count) }} rows
          </template>
        </span>
      </div>
      <div class="toolbar-right">
        <button @click="refreshData" class="btn btn-secondary btn-sm" :disabled="loading">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="23 4 23 10 17 10"/>
            <polyline points="1 20 1 14 7 14"/>
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
          </svg>
          refresh
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-skeleton">
        <div v-for="i in pageSize" :key="i" class="skeleton-row">
          <div class="skeleton-cell" v-for="j in 5" :key="j"></div>
        </div>
      </div>
    </div>

    <div v-else-if="error" class="error-container">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      <p class="error-message">{{ error }}</p>
      <button @click="loadData" class="btn btn-primary btn-sm">Retry</button>
    </div>

    <div v-else class="table-container">
      <table class="preview-table">
        <thead>
          <tr>
            <th v-for="col in columns" :key="col" :title="getColumnType(col)">
              {{ col }}
              <span v-if="getColumnType(col)" class="column-type">{{ getColumnType(col) }}</span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in data" :key="index">
            <td v-for="col in columns" :key="col" :title="formatValue(row[col])">
              {{ formatValue(row[col]) }}
            </td>
          </tr>
          <tr v-if="data.length === 0">
            <td :colspan="columns.length" class="empty-cell">No data available</td>
          </tr>
        </tbody>
      </table>
    </div>

    <Pagination
      v-if="pagination && !loading && !error"
      :current-page="pagination.page"
      :total-pages="pagination.total_pages"
      :total-count="pagination.total_count"
      @page-change="handlePageChange"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { getTableMetadata, previewData } from '../../utils/catalogApi'
import Pagination from './Pagination.vue'

const props = defineProps({
  datasetId: { type: Number, required: true },
})
const emit = defineEmits(['columns-loaded'])

const metadata = ref(null)
const data = ref([])
const columns = ref([])
const pagination = ref(null)
const loading = ref(true)
const error = ref(null)

const currentPage = ref(1)
const pageSize = ref(10)

const columnTypes = computed(() => {
  if (!metadata.value) return {}
  const types = {}
  for (const col of metadata.value.columns) types[col.name] = col.type
  return types
})
const getColumnType = (colName) => columnTypes.value[colName] || ''

const loadMetadata = async () => {
  try {
    const response = await getTableMetadata(props.datasetId)
    metadata.value = response.data
    emit('columns-loaded', metadata.value.columns.map((c) => c.name))
  } catch (err) {
    console.error('Failed to load metadata:', err)
  }
}

const loadData = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await previewData(props.datasetId, {
      page: currentPage.value,
      pageSize: pageSize.value,
    })
    data.value = response.data.data
    columns.value = response.data.columns
    pagination.value = response.data.pagination
  } catch (err) {
    console.error('Failed to load preview data:', err)
    error.value = err.payload?.detail || 'Failed to load data, please try again later'
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  loadData()
}

const refreshData = () => {
  currentPage.value = 1
  loadData()
}

const formatValue = (value) => {
  if (value === null || value === undefined) return '-'
  if (typeof value === 'object') return JSON.stringify(value)
  if (typeof value === 'string' && value.length > 100) return value.substring(0, 100) + '...'
  return String(value)
}
const formatNumber = (num) => new Intl.NumberFormat('en-US').format(num)

watch(() => props.datasetId, () => {
  currentPage.value = 1
  loadMetadata()
  loadData()
})

onMounted(async () => {
  await loadMetadata()
  await loadData()
})
</script>

<style scoped>
.data-preview {
  background: white;
  border: 1px solid #eeeeee;
  border-radius: 12px;
  overflow: hidden;
}
.preview-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #eeeeee;
  background: #f9f9fb;
}
.toolbar-left { display: flex; align-items: center; gap: 1rem; }
.preview-title { margin: 0; font-size: 16px; font-weight: 600; color: #1a1a1a; }
.column-count { font-size: 13px; color: #666666; }
.btn-sm { padding: 0.5rem 1rem; font-size: 13px; }
.btn-sm svg { margin-right: 0.25rem; }

.loading-container { padding: 1rem; }
.loading-skeleton { display: flex; flex-direction: column; gap: 0.75rem; }
.skeleton-row { display: flex; gap: 1rem; }
.skeleton-cell {
  flex: 1;
  height: 20px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
}
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  color: #666666;
}
.error-container svg { color: #ef4444; margin-bottom: 1rem; }
.error-message { margin-bottom: 1rem; text-align: center; }

.table-container { overflow-x: auto; }
.preview-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}
.preview-table th, .preview-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #eeeeee;
  max-width: 250px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.preview-table th {
  background: #f9f9fb;
  font-weight: 600;
  color: #1a1a1a;
  position: sticky;
  top: 0;
  z-index: 10;
}
.preview-table th .column-type {
  display: block;
  font-size: 11px;
  font-weight: 400;
  color: #999999;
  margin-top: 2px;
}
.preview-table tbody tr:hover { background: #fafafa; }
.preview-table td { color: #333333; }
.empty-cell { text-align: center !important; color: #999999; padding: 2rem !important; }

.data-preview :deep(.pagination) {
  padding: 1rem 1.5rem;
  margin-top: 0;
  border-top: none;
}

@media (max-width: 768px) {
  .preview-toolbar { flex-direction: column; gap: 1rem; align-items: flex-start; }
  .preview-table th, .preview-table td { padding: 0.5rem 0.75rem; font-size: 12px; }
}
</style>
