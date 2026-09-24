import { createAuthGuard } from '@auth0/auth0-vue'
import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import LandingView from '../views/LandingView.vue'
import AnonRecipeBrowserView from '../views/AnonRecipeBrowserView.vue'
import SkapaRecept from '../components/dashboard/SkapaRecept.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingView,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      beforeEnter: createAuthGuard(),
    },
    {
      path: '/anonrecipebrowsing',
      name: 'anonrecipebrowsing',
      component: AnonRecipeBrowserView,
    },
    {
      path: '/skapa-recept',
      name: 'skapa-recept',
      component: SkapaRecept,
    },
  ],
})

export default router