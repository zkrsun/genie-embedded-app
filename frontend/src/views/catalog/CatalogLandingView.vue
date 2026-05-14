<template>
  <div class="catalog-root landing-page">
    <!-- Hero Section -->
    <section class="hero fade-in">
      <div class="bubbles-container" aria-hidden="true">
        <div class="bubble"></div><div class="bubble"></div><div class="bubble"></div>
        <div class="bubble"></div><div class="bubble"></div><div class="bubble"></div>
        <div class="bubble"></div><div class="bubble"></div><div class="bubble"></div>
        <div class="bubble"></div>
      </div>
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="title-main">Suntory's</span>
          <span class="title-sub">open data center</span>
        </h1>
        <p class="hero-subtitle">Explore company datasets and Power BI.</p>

        <div class="search-box-wrapper">
          <div class="search-input-group">
            <input
              type="text"
              v-model="searchQuery"
              @keyup.enter="handleSearch"
              @keydown.esc="searchQuery = ''"
              placeholder="Try keywords like: SELLIN, SELLOUT, RMS"
              class="search-input"
              aria-label="Search datasets"
            />
            <button v-if="searchQuery" @click="searchQuery = ''" class="search-clear-btn" aria-label="Clear search" type="button">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
            <button @click="handleSearch" class="search-btn-icon" aria-label="click to search" :disabled="!hasSearchQuery">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M9 17A8 8 0 1 0 9 1a8 8 0 0 0 0 16zM18.707 17.293l-3.675-3.675a7 7 0 1 0-1.414 1.414l3.675 3.675a1 1 0 0 0 1.414-1.414z" fill="currentColor"/>
              </svg>
            </button>
          </div>
        </div>

        <div class="categories-section">
          <div class="categories-grid" role="list">
            <button
              v-for="category in categories"
              :key="category.id"
              @click="handleCategoryClick(category.name)"
              class="category-tag"
              role="listitem"
              :aria-label="`Browse ${category.name} datasets`"
              type="button"
            >
              <svg class="category-icon" :viewBox="getCategoryIconConfig(category.name).viewBox" aria-hidden="true">
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
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section">
      <div class="container">
        <div class="stats-banner">
          <h2 class="stats-title">
            <span class="stats-number">{{ totalDatasets }}+</span>
            <span class="stats-label">datasets from</span>
            <span class="stats-number">{{ totalCategories }}+</span>
            <span class="stats-label">categories</span>
          </h2>
        </div>

        <div class="agencies-section" v-if="categories.length > 0">
          <div class="agencies-grid">
            <div
              v-for="(category, index) in categories.slice(0, 6)"
              :key="category.id"
              class="agency-card"
              @click="handleCategoryClick(category.name)"
            >
              <svg class="agency-icon" :viewBox="getCategoryIconConfig(category.name).viewBox" aria-hidden="true">
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
              <div class="agency-name">{{ category.name }}</div>
              <div class="agency-stats">
                <span class="agency-stat-item">
                  <span class="stat-value data-value">{{ formatLargeNumber(getMockApiCalls(index)) }}</span>
                  <span class="stat-label-small">API Calls</span>
                </span>
                <span class="agency-stat-item">
                  <span class="stat-value data-value">{{ formatLargeNumber(getMockDownloads(index)) }}</span>
                  <span class="stat-label-small">downloads</span>
                </span>
              </div>
            </div>
          </div>
          <div class="view-all-agencies">
            <router-link to="/catalog/categories" class="view-all-link">View all categories →</router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Trusted By Section -->
    <section class="trusted-section" v-if="businessUnits.length > 0">
      <div class="container">
        <h3 class="trusted-title">Trusted everyday by teams at</h3>
        <div class="bu-cards-grid">
          <div
            v-for="bu in businessUnits.slice(0, 8)"
            :key="bu.id"
            class="bu-card"
            :title="bu.name"
            @click="handleTeamClick(bu.code)"
          >
            <div class="bu-logo-wrapper">
              <img
                v-if="bu.logo_filename"
                :src="getBusinessUnitLogoUrl(bu.id)"
                :alt="bu.name"
                class="bu-logo-img"
              />
            </div>
            <span class="bu-name">{{ bu.name }}</span>
            <div class="bu-stats">
              <span class="bu-stat-item">{{ formatLargeNumber(bu.api_calls) }} API Calls</span>
              <span class="bu-stat-item">{{ formatLargeNumber(bu.download_count) }} downloads</span>
            </div>
          </div>
        </div>
        <div class="view-all-agencies">
          <router-link to="/catalog/teams" class="view-all-link">View all teams →</router-link>
        </div>
      </div>
    </section>

    <!-- Popular Datasets Section -->
    <section class="featured-datasets">
      <div class="container">
        <div class="section-header">
          <h2>Our most used datasets</h2>
        </div>

        <div v-if="popularDatasets.length === 0" class="loading-skeleton">
          <div v-for="i in 6" :key="`skeleton-${i}`" class="dataset-card-skeleton">
            <div class="skeleton skeleton-title"></div>
            <div class="skeleton skeleton-text" style="width: 100%;"></div>
            <div class="skeleton skeleton-text" style="width: 80%;"></div>
            <div class="skeleton skeleton-text" style="width: 40%;"></div>
          </div>
        </div>
        <div v-else class="datasets-grid">
          <article
            v-for="dataset in popularDatasets"
            :key="dataset.id"
            class="dataset-card fade-in"
            @click="openDataset(dataset.id)"
          >
            <div class="dataset-header">
              <h3>{{ dataset.title }}</h3>
              <span class="category-badge">{{ dataset.category.name }}</span>
            </div>
            <p class="dataset-description">{{ dataset.description }}</p>
            <div class="dataset-stats">
              <div class="stat-item">
                <span class="stat-label">Rows</span>
                <span class="stat-value data-value">{{ formatNumber(dataset.row_count) }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Downloads</span>
                <span class="stat-value data-value">{{ formatNumber(dataset.download_count) }}</span>
              </div>
            </div>
          </article>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getPopularDatasets, getAllCategories, getBusinessUnits, getBusinessUnitLogoUrl } from '../../utils/catalogApi'
