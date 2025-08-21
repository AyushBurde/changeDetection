import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import AOIManagement from '@/views/AOIManagement.vue'
import ChangeDetection from '@/views/ChangeDetection.vue'
import Alerts from '@/views/Alerts.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { title: 'Dashboard - Change Detection System' }
  },
  {
    path: '/aoi',
    name: 'AOIManagement',
    component: AOIManagement,
    meta: { title: 'AOI Management - Change Detection System' }
  },
  {
    path: '/detection',
    name: 'ChangeDetection',
    component: ChangeDetection,
    meta: { title: 'Change Detection - Change Detection System' }
  },
  {
    path: '/alerts',
    name: 'Alerts',
    component: Alerts,
    meta: { title: 'Alerts - Change Detection System' }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Update page title on route change
router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title
  }
  next()
})

export default router

