import api from './api'

export async function loginJson(username, password) {
  const { data } = await api.post('/login-json', { username, password })
  localStorage.setItem('token', data.access_token)
  return data
}

export async function registerUser(username, password) {
  const { data } = await api.post('/register', { username, password })
  return data
}

export async function getCurrentUser() {
  const { data } = await api.get('/me')
  return data
}

export function logout() {
  localStorage.removeItem('token')
}

