import React, { useState } from 'react'

export default function RaidScheduleForm({ application, onSubmit, onCancel, loading = false }) {
  const [formData, setFormData] = useState({
    farmer_id: application?.farmer_id || '',
    scheme_id: application?.scheme_id || '',
    application_id: application?._id || '',
    officer_id: '', // can be populated or assigned
    date: '',
    time: ''
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <form onSubmit={handleSubmit} className="raid-schedule-form">
      <div className="form-group">
        <label className="form-label">Application Details</label>
        <div className="details-read-only">
          <p><strong>Farmer ID:</strong> {application?.farmer_id}</p>
          <p><strong>Scheme ID:</strong> {application?.scheme_id}</p>
          <p><strong>Cattle Registered:</strong> {application?.step1_data?.cattle_count || 'N/A'}</p>
        </div>
      </div>

      <div className="form-group">
        <label className="form-label" htmlFor="officer_id">Assign Officer ID</label>
        <input
          type="text"
          id="officer_id"
          name="officer_id"
          className="form-control"
          placeholder="e.g. 65db4a5..."
          value={formData.officer_id}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-row">
        <div className="form-group col-6">
          <label className="form-label" htmlFor="date">Inspection Date</label>
          <input
            type="date"
            id="date"
            name="date"
            className="form-control"
            value={formData.date}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group col-6">
          <label className="form-label" htmlFor="time">Inspection Time</label>
          <input
            type="time"
            id="time"
            name="time"
            className="form-control"
            value={formData.time}
            onChange={handleChange}
            required
          />
        </div>
      </div>

      <div className="form-actions">
        {onCancel && (
          <button type="button" className="btn btn-outline" onClick={onCancel} disabled={loading}>
            Cancel
          </button>
        )}
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Scheduling...' : 'Schedule Raid'}
        </button>
      </div>
    </form>
  )
}
