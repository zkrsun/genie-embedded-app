import { createRouter, createWebHistory } from 'vue-router'
import HomeView  from '../views/HomeView.vue'
import GenieView from '../views/GenieView.vue'
import { store } from '../store.js'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/',      name: 'home',  component: HomeView },
    { path: '/genie', name: 'genie', component: GenieView },
  ],
})

// Guard: redirect to home if /genie is accessed without an activeSpace
router.beforeEach((to) => {
  if (to.name === 'genie' && !store.activeSpace) {
    return { name: 'home' }
  }
})

export default router
