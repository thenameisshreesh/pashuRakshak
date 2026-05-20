import client from './client'

export async function startSession(raidId) {
  return client('/scanning/session/start', {
    method: 'POST',
    body: JSON.stringify({ raid_id: raidId })
  })
}

export async function submitTag(sessionId, tagId) {
  return client('/scanning/tag', {
    method: 'POST',
    body: JSON.stringify({ session_id: sessionId, tag_id: tagId })
  })
}

export async function endSession(sessionId) {
  return client(`/scanning/session/${sessionId}/end`, {
    method: 'POST'
  })
}

export async function getResults(sessionId) {
  return client(`/scanning/session/${sessionId}/results`)
}
