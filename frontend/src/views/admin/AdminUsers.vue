<template>
    <div>
      <h1>All Users</h1>
      <ul>
        <li v-for="user in users" :key="user.id">
          <router-link :to="`/admin/users/${user.id}/measurements`">
            {{ user.username }}
          </router-link>
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import api from '../../services/api'
  
  const users = ref([])
  
  async function loadUsers() {
    const { data } = await api.get('/admin/users') // make sure you have this endpoint
    users.value = data
  }
  
  onMounted(loadUsers)
  </script>
  