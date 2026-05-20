import React from 'react'

export default function Loader({ fullPage = false }) {
  if (fullPage) {
    return (
      <div className="fullpage-loader-wrapper">
        <div className="spinner"></div>
        <p className="loader-text">Loading PashuRakshak Portal...</p>
      </div>
    )
  }

  return (
    <div className="inline-loader-wrapper">
      <div className="spinner spinner-sm"></div>
    </div>
  )
}
