import React from 'react'

export default function Badge({ status, children }) {
  const getBadgeClass = (s) => {
    if (!s) return 'badge-default'
    const val = s.toLowerCase()
    if (['approved', 'completed', 'pass', 'matched', 'active'].includes(val)) return 'badge-success'
    if (['rejected', 'fail', 'unmatched', 'inactive', 'cancelled'].includes(val)) return 'badge-danger'
    if (['pending', 'scheduled', 'under_review'].includes(val)) return 'badge-warning'
    if (['suspicious'].includes(val)) return 'badge-suspicious'
    return 'badge-default'
  }

  return (
    <span className={`badge ${getBadgeClass(status)}`}>
      {children || status}
    </span>
  )
}
