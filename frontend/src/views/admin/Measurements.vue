<template>
  <div class="p-4 md:p-6 space-y-4">
    <div class="flex items-center justify-between">
      <h1 class="text-lg md:text-xl font-semibold">All Measurements</h1>
      <button @click="load" class="text-sm text-blue-600">Refresh</button>
    </div>
    <div class="bg-white rounded-lg border p-0 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead class="bg-gray-50 text-gray-700">
            <tr>
              <th class="px-3 py-2">User</th>
              <th class="px-3 py-2">Time</th>
              <th class="px-3 py-2">pH</th>
              <th class="px-3 py-2">EC</th>
              <th class="px-3 py-2">Oxygen</th>
            </tr>
          </thead>
          <tbody class="divide-y">
            <tr v-for="m in data" :key="m.id" class="hover:bg-gray-50">
              <td class="px-3 py-2">{{ m.user_id }}</td>
              <td class="px-3 py-2">{{ new Date(m.timestamp).toLocaleString() }}</td>
              <td class="px-3 py-2">{{ m.ph }}</td>
              <td class="px-3 py-2">{{ m.ec }}</td>
              <td class="px-3 py-2">{{ m.oxygen }}</td>
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

const data = ref([])

async function load() {
  const { data: res } = await api.get('/admin/measurements')
  data.value = res
}

onMounted(load)
</script>

