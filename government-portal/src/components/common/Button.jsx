import React from 'react'

export default function Button({ children, type = 'button', variant = 'primary', loading = false, disabled = false, onClick, className = '', ...props }) {
  return (
    <button
      type={type}
      className={`btn btn-${variant} ${loading ? 'loading' : ''} ${className}`}
      disabled={disabled || loading}
      onClick={onClick}
      {...props}
    >
      {loading ? (
        <span className="btn-spinner">⌛</span>
      ) : null}
      {children}
    </button>
  )
}
