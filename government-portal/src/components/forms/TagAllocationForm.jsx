import React, { useState } from 'react'

export default function TagAllocationForm({ application, onSubmit, onCancel, loading = false }) {
  const [formData, setFormData] = useState({
    application_id: application?._id || '',
    farmer_id: application?.farmer_id || '',
    scheme_id: application?.scheme_id || '',
    cattle_count: application?.step1_data?.cattle_count || 1
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name === 'cattle_count' ? parseInt(value) || 0 : value
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <form onSubmit={handleSubmit} className="tag-allocation-form">
      <div className="form-group">
        <label className="form-label">Application Info</label>
        <div className="details-read-only">
          <p><strong>Application ID:</strong> {application?._id}</p>
          <p><strong>Farmer ID:</strong> {application?.farmer_id}</p>
          <p><strong>Registered Cattle Count:</strong> {application?.step1_data?.cattle_count}</p>
        </div>
      </div>

      <div className="form-group">
        <label className="form-label" htmlFor="cattle_count">Allocate Tags For Cattle Count</label>
        <input
          type="number"
          id="cattle_count"
          name="cattle_count"
          className="form-control"
          value={formData.cattle_count}
          onChange={handleChange}
          min="1"
          required
        />
        <small className="help-text">This will auto-generate RFID tags in format RFID-FARM[XXX]-[NNN].</small>
      </div>

      <div className="form-actions">
        {onCancel && (
          <button type="button" className="btn btn-outline" onClick={onCancel} disabled={loading}>
            Cancel
          </button>
        )}
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Allocating...' : 'Allocate Tags'}
        </button>
      </div>
    </form>
  )
}
