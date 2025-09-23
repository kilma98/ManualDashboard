<template>
  <div class="min-h-[calc(100vh-56px)] flex items-center justify-center p-4">
    <div class="w-full max-w-sm bg-white rounded-lg border p-6">
      <h1 class="text-xl font-semibold mb-4">Create account</h1>
      <form @submit.prevent="onSubmit" class="space-y-3">
        <div>
          <label class="text-sm text-gray-700">Username</label>
          <input v-model="username" class="mt-1 w-full border rounded-md p-2" placeholder="Choose a username" />
        </div>
        <div>
          <label class="text-sm text-gray-700">Password</label>
          <input v-model="password" type="password" class="mt-1 w-full border rounded-md p-2" placeholder="••••••••" />
        </div>
        <button class="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded-md">Register</button>
      </form>
      <p v-if="error" class="text-red-600 text-sm mt-2">{{ error }}</p>
      <router-link class="text-sm text-blue-600" :to="{ name: 'login' }">Back to login</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { registerUser } from '../services/auth'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')

async function onSubmit() {
  error.value = ''
  try {
    await registerUser(username.value, password.value)
    router.replace({ name: 'login' })
  } catch (e) {
    error.value = 'Registration failed'
  }
}
</script>

