<template>
  <div class="download-wrapper">
    <button @click="toggleDropdown" class="btn btn-primary download-btn" :disabled="downloading">
      <span v-if="downloading" class="download-progress">
        <svg class="spinner" width="16" height="16" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" fill="none" stroke-dasharray="60" stroke-linecap="round"/>
        </svg>
        Downloading...
      </span>
      <span v-else class="download-label">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
          <polyline points="7 10 12 15 17 10"/>
          <line x1="12" y1="15" x2="12" y2="3"/>
        </svg>
        Download Dataset
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="6 9 12 15 18 9"/>
        </svg>
      </span>
    </button>

    <Transition name="dropdown">
      <div v-if="showDropdown" class="download-dropdown">
        <button @click="download('csv')" class="dropdown-item">
          <span class="format-icon csv">CSV</span>
          <div class="format-info">
            <span class="format-name">CSV Format</span>
            <span class="format-desc">Universal table format, best compatibility</span>
          </div>
        </button>
        <button @click="download('xlsx')" class="dropdown-item">
          <span class="format-icon xlsx">XLSX</span>
          <div class="format-info">
            <span class="format-name">Excel Format</span>
            <span class="format-desc">Best for opening and analyzing with Excel</span>
          </div>
        </button>
        <button @click="download('json')" class="dropdown-item">
          <span class="format-icon json">JSON</span>
          <div class="format-info">
            <span class="format-name">JSON Format</span>
            <span class="format-desc">Best for programmatic processing and API integration</span>
          </div>
        </button>
      </div>
    </Transition>

    <div v-if="showDropdown" class="dropdown-overlay" @click="showDropdown = false"></div>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'

const props = defineProps({
  datasetId:     { type: Number, required: true },
  datasetTitle:  { type: String, default: 'dataset' },
  selectedColumns: { type: Array,  default: () => [] },
})

const showDropdown = ref(false)
const downloading  = ref(false)

const toggleDropdown = () => { showDropdown.value = !showDropdown.value }

const download = async (format) => {
  showDropdown.value = false
  downloading.value = true
  try {
    const params = new URLSearchParams()
    params.append('format', format)
    if (props.selectedColumns.length > 0) {
      params.append('columns', props.selectedColumns.join(','))
    }
    const url = `/api/data/datasets/${props.datasetId}/download?${params.toString()}`
    const response = await fetch(url)
    if (!response.ok) throw new Error(`Download failed: ${response.statusText}`)

    const contentDisposition = response.headers.get('Content-Disposition')
    let filename = `${props.datasetTitle}.${format}`
    if (contentDisposition) {
      const match = contentDisposition.match(/filename="?([^";\n]+)"?/)
      if (match) filename = match[1]
    }

    const blob = await response.blob()
    const downloadUrl = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = downloadUrl
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(downloadUrl)
  } catch (error) {
    console.error('Download failed:', error)
    alert('Download failed, please try again later')
  } finally {
    downloading.value = false
  }
}

const handleKeydown = (e) => { if (e.key === 'Escape') showDropdown.value = false }
if (typeof window !== 'undefined') {
  window.addEventListener('keydown', handleKeydown)
  onUnmounted(() => window.removeEventListener('keydown', handleKeydown))
}
</script>

<style scoped>
.download-wrapper { position: relative; }
.download-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.875rem 1.5rem;
  font-size: 15px;
  font-weight: 500;
}
.download-label, .download-progress { display: flex; align-items: center; gap: 0.5rem; }
.spinner { animation: spin 1s linear infinite; }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

.download-dropdown {
  position: absolute;
  top: 100%; left: 0; right: 0;
  margin-top: 0.5rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.12);
  overflow: hidden;
  z-index: 100;
}
.dropdown-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  padding: 1rem;
  border: none;
  background: white;
  text-align: left;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.dropdown-item:hover { background: #f9f9fb; }
.dropdown-item:not(:last-child) { border-bottom: 1px solid #eeeeee; }

.format-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px; height: 48px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
  color: white;
}
.format-icon.csv  { background: linear-gradient(135deg, #10b981, #059669); }
.format-icon.xlsx { background: linear-gradient(135deg, #22c55e, #16a34a); }
.format-icon.json { background: linear-gradient(135deg, #6366f1, #4f46e5); }

.format-info { display: flex; flex-direction: column; gap: 0.25rem; }
.format-name { font-size: 14px; font-weight: 600; color: #1a1a1a; }
.format-desc { font-size: 12px; color: #666666; }

.dropdown-overlay { position: fixed; inset: 0; z-index: 50; }

.dropdown-enter-active, .dropdown-leave-active { transition: all 0.2s ease; }
.dropdown-enter-from, .dropdown-leave-to { opacity: 0; transform: translateY(-8px); }
</style>
