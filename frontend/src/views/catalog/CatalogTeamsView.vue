<template>
  <div class="catalog-root teams-page">
    <section class="page-header">
      <div class="container">
        <h1 class="page-title">Teams</h1>
        <p class="page-subtitle">
          {{ businessUnits.length }} teams in order of API calls over 6 months
        </p>
      </div>
    </section>

    <section class="teams-content">
      <div class="container">
        <div v-if="loading" class="loading-grid">
          <div v-for="i in 12" :key="`skeleton-${i}`" class="team-card-skeleton">
            <div class="skeleton skeleton-logo"></div>
            <div class="skeleton-info">
              <div class="skeleton skeleton-title"></div>
              <div class="skeleton skeleton-stats"></div>
            </div>
          </div>
        </div>

        <div v-else class="teams-grid">
          <div
            v-for="bu in sortedBusinessUnits"
            :key="bu.id"
            class="team-card"
            @click="handleTeamClick(bu.code)"
          >
            <div class="team-logo-wrapper">
              <img
                v-if="bu.logo_filename"
                :src="getBusinessUnitLogoUrl(bu.id)"
                :alt="bu.name"
                class="team-logo-img"
              />
              <div v-else class="team-logo-placeholder">{{ bu.name.charAt(0) }}</div>
            </div>
            <div class="team-info">
              <h3 class="team-name">{{ bu.name }}</h3>
              <div class="team-stats">
                <div class="stat-item">
                  <span class="stat-value">{{ formatLargeNumber(bu.api_calls) }}</span>
                  <span class="stat-label">API Calls</span>
                </div>
                <div class="stat-item">
                  <span class="stat-value">{{ formatLargeNumber(bu.download_count) }}</span>
                  <span class="stat-label">downloads</span>
                </div>
              </div>
            </div>
            <div class="team-arrow">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
        </div>

        <div v-if="!loading && businessUnits.length === 0" class="empty-state">
          <p>No teams found.</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getBusinessUnits, getBusinessUnitLogoUrl } from '../../utils/catalogApi'

const router = useRouter()
const businessUnits = ref([])
const loading = ref(true)

const sortedBusinessUnits = computed(() =>
  [...businessUnits.value].sort((a, b) => (b.api_calls || 0) - (a.api_calls || 0)),
)

onMounted(async () => {
  try {
    loading.value = true
    const res = await getBusinessUnits()
    businessUnits.value = res.data || []
  } catch (error) {
    console.error('Failed to load business units:', error)
  } finally {
    loading.value = false
  }
})

const handleTeamClick = (teamCode) =>
  router.push({ name: 'catalog-search', query: { team: teamCode } })

const formatLargeNumber = (num) => {
  if (!num) return '0'
  if (num >= 1e9) return (num / 1e9).toFixed(1) + 'B'
  if (num >= 1e6) return (num / 1e6).toFixed(1) + 'M'
  if (num >= 1e3) return (num / 1e3).toFixed(1) + 'K'
  return num.toString()
}
</script>

<style scoped>
.teams-page {
  min-height: 100%;
  height: 100%;
  overflow-y: auto;
  background: var(--color-bg-light);
}
.page-header { background: white; padding: 3rem 1rem; border-bottom: 1px solid var(--color-border); }
.container { max-width: 1000px; margin: 0 auto; padding: 0 1rem; }
.page-title { font-size: clamp(28px, 5vw, 40px); font-weight: 700; color: var(--color-text-primary); margin: 0 0 0.5rem; }
.page-subtitle { font-size: 16px; color: var(--color-text-secondary); margin: 0; }

.teams-content { padding: 2rem 1rem 4rem; }
.teams-grid { display: flex; flex-direction: column; gap: 1rem; }
.team-card {
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
.team-card:hover { border-color: var(--color-primary); box-shadow: var(--shadow-md); transform: translateX(4px); }
.team-logo-wrapper {
  flex-shrink: 0;
  width: 80px; height: 48px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}
.team-logo-img { max-width: 100%; max-height: 100%; object-fit: contain; object-position: left; }
.team-logo-placeholder {
  width: 48px; height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary-light);
  color: var(--color-primary);
  font-size: 20px;
  font-weight: 600;
  border-radius: var(--radius-md);
}
.team-info { flex: 1; min-width: 0; }
.team-name { font-size: 18px; font-weight: 600; color: var(--color-text-primary); margin: 0 0 0.5rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.team-stats { display: flex; gap: 2rem; }
.stat-item { display: flex; align-items: baseline; gap: 0.5rem; }
.stat-value { font-size: 16px; font-weight: 600; color: var(--color-text-primary); }
.stat-label { font-size: 13px; color: var(--color-text-tertiary); }
.team-arrow { flex-shrink: 0; color: var(--color-text-tertiary); transition: all var(--transition-base); }
.team-card:hover .team-arrow { color: var(--color-primary); transform: translateX(4px); }

.loading-grid { display: flex; flex-direction: column; gap: 1rem; }
.team-card-skeleton {
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
.skeleton-logo  { width: 80px; height: 48px; border-radius: var(--radius-md); flex-shrink: 0; }
.skeleton-info  { flex: 1; }
.skeleton-title { width: 200px; height: 24px; margin-bottom: 0.5rem; }
.skeleton-stats { width: 180px; height: 16px; }
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.empty-state { text-align: center; padding: 4rem 2rem; color: var(--color-text-secondary); }

@media (max-width: 640px) {
  .page-header { padding: 2rem 1rem; }
  .team-card { padding: 1rem; gap: 1rem; }
  .team-logo-wrapper { width: 60px; height: 40px; }
  .team-logo-placeholder { width: 40px; height: 40px; font-size: 16px; }
  .team-name { font-size: 16px; }
  .team-stats { flex-direction: column; gap: 0.25rem; }
  .stat-item { gap: 0.25rem; }
  .stat-value { font-size: 14px; }
  .stat-label { font-size: 12px; }
}
</style>
