import React, { createContext, useContext, useState, useEffect } from 'react'
import { getProfile, login as apiLogin } from '../api/auth'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function initAuth() {
      const token = localStorage.getItem('pashurakshak-token')
      if (token) {
        try {
          const profile = await getProfile()
          setUser(profile.data || profile)
        } catch (err) {
          console.error('Failed to restore session:', err)
          localStorage.removeItem('pashurakshak-token')
        }
      }
      setLoading(false)
    }
    initAuth()
  }, [])

  const login = async (credentials) => {
    setLoading(true)
    try {
      const res = await apiLogin(credentials.username, credentials.password)
      const data = res.data || res
      localStorage.setItem('pashurakshak-token', data.access_token)
      setUser(data.user)
      setLoading(false)
      return data.user
    } catch (err) {
      setLoading(false)
      throw err
    }
  }

  const logout = () => {
    localStorage.removeItem('pashurakshak-token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, setUser }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
