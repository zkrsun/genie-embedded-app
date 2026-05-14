// Catalog API surface — talks to /api/* served by backend/routers/catalog/*.
// Lightweight fetch wrapper (no axios) to avoid extra deps.

const BASE = '/api'

async function request(path, { method = 'GET', params, body, signal } = {}) {
  const url = new URL(BASE + path, window.location.origin)
  if (params) {
    for (const [k, v] of Object.entries(params)) {
      if (v === undefined || v === null) continue
      if (Array.isArray(v)) {
        for (const item of v) url.searchParams.append(k, item)
      } else {
        url.searchParams.append(k, v)
      }
    }
  }

  const res = await fetch(url, {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : undefined,
    body: body ? JSON.stringify(body) : undefined,
    signal,
  })
  if (!res.ok) {
    const err = new Error(`HTTP ${res.status}`)
    err.status = res.status
    try { err.payload = await res.json() } catch {}
    throw err
  }
  // axios-shaped response so the copied pages keep working: { data }
  return { data: await res.json() }
}

// ── Catalog reads ──────────────────────────────────────────────────────
export const getAllCategories  = () => request('/categories')
export const getBusinessUnits  = () => request('/business-units')
export const getPopularDatasets = (limit = 10) => request('/datasets/popular', { params: { limit } })
export const getDatasetDetail  = (id) => request(`/datasets/${id}`)

export const searchDatasets = (query, filters = {}) =>
  request('/search', { params: { q: query || '', ...filters } })

// ── BU logo (returns URL, not data) ─────────────────────────────────────
export const getBusinessUnitLogoUrl = (buId) => `${BASE}/business-units/${buId}/logo`

// ── Data access ─────────────────────────────────────────────────────────
export const getTableMetadata = (datasetId) =>
  request(`/data/datasets/${datasetId}/metadata`)

export const previewData = (datasetId, { page = 1, pageSize = 10, columns = null } = {}) =>
  request(`/data/datasets/${datasetId}/preview`, {
    params: {
      page,
      page_size: pageSize,
      columns: columns ? columns.join(',') : undefined,
    },
  })

export const getDownloadUrl = (datasetId, format = 'csv', columns = null) => {
  const params = new URLSearchParams()
  params.append('format', format)
  if (columns && columns.length) params.append('columns', columns.join(','))
  return `${BASE}/data/datasets/${datasetId}/download?${params}`
}

export default {
  getAllCategories,
  getBusinessUnits,
  getPopularDatasets,
  getDatasetDetail,
  searchDatasets,
  getBusinessUnitLogoUrl,
  getTableMetadata,
  previewData,
  getDownloadUrl,
}
