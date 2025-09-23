<template>
  <div class="p-4 md:p-6 space-y-4">
    <h1 class="text-lg md:text-xl font-semibold">
      Measurements for {{ user?.username }}
    </h1>

    <div class="bg-white rounded-lg border p-0 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead class="bg-gray-50 text-gray-700">
            <tr>
              <th class="px-3 py-2">Time</th>
              <th class="px-3 py-2">pH</th>
              <th class="px-3 py-2">EC</th>
              <th class="px-3 py-2">Oxygen</th>
              <th class="px-3 py-2">Temperature (°C)</th>
              <th class="px-3 py-2">Water Temp (°C)</th>
              <th class="px-3 py-2">Humidity (%)</th>
            </tr>
          </thead>
          <tbody class="divide-y">
            <tr v-for="m in measurements" :key="m.id" class="hover:bg-gray-50">
              <td class="px-3 py-2">
                {{ m.timestamp ? new Date(m.timestamp.replace(" ", "T")).toLocaleString() : "—" }}
              </td>
              <td class="px-3 py-2">{{ m.ph ?? "—" }}</td>
              <td class="px-3 py-2">{{ m.ec ?? "—" }}</td>
              <td class="px-3 py-2">{{ m.oxygen ?? "—" }}</td>
              <td class="px-3 py-2">{{ m.temperature ?? "—" }}</td>
              <td class="px-3 py-2">{{ m.water_temperature ?? "—" }}</td>
              <td class="px-3 py-2">{{ m.humidity ?? "—" }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../../services/api'

const route = useRoute()
const userId = route.params.id

const measurements = ref([])
const user = ref(null)

async function loadData() {
  try {
    // fetch measurements
    const { data: mData } = await api.get(`/admin/users/${userId}/measurements`)
    console.log("Measurements API data:", mData)
    measurements.value = mData

    // fetch user info
    const { data: uData } = await api.get(`/admin/users/${userId}`)
    console.log("User API data:", uData)
    user.value = uData
  } catch (err) {
    console.error("Error loading data:", err)
  }
}

onMounted(loadData)
</script>