import { getCategoryIconConfig } from '../../config/categoryConfig'

const router = useRouter()
const searchQuery = ref('')
const popularDatasets = ref([])
const categories = ref([])
const businessUnits = ref([])

const hasSearchQuery = computed(() => searchQuery.value.trim().length > 0)
const totalDatasets = computed(() => popularDatasets.value.length > 0 ? 500 : 0)
const totalCategories = computed(() => categories.value.length)

onMounted(async () => {
  try {
    const [d, c, b] = await Promise.all([
      getPopularDatasets(),
      getAllCategories(),
      getBusinessUnits(),
    ])
    popularDatasets.value = d.data || []
    categories.value = c.data || []
    businessUnits.value = b.data || []
  } catch (error) {
    console.error('Failed to load data:', error)
  }
})

const handleSearch = () => {
  if (!hasSearchQuery.value) return
  router.push({ name: 'catalog-search', query: { q: searchQuery.value.trim() } })
}
const handleCategoryClick = (categoryName) =>
  router.push({ name: 'catalog-search', query: { category: categoryName } })
const handleTeamClick = (teamCode) =>
  router.push({ name: 'catalog-search', query: { team: teamCode } })
const openDataset = (id) =>
  router.push({ name: 'catalog-dataset-detail', params: { id } })

const formatNumber = (num) => num ? num.toLocaleString('en-US') : '0'
const formatLargeNumber = (num) => {
  if (!num) return '0'
  if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B'
  if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M'
  if (num >= 1e3) return (num / 1e3).toFixed(1) + 'K'
  return num.toString()
}
const getMockApiCalls = (index) => {
  const calls = [840300000, 8300000, 4800000, 121900, 64800, 744]
  return calls[index] || 1000
}
const getMockDownloads = (index) => {
  const downloads = [132100, 36600, 110200, 38900, 3800, 2000]
  return downloads[index] || 100
}
</script>

<style scoped>
.landing-page {
  min-height: 100%;
  background: var(--color-bg-light);
  overflow-y: auto;
  height: 100%;
}

