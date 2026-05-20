import React from 'react'

export default function StatsCard({ title, value, icon, trend, trendType = 'up', className = '' }) {
  return (
    <div className={`stats-card ${className}`}>
      <div className="stats-card-main">
        <div className="stats-card-details">
          <p className="stats-card-title">{title}</p>
          <h3 className="stats-card-value">{value}</h3>
        </div>
        <div className="stats-card-icon">{icon}</div>
      </div>
      {trend && (
        <div className="stats-card-footer">
          <span className={`trend-indicator ${trendType}`}>
            {trendType === 'up' ? '▲' : '▼'} {trend}
          </span>
          <span className="trend-text"> since last month</span>
        </div>
      )}
    </div>
  )
}
