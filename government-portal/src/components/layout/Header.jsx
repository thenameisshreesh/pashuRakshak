import React, { useState } from 'react'
import { useTheme } from '../../context/ThemeContext'
import { useAuth } from '../../context/AuthContext'

export default function Header() {
  const { theme, toggleTheme } = useTheme()
  const { user } = useAuth()
  const [showNotifications, setShowNotifications] = useState(false)

  const notifications = [
    { id: 1, title: 'New Application', desc: 'Farmer Ramesh Patil submitted a new application.', time: '10m ago' },
    { id: 2, title: 'Raid Scheduled', desc: 'Raid scheduled for Gaushala Dev Grant.', time: '1h ago' }
  ]

  return (
    <header className="header">
      <div className="header-left">
        <h1 className="header-title">National Cattle Grant Monitoring</h1>
        <div className="header-subtitle">Government of India Portal</div>
      </div>

      <div className="header-right">
        {/* Theme Toggle */}
        <button className="theme-toggle-btn" onClick={toggleTheme} title="Toggle Theme">
          {theme === 'light' ? '🌙' : '☀️'}
        </button>

        {/* Notifications */}
        <div className="notification-container">
          <button className="notification-bell" onClick={() => setShowNotifications(!showNotifications)}>
            🔔
            <span className="bell-badge">2</span>
          </button>
          
          {showNotifications && (
            <div className="notification-dropdown">
              <div className="dropdown-header">
                <h3>Notifications</h3>
                <button className="clear-btn">Mark all read</button>
              </div>
              <div className="dropdown-body">
                {notifications.map(n => (
                  <div key={n.id} className="dropdown-item">
                    <p className="item-title">{n.title}</p>
                    <p className="item-desc">{n.desc}</p>
                    <span className="item-time">{n.time}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* User profile */}
        <div className="header-profile">
          <span className="profile-initials">
            {user?.name ? user.name.split(' ').map(n => n[0]).join('') : 'GO'}
          </span>
          <span className="profile-name">{user?.name || 'Gov Officer'}</span>
        </div>
      </div>
    </header>
  )
}
