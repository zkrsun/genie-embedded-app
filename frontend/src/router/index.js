import { createRouter, createWebHistory } from 'vue-router'
import HomeView  from '../views/HomeView.vue'
import GenieView from '../views/GenieView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/',                              name: 'home',  component: HomeView },
    { path: '/genie/:bu/:domain/:space',      name: 'genie', component: GenieView },
  ],
})

export default router
