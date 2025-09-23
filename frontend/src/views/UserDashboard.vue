<template>
  <div class="p-4 md:p-6">
    <div class="flex items-center justify-between mb-4 md:mb-6">
      <h1 class="text-xl md:text-2xl font-semibold tracking-tight">Dashboard</h1>
    </div>

    <!-- Add Measurement -->
    <div class="bg-white p-4 md:p-6 rounded-lg border mb-6">
      <h2 class="text-lg font-medium mb-4">Add Measurement</h2>
      <form @submit.prevent="submitMeasurement" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
        <div>
          <label class="text-sm text-gray-600">pH</label>
          <input v-model.number="form.ph" type="number" step="0.01" min="0" max="14"
                 class="w-full border rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 6.2" />
        </div>
        <div>
          <label class="text-sm text-gray-600">EC</label>
          <input v-model.number="form.ec" type="number" step="0.01"
                 class="w-full border rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 1.8" />
        </div>
        <div>
          <label class="text-sm text-gray-600">Oxygen (mg/L)</label>
          <input v-model.number="form.oxygen" type="number" step="0.01"
                 class="w-full border rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 8.5" />
        </div>
        <div>
          <label class="text-sm text-gray-600">Air Temperature (°C)</label>
          <input v-model.number="form.temperature" type="number" step="0.1"
                 class="w-full border rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 25.3" />
        </div>
        <div>
          <label class="text-sm text-gray-600">Water Temperature (°C)</label>
          <input v-model.number="form.water_temperature" type="number" step="0.1"
                 class="w-full border rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 22.5" />
        </div>
        <div>
          <label class="text-sm text-gray-600">Humidity (%)</label>
          <input v-model.number="form.humidity" type="number" step="0.1" min="0" max="100"
                 class="w-full border rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 60" />
        </div>
        <div class="flex items-end">
          <button class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-md transition-colors">Save</button>
        </div>
      </form>

      <!-- Alerts & messages -->
      <div v-if="alerts.length" class="mt-3 rounded-md border border-amber-200 bg-amber-50 text-amber-800 p-3 text-sm">
        <div class="font-medium mb-1">Alerts</div>
        <ul class="list-disc pl-5 space-y-1">
          <li v-for="a in alerts" :key="a">{{ a }}</li>
        </ul>
      </div>
      <p v-if="successMessage" class="mt-3 text-sm text-green-700">{{ successMessage }}</p>
      <p v-if="errorMessage" class="mt-3 text-sm text-red-700">{{ errorMessage }}</p>
    </div>

    <!-- Latest values cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4 md:gap-6 mb-6">
      <div class="bg-white p-6 rounded-lg border" v-for="field in latestFields" :key="field.key">
        <h3 class="text-sm font-medium text-gray-600 mb-2">Latest {{ field.label }}</h3>
        <p class="text-2xl font-bold" :class="field.color">{{ latest?.[field.key] ?? '--' }}</p>
        <p class="text-xs text-gray-500 mt-1">{{ latest ? 'Last updated: ' + formatTime(latest.timestamp) : 'No data yet' }}</p>
      </div>
    </div>

    <!-- Recent measurements table -->
    <div class="bg-white p-4 md:p-6 rounded-lg border">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-medium">Recent Measurements</h2>
        <button @click="loadMeasurements" class="text-sm text-blue-600">Refresh</button>
      </div>
      <div v-if="loading" class="text-center py-4">Loading...</div>
      <div v-else-if="measurements.length === 0" class="text-center py-4 text-gray-500">No measurements available</div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full">
          <thead>
            <tr class="border-b">
              <th class="text-left py-2 px-2">Time</th>
              <th class="text-left py-2 px-2">pH</th>
              <th class="text-left py-2 px-2">EC</th>
              <th class="text-left py-2 px-2">Oxygen</th>
              <th class="text-left py-2 px-2">Air Temp</th>
              <th class="text-left py-2 px-2">Water Temp</th>
              <th class="text-left py-2 px-2">Humidity</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="measurement in measurements.slice(0, 10)" :key="measurement.id" class="border-b">
              <td class="py-2 px-2">{{ formatTime(measurement.timestamp) }}</td>
              <td class="py-2 px-2">{{ measurement.ph }}</td>
              <td class="py-2 px-2">{{ measurement.ec }}</td>
              <td class="py-2 px-2">{{ measurement.oxygen }}</td>
              <td class="py-2 px-2">{{ measurement.temperature }}</td>
              <td class="py-2 px-2">{{ measurement.water_temperature }}</td>
              <td class="py-2 px-2">{{ measurement.humidity }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../services/api'

const measurements = ref([])
const loading = ref(true)
const form = ref({
  ph: null,
  ec: null,
  oxygen: null,
  temperature: null,
  water_temperature: null,
  humidity: null
})
const alerts = ref([])
const successMessage = ref('')
const errorMessage = ref('')

const latest = computed(() => (measurements.value.length > 0 ? measurements.value[0] : null))

// config for latest cards
const latestFields = [
  { key: 'ph', label: 'pH', color: 'text-blue-600' },
  { key: 'ec', label: 'EC', color: 'text-green-600' },
  { key: 'oxygen', label: 'Oxygen', color: 'text-orange-600' },
  { key: 'temperature', label: 'Air Temp', color: 'text-red-600' },
  { key: 'water_temperature', label: 'Water Temp', color: 'text-cyan-600' },
  { key: 'humidity', label: 'Humidity', color: 'text-purple-600' }
]

async function loadMeasurements() {
  try {
    loading.value = true
    const { data } = await api.get('/measurements/')
    measurements.value = data
  } catch (error) {
    console.error('Failed to load measurements:', error)
  } finally {
    loading.value = false
  }
}

async function submitMeasurement() {
  successMessage.value = ''
  errorMessage.value = ''
  alerts.value = []
  try {
    const payload = { ...form.value }
    const { data } = await api.post('/measurements/', payload)
    alerts.value = data.alerts || []
    successMessage.value = 'Measurement saved successfully.'
    await loadMeasurements()
  } catch (e) {
    errorMessage.value = 'Failed to save measurement.'
    console.error('Error submitting measurement:', e.response?.data || e)
  }
}

function formatTime(timestamp) {
  if (!timestamp) return '--'
  return new Date(timestamp).toLocaleString()
}

onMounted(loadMeasurements)
</script>
