<template>
  <div class="p-4 md:p-6 space-y-4">
    <div class="flex items-center justify-between">
      <h1 class="text-lg md:text-xl font-semibold">Thresholds</h1>
    </div>

    <form @submit.prevent="save" class="grid grid-cols-2 md:grid-cols-4 gap-3 items-end bg-white p-4 rounded-lg border">
      <div class="col-span-2">
        <label class="text-sm text-gray-700">User ID (blank = global)</label>
        <input v-model="userId" type="number" class="w-full border rounded-md p-2" placeholder="User ID or empty" />
      </div>
      <div>
        <label class="text-sm text-gray-700">pH Min</label>
        <input v-model.number="form.ph_min" type="number" step="0.01" class="w-full border rounded-md p-2" />
      </div>
      <div>
        <label class="text-sm text-gray-700">pH Max</label>
        <input v-model.number="form.ph_max" type="number" step="0.01" class="w-full border rounded-md p-2" />
      </div>
      <div>
        <label class="text-sm text-gray-700">EC Min</label>
        <input v-model.number="form.ec_min" type="number" step="0.01" class="w-full border rounded-md p-2" />
      </div>
      <div>
        <label class="text-sm text-gray-700">EC Max</label>
        <input v-model.number="form.ec_max" type="number" step="0.01" class="w-full border rounded-md p-2" />
      </div>
      <div>
        <label class="text-sm text-gray-700">Oxygen Min</label>
        <input v-model.number="form.oxygen_min" type="number" step="0.01" class="w-full border rounded-md p-2" />
      </div>
      <div>
        <label class="text-sm text-gray-700">Oxygen Max</label>
        <input v-model.number="form.oxygen_max" type="number" step="0.01" class="w-full border rounded-md p-2" />
      </div>
      <button class="bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-md">Save</button>
    </form>

    <div class="bg-white rounded-lg border p-0 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead class="bg-gray-50 text-gray-700">
            <tr>
              <th class="px-3 py-2">ID</th>
              <th class="px-3 py-2">User ID</th>
              <th class="px-3 py-2">pH</th>
              <th class="px-3 py-2">EC</th>
              <th class="px-3 py-2">Oxygen</th>
            </tr>
          </thead>
          <tbody class="divide-y">
            <tr v-for="t in items" :key="t.id" class="hover:bg-gray-50">
              <td class="px-3 py-2">{{ t.id }}</td>
              <td class="px-3 py-2">{{ t.user_id ?? 'Global' }}</td>
              <td class="px-3 py-2">{{ t.ph_min }} - {{ t.ph_max }}</td>
              <td class="px-3 py-2">{{ t.ec_min }} - {{ t.ec_max }}</td>
              <td class="px-3 py-2">{{ t.oxygen_min }} - {{ t.oxygen_max }}</td>
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

const items = ref([])
const form = ref({ ph_min: 5.5, ph_max: 6.5, ec_min: 1, ec_max: 2, oxygen_min: 6, oxygen_max: 10 })
const userId = ref('')

async function load() {
  const { data } = await api.get('/admin/thresholds')
  items.value = data
}

async function save() {
  const payload = { ...form.value, user_id: userId.value ? Number(userId.value) : null }
  await api.post('/admin/thresholds', payload)
  await load()
}

onMounted(load)
</script>

