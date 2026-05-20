import apiClient from './client.js'

export async function listFarmers(params = {}) {
  const query = new URLSearchParams(params).toString()
  return apiClient(`/farmers${query ? `?${query}` : ''}`)
}

export async function getFarmerById(id) {
  return apiClient(`/farmers/${id}`)
}

export async function getFarmerApplications(id) {
  return apiClient(`/farmers/${id}/applications`)
}

export async function updateApplicationStatus(applicationId, data) {
  return apiClient(`/applications/${applicationId}/status`, {
    method: 'PUT',
    body: JSON.stringify(data),
  })
}

export async function listApplications(params = {}) {
  const query = new URLSearchParams(params).toString()
  return apiClient(`/applications${query ? `?${query}` : ''}`)
}

export default { listFarmers, getFarmerById, getFarmerApplications, updateApplicationStatus, listApplications }
