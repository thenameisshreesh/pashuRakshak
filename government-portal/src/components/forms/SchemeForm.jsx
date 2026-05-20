import React, { useState } from 'react'

export default function SchemeForm({ initialData = {}, onSubmit, onCancel, loading = false }) {
  const [formData, setFormData] = useState({
    name: initialData.name || '',
    motive: initialData.motive || '',
    eligibility: initialData.eligibility || '',
    sponsor: initialData.sponsor || '',
    benefits: initialData.benefits || '',
    description: initialData.description || '',
    required_validations: initialData.required_validations || 1,
    required_cattle_count: initialData.required_cattle_count || 10,
    duration_days: initialData.duration_days || 365,
    ...initialData
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: ['required_validations', 'required_cattle_count', 'duration_days'].includes(name)
        ? parseInt(value) || 0
        : value
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <form onSubmit={handleSubmit} className="scheme-form">
      <div className="form-group">
        <label className="form-label" htmlFor="name">Scheme Name</label>
        <input
          type="text"
          id="name"
          name="name"
          className="form-control"
          value={formData.name}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-row">
        <div className="form-group col-6">
          <label className="form-label" htmlFor="sponsor">Sponsor / Department</label>
          <input
            type="text"
            id="sponsor"
            name="sponsor"
            className="form-control"
            value={formData.sponsor}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group col-6">
          <label className="form-label" htmlFor="duration_days">Duration (Days)</label>
          <input
            type="number"
            id="duration_days"
            name="duration_days"
            className="form-control"
            value={formData.duration_days}
            onChange={handleChange}
            min="1"
            required
          />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group col-6">
          <label className="form-label" htmlFor="required_cattle_count">Min Cattle Required</label>
          <input
            type="number"
            id="required_cattle_count"
            name="required_cattle_count"
            className="form-control"
            value={formData.required_cattle_count}
            onChange={handleChange}
            min="0"
            required
          />
        </div>
        <div className="form-group col-6">
          <label className="form-label" htmlFor="required_validations">Annual Inspections Required</label>
          <input
            type="number"
            id="required_validations"
            name="required_validations"
            className="form-control"
            value={formData.required_validations}
            onChange={handleChange}
            min="1"
            required
          />
        </div>
      </div>

      <div className="form-group">
        <label className="form-label" htmlFor="motive">Scheme Motive / Objective</label>
        <input
          type="text"
          id="motive"
          name="motive"
          className="form-control"
          value={formData.motive}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label className="form-label" htmlFor="eligibility">Eligibility Criteria</label>
        <textarea
          id="eligibility"
          name="eligibility"
          className="form-control"
          rows="3"
          value={formData.eligibility}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label className="form-label" htmlFor="benefits">Benefits Offered</label>
        <textarea
          id="benefits"
          name="benefits"
          className="form-control"
          rows="3"
          value={formData.benefits}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label className="form-label" htmlFor="description">Detailed Description</label>
        <textarea
          id="description"
          name="description"
          className="form-control"
          rows="4"
          value={formData.description}
          onChange={handleChange}
        />
      </div>

      <div className="form-actions">
        {onCancel && (
          <button type="button" className="btn btn-outline" onClick={onCancel} disabled={loading}>
            Cancel
          </button>
        )}
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Saving...' : 'Save Scheme'}
        </button>
      </div>
    </form>
  )
}
