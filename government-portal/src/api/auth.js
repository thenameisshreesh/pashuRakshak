import apiClient from './client.js'

export async function login(username, password) {
  return apiClient('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
}

export async function getProfile() {
  return apiClient('/auth/profile')
}

export default { login, getProfile }
