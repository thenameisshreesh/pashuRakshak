const API_BASE = '/api'

export async function apiClient(endpoint, options = {}) {
  const token = localStorage.getItem('pashurakshak-token')
  
  const config = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
  }

  // Remove Content-Type for FormData
  if (options.body instanceof FormData) {
    delete config.headers['Content-Type']
  }

  const response = await fetch(`${API_BASE}${endpoint}`, config)

  if (response.status === 401) {
    localStorage.removeItem('pashurakshak-token')
    localStorage.removeItem('pashurakshak-user')
    window.location.href = '/login'
    throw new Error('Unauthorized')
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.message || `Request failed with status ${response.status}`)
  }

  if (response.status === 204) return null
  return response.json()
}

export default apiClient
