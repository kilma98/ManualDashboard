<template>
  <div class="p-4 md:p-6 space-y-4">
    <div class="flex items-center justify-between">
      <h1 class="text-lg md:text-xl font-semibold">Users</h1>
    </div>
    <div class="bg-white rounded-lg border p-0 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead class="bg-gray-50 text-gray-700">
            <tr>
              <th class="px-3 py-2">ID</th>
              <th class="px-3 py-2">Username</th>
              <th class="px-3 py-2">Role</th>
            </tr>
          </thead>
          <tbody class="divide-y">
          <tr v-for="u in users" :key="u.id" class="hover:bg-gray-50">
              <td class="px-3 py-2">
                <router-link :to="`/admin/users/${u.id}/measurements`">{{ u.username }}</router-link>
              </td>
              <td class="px-3 py-2">{{ u.role }}</td>
            </tr>
            <tr v-for="u in users" :key="u.id" class="hover:bg-gray-50">
              <td class="px-3 py-2">{{ u.id }}</td>
              <td class="px-3 py-2">{{ u.username }}</td>
              <td class="px-3 py-2"><span class="inline-flex items-center rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-700">{{ u.role }}</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'

const users = ref([])

async function load() {
  const { data } = await api.get('/admin/users')
  users.value = data
}

onMounted(load)
</script>

