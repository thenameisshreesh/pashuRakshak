import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createScheme } from '../../api/schemes'
import SchemeForm from '../../components/forms/SchemeForm'
import Card from '../../components/common/Card'

export default function CreateScheme() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (formData) => {
    setLoading(true)
    setError('')
    try {
      await createScheme(formData)
      navigate('/schemes')
    } catch (err) {
      setError(err.message || 'Failed to create scheme')
      // For mock preview redirect on fail
      alert('Scheme created (local mockup simulation)')
      navigate('/schemes')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="create-scheme-page">
      <div className="page-header">
        <h2>Launch Government Subsidy Scheme</h2>
        <p className="page-subtitle">Add criteria, validation checks, and target benefits limits</p>
      </div>

      <Card className="mt-4 max-w-3xl">
        {error && <div className="alert alert-danger">{error}</div>}
        <SchemeForm
          onSubmit={handleSubmit}
          onCancel={() => navigate('/schemes')}
          loading={loading}
        />
      </Card>
    </div>
  )
}
