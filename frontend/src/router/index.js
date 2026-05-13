import { createRouter, createWebHistory } from 'vue-router'
import HomeView           from '../views/HomeView.vue'
import GenieView          from '../views/GenieView.vue'
import GettingStartedView from '../views/GettingStartedView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/',                 name: 'home',            component: HomeView },
    { path: '/getting-started',  name: 'getting-started', component: GettingStartedView },
    { path: '/genie/:space',     name: 'genie',           component: GenieView },
  ],
})

export default router
