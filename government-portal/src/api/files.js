import client from './client'

export async function uploadFile(formData) {
  return client('/files/upload', {
    method: 'POST',
    body: formData
  })
}

export function getFileUrl(fileId) {
  return `/api/files/${fileId}`
}
