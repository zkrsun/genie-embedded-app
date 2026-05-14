import { createRouter, createWebHistory } from 'vue-router'

import HomeView                from '../views/HomeView.vue'
import GenieView               from '../views/GenieView.vue'
import GettingStartedView      from '../views/GettingStartedView.vue'

import CatalogLandingView      from '../views/catalog/CatalogLandingView.vue'
import CatalogSearchView       from '../views/catalog/CatalogSearchView.vue'
import CatalogCategoriesView   from '../views/catalog/CatalogCategoriesView.vue'
import CatalogTeamsView        from '../views/catalog/CatalogTeamsView.vue'
import CatalogDataDetailView   from '../views/catalog/CatalogDataDetailView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/',                 name: 'home',            component: HomeView },
    { path: '/getting-started',  name: 'getting-started', component: GettingStartedView },
    { path: '/genie/:space',     name: 'genie',           component: GenieView },

    // Catalog
    { path: '/catalog',                   name: 'catalog',                  component: CatalogLandingView },
    { path: '/catalog/search',            name: 'catalog-search',           component: CatalogSearchView },
    { path: '/catalog/categories',        name: 'catalog-categories',       component: CatalogCategoriesView },
    { path: '/catalog/teams',             name: 'catalog-teams',            component: CatalogTeamsView },
    { path: '/catalog/datasets/:id',      name: 'catalog-dataset-detail',   component: CatalogDataDetailView },
  ],
})

export default router