/* Hero */
.hero {
  background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 50%, #f0f9ff 100%);
  color: var(--color-text-primary);
  padding: 4rem 1rem 3rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.bubbles-container { position: absolute; inset: 0; overflow: hidden; pointer-events: none; z-index: 0; }
.bubble { position: absolute; bottom: -100px; border-radius: 50%; opacity: 0.6; animation: float-up linear infinite; }
.bubble:nth-child(1)  { width: 40px; height: 40px; left: 10%; background: linear-gradient(135deg, rgba(99,102,241,0.3), rgba(139,92,246,0.2));  animation-duration: 18s; }
.bubble:nth-child(2)  { width: 20px; height: 20px; left: 20%; background: linear-gradient(135deg, rgba(59,130,246,0.3), rgba(99,102,241,0.2));   animation-duration: 14s; animation-delay: 2s; }
.bubble:nth-child(3)  { width: 50px; height: 50px; left: 35%; background: linear-gradient(135deg, rgba(14,165,233,0.25), rgba(59,130,246,0.15)); animation-duration: 22s; animation-delay: 4s; }
.bubble:nth-child(4)  { width: 80px; height: 80px; left: 50%; background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(168,85,247,0.1));   animation-duration: 25s; }
.bubble:nth-child(5)  { width: 35px; height: 35px; left: 55%; background: linear-gradient(135deg, rgba(59,130,246,0.3), rgba(14,165,233,0.2));   animation-duration: 16s; animation-delay: 6s; }
.bubble:nth-child(6)  { width: 45px; height: 45px; left: 65%; background: linear-gradient(135deg, rgba(139,92,246,0.25), rgba(99,102,241,0.15)); animation-duration: 20s; animation-delay: 3s; }
.bubble:nth-child(7)  { width: 25px; height: 25px; left: 75%; background: linear-gradient(135deg, rgba(14,165,233,0.3), rgba(59,130,246,0.2));   animation-duration: 15s; animation-delay: 7s; }
.bubble:nth-child(8)  { width: 60px; height: 60px; left: 80%; background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(139,92,246,0.1));   animation-duration: 24s; animation-delay: 5s; }
.bubble:nth-child(9)  { width: 15px; height: 15px; left: 90%; background: linear-gradient(135deg, rgba(59,130,246,0.35), rgba(99,102,241,0.25)); animation-duration: 12s; animation-delay: 1s; }
.bubble:nth-child(10) { width: 70px; height: 70px; left: 5%;  background: linear-gradient(135deg, rgba(168,85,247,0.2), rgba(139,92,246,0.1));   animation-duration: 28s; animation-delay: 8s; }

@keyframes float-up {
  0% { transform: translateY(0) rotate(0deg) scale(1); opacity: 0; }
  10%,90% { opacity: 0.6; }
  100% { transform: translateY(-120vh) rotate(360deg) scale(0.8); opacity: 0; }
}
@media (prefers-reduced-motion: reduce) {
  .bubble { animation: none; opacity: 0.3; bottom: auto; top: 50%; transform: translateY(-50%); }
}

.hero-content { max-width: 1200px; margin: 0 auto; position: relative; z-index: 1; }
.hero-title { margin: 0 0 1.5rem; display: flex; flex-direction: column; align-items: center; gap: 0.25rem; }
.title-main { font-size: clamp(36px, 7vw, 56px); font-weight: 700; color: var(--color-text-primary); line-height: 1.2; letter-spacing: -0.01em; }
.title-sub  { font-size: clamp(28px, 5vw, 40px); font-weight: 400; color: var(--color-text-secondary); line-height: 1.2; }
.hero-subtitle {
  font-size: clamp(18px, 2.5vw, 20px);
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 auto 3rem;
  max-width: 600px;
  line-height: 1.6;
}

