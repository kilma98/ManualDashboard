<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCurrentUser, logout } from './services/auth'

const router = useRouter()
const user = ref(null)
const sidebarOpen = ref(false)

async function loadMe() {
  try { user.value = await getCurrentUser() } catch { user.value = null }
}

function onLogout() {
  logout()
  user.value = null
  router.replace({ name: 'login' })
}

onMounted(loadMe)
</script>

<template>
  <div class="min-h-screen">
    <header class="fixed top-0 inset-x-0 z-30 bg-white/80 backdrop-blur border-b">
      <div class="px-4 h-14 flex items-center gap-3">
        <button class="md:hidden inline-flex items-center justify-center rounded-md p-2 text-gray-600 hover:bg-gray-100" @click="sidebarOpen = !sidebarOpen" aria-label="Toggle navigation">
          <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
        </button>
        <router-link class="font-semibold text-gray-900" :to="{ name: 'dashboard' }">La Ferme Urbaine</router-link>
        <div class="ml-auto flex items-center gap-3 text-sm">
          <span v-if="user" class="hidden sm:inline text-gray-700">{{ user.username }} ({{ user.role }})</span>
          <router-link v-if="!user" class="text-blue-600 hover:text-blue-700" :to="{ name: 'login' }">Login</router-link>
          <button v-else class="text-red-600 hover:text-red-700" @click="onLogout">Logout</button>
        </div>
      </div>
    </header>

    <aside :class="['fixed z-20 top-14 left-0 h-[calc(100vh-56px)] w-64 bg-white border-r transform transition-transform duration-200 ease-in-out', sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0']">
      <nav class="p-3 space-y-1 text-sm">
        <router-link class="flex items-center gap-2 rounded px-3 py-2 hover:bg-gray-100" :to="{ name: 'dashboard' }" @click="sidebarOpen=false">
          <span class="i">🏠</span>
          <span>Dashboard</span>
        </router-link>
        <template v-if="user?.role === 'admin'">
          <router-link class="flex items-center gap-2 rounded px-3 py-2 hover:bg-gray-100" :to="{ name: 'admin-users' }" @click="sidebarOpen=false">👤 <span>Users</span></router-link>
          <router-link class="flex items-center gap-2 rounded px-3 py-2 hover:bg-gray-100" :to="{ name: 'admin-measurements' }" @click="sidebarOpen=false">📈 <span>Measurements</span></router-link>
          <router-link class="flex items-center gap-2 rounded px-3 py-2 hover:bg-gray-100" :to="{ name: 'admin-thresholds' }" @click="sidebarOpen=false">⚙️ <span>Thresholds</span></router-link>
        </template>
      </nav>
    </aside>

    <div class="pt-14 md:pl-64">
      <main class="px-4 py-4">
        <router-view />
      </main>
    </div>
  </div>
 </template>

<style scoped>
</style>
