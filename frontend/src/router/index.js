import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import UserDashboard from '../views/UserDashboard.vue'
import AdminUsers from '../views/admin/Users.vue'
import AdminMeasurements from '../views/admin/Measurements.vue'
import AdminThresholds from '../views/admin/Thresholds.vue'
import { getCurrentUser } from '../services/auth'
import UserMeasurements from '../views/admin/UserMeasurements.vue'

const routes = [
  { path: '/login', name: 'login', component: Login, meta: { public: true } },
  { path: '/register', name: 'register', component: Register, meta: { public: true } },
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', name: 'dashboard', component: UserDashboard },
  { path: '/admin/users', name: 'admin-users', component: AdminUsers, meta: { requiresAdmin: true } },
  { path: '/admin/users/:id/measurements', name: 'admin-user-measurements', component: UserMeasurements, meta: { requiresAdmin: true } },
  { path: '/admin/measurements', name: 'admin-measurements', component: AdminMeasurements, meta: { requiresAdmin: true } },
  { path: '/admin/thresholds', name: 'admin-thresholds', component: AdminThresholds, meta: { requiresAdmin: true }},
  { path: '/admin/users/:id/measurements', name: 'admin-user-measurements', component: UserMeasurements, meta: { requiresAdmin: true } },
]


const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  if (to.meta.public) return true
  const token = localStorage.getItem('token')
  if (!token) return { name: 'login', query: { redirect: to.fullPath } }
  try {
    const me = await getCurrentUser()
    if (to.meta.requiresAdmin && me.role !== 'admin') return { name: 'dashboard' }
    return true
  } catch {
    localStorage.removeItem('token')
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  
})

export default router