.search-box-wrapper { margin: 0 auto 3rem; max-width: 700px; }
.search-input-group {
  display: flex;
  align-items: center;
  background: white;
  border: 2px solid var(--color-border);
  border-radius: var(--radius-full);
  box-shadow: var(--shadow-md);
  overflow: hidden;
  transition: all var(--transition-base);
}
.search-input-group:focus-within {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}
.search-input { flex: 1; border: none; padding: 1.25rem 2rem; font-size: 16px; outline: none; background: transparent; }
.search-input::placeholder { font-size: 14px; font-weight: 550; color: #6b7280; opacity: 1; }
.search-btn-icon {
  background: var(--color-primary);
  border: none;
  padding: 0 2rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  min-width: 60px;
  min-height: 60px;
  margin: 4px;
  border-radius: var(--radius-full);
  transition: all var(--transition-base);
}
.search-btn-icon:hover:not(:disabled) { background: var(--color-primary-hover); transform: scale(1.05); }
.search-btn-icon:disabled { opacity: 0.5; cursor: not-allowed; }
.search-clear-btn {
  background: transparent;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  color: var(--color-text-tertiary);
  margin-right: 0.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.search-clear-btn:hover { color: var(--color-text-primary); background: var(--color-bg-light); }

.categories-section { margin-top: 2rem; }
.categories-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.75rem;
  max-width: 1000px;
  margin: 0 auto;
}
.category-tag {
  padding: 0.625rem 1.5rem;
  border-radius: var(--radius-full);
  border: 1px solid var(--color-border);
  background: white;
  color: var(--color-text-primary);
  font-size: 15px;
  font-weight: 550;
  cursor: pointer;
  transition: all var(--transition-base);
  min-height: 44px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
}
.category-icon { width: 24px; height: 24px; flex-shrink: 0; }
.category-tag:hover {
  background: var(--color-primary-light);
  border-color: var(--color-primary);
  color: var(--color-primary);
  transform: translateY(-2px);
}

/* Stats banner */
.stats-section { padding: 4rem 1rem; background: white; }
.container { max-width: 1400px; margin: 0 auto; }
.stats-banner { text-align: center; margin-bottom: 3rem; }
.stats-title { font-size: clamp(24px, 4vw, 32px); font-weight: 600; color: var(--color-text-primary); line-height: 1.4; }
.stats-number { color: var(--color-primary); font-weight: 700; }
.stats-label  { color: var(--color-text-secondary); font-weight: 400; margin: 0 0.5rem; }

.agencies-section { margin-top: 3rem; }
.agencies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}
.agency-card {
  background: var(--color-bg-light);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-base);
}
.agency-card:hover {
  background: white;
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
  border-color: var(--color-primary);
}
.agency-icon { width: 32px; height: 32px; margin-bottom: 0.75rem; color: var(--color-primary); }
.agency-name { font-size: 14px; font-weight: 600; color: var(--color-text-primary); margin-bottom: 1rem; }
.agency-stats { display: flex; flex-direction: column; gap: 0.5rem; font-size: 12px; }
.agency-stat-item { display: flex; flex-direction: column; gap: 0.25rem; }
.stat-value { font-size: 16px; font-weight: 600; color: var(--color-text-primary); }
.stat-label-small { font-size: 11px; color: var(--color-text-tertiary); text-transform: uppercase; letter-spacing: 0.5px; }
.view-all-agencies { text-align: center; margin-top: 2rem; }
.view-all-link {
  color: var(--color-primary);
  font-weight: 500;
  text-decoration: none;
  transition: color var(--transition-base);
}
.view-all-link:hover { color: var(--color-primary-hover); text-decoration: underline; }

/* Trusted Section */
.trusted-section { padding: 4rem 1rem; background: var(--color-bg-light); }
.trusted-title {
  font-size: clamp(18px, 3vw, 22px);
  font-weight: 500;
  color: var(--color-text-secondary);
  text-align: center;
  margin-bottom: 2rem;
}
.bu-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}
.bu-card {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1.25rem;
  background: white;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  transition: all var(--transition-base);
  cursor: pointer;
}
.bu-card:hover { border-color: var(--color-primary); box-shadow: var(--shadow-md); }
.bu-logo-wrapper { position: relative; height: 40px; width: 180px; margin-bottom: 0.5rem; }
.bu-logo-img { position: absolute; inset: 0; object-fit: contain; object-position: left; width: 100%; height: 100%; }
.bu-name { font-size: 14px; font-weight: 600; color: var(--color-text-primary); line-height: 1.4; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.bu-stats { display: flex; flex-wrap: wrap; gap: 0.25rem; }
.bu-stat-item { font-size: 12px; color: var(--color-text-tertiary); line-height: 1.4; }
.bu-stat-item:not(:first-child)::before { content: '• '; }

/* Featured Datasets */
.featured-datasets { padding: 5rem 1rem; background: var(--color-bg-light); }
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}
.section-header h2 { font-size: clamp(24px, 4vw, 32px); font-weight: 700; color: var(--color-text-primary); margin: 0; }
.datasets-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}
.dataset-card {
  background: white;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  cursor: pointer;
  transition: all var(--transition-base);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.dataset-card:hover { box-shadow: var(--shadow-lg); transform: translateY(-4px); border-color: var(--color-primary); }
.dataset-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; }
.dataset-header h3 { font-size: 18px; font-weight: 600; color: var(--color-text-primary); margin: 0; flex: 1; line-height: 1.4; }
.category-badge {
  padding: 0.25rem 0.75rem;
  background: var(--color-primary-light);
  color: var(--color-primary);
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
}
.dataset-description {
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.dataset-stats {
  display: flex;
  gap: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border-light);
}
.stat-item { display: flex; flex-direction: column; gap: 0.25rem; }
.stat-label { font-size: 12px; color: var(--color-text-tertiary); text-transform: uppercase; letter-spacing: 0.5px; }

.loading-skeleton {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}
.dataset-card-skeleton {
  background: white;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
}
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-sm);
  height: 16px;
  margin-bottom: 0.5rem;
}
.skeleton-title { width: 70%; height: 20px; }
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@media (max-width: 768px) {
  .hero { padding: 3rem 1rem 2rem; }
  .datasets-grid { grid-template-columns: 1fr; }
  .section-header { flex-direction: column; align-items: flex-start; }
}
</style>
