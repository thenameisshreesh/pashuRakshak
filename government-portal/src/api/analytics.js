import client from './client'

export async function getDashboard() {
  return client('/analytics/dashboard')
}

export async function getCattleAttendance() {
  return client('/analytics/cattle-attendance')
}

export async function getSchemeStats() {
  return client('/analytics/scheme-stats')
}

export async function getValidationStats() {
  return client('/analytics/validation-stats')
}
