import client from './client'

export async function listSchemes() {
  return client('/schemes')
}

export async function createScheme(data) {
  return client('/schemes', {
    method: 'POST',
    body: JSON.stringify(data)
  })
}

export async function updateScheme(id, data) {
  return client(`/schemes/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data)
  })
}

export async function deleteScheme(id) {
  return client(`/schemes/${id}`, {
    method: 'DELETE'
  })
}

export async function getSchemeById(id) {
  return client(`/schemes/${id}`)
}
