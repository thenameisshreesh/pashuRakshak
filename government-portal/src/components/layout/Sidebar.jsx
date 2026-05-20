import React from 'react'
import { NavLink } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

export default function Sidebar({ collapsed, toggleCollapse }) {
  const { user, logout } = useAuth()

  const links = [
    { to: '/', label: 'Dashboard', icon: '📊' },
    { to: '/schemes', label: 'Schemes', icon: '📜' },
    { to: '/farmers', label: 'Farmers', icon: '👥' },
    { to: '/verification', label: 'Verification', icon: '🔍' },
    { to: '/raids', label: 'Raids', icon: '🚨' },
    { to: '/analytics', label: 'Analytics', icon: '📈' },
    { to: '/audit-logs', label: 'Audit Logs', icon: '🛡️' },
    { to: '/profile', label: 'My Profile', icon: '👤' },
    { to: '/settings', label: 'Settings', icon: '⚙️' },
    { to: '/support', label: 'Support', icon: '❓' }
  ]

  return (
    <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-header">
        <div className="logo-area">
          <span className="logo-icon">🐄</span>
          {!collapsed && <span className="logo-text">PashuRakshak</span>}
        </div>
        <button className="toggle-btn" onClick={toggleCollapse}>
          {collapsed ? '→' : '←'}
        </button>
      </div>

      <nav className="sidebar-nav">
        {links.map(link => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
            end={link.to === '/'}
          >
            <span className="nav-icon">{link.icon}</span>
            {!collapsed && <span className="nav-label">{link.label}</span>}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        {!collapsed && (
          <div className="user-info">
            <div className="user-avatar">👤</div>
            <div className="user-details">
              <p className="user-name">{user?.name || 'Officer'}</p>
              <p className="user-role">{user?.role?.toUpperCase() || 'OFFICER'}</p>
            </div>
          </div>
        )}
        <button className="logout-btn" onClick={logout} title="Logout">
          <span className="nav-icon">🚪</span>
          {!collapsed && <span>Logout</span>}
        </button>
      </div>
    </aside>
  )
}
