import client from './client'

export async function scheduleRaid(data) {
  return client('/raids', {
    method: 'POST',
    body: JSON.stringify(data)
  })
}

export async function listRaids(params = {}) {
  const query = new URLSearchParams(params).toString()
  return client(`/raids${query ? `?${query}` : ''}`)
}

export async function getRaidById(id) {
  return client(`/raids/${id}`)
}

export async function updateRaidStatus(id, status) {
  return client(`/raids/${id}`, {
    method: 'PUT',
    body: JSON.stringify({ status })
  })
}
