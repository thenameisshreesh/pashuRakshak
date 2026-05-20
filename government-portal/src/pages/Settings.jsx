import React, { useState } from 'react'
import Card from '../components/common/Card'
import Button from '../components/common/Button'

export default function Settings() {
  const [loading, setLoading] = useState(false)
  const [settings, setSettings] = useState({
    rfidFrequency: '134.2 kHz (FDX-B)',
    mismatchThreshold: '5%',
    autoRaidTrigger: 'true',
    alertEmails: 'officer-alerts@pashurakshak.gov.in'
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setSettings(prev => ({ ...prev, [name]: value }))
  }

  const handleSave = (e) => {
    e.preventDefault()
    setLoading(true)
    setTimeout(() => {
      setLoading(false)
      alert('Configurations updated successfully!')
    }, 1000)
  }

  return (
    <div className="settings-page">
      <div>
        <h2>Portal Configurations</h2>
        <p className="page-subtitle">Adjust settings, RFID hardware thresholds, and auto-flag parameters</p>
      </div>

      <Card className="mt-4 max-w-2xl">
        <form onSubmit={handleSave}>
          <div className="form-group">
            <label className="form-label" htmlFor="rfidFrequency">RFID Scanning Frequency Standard</label>
            <select
              id="rfidFrequency"
              name="rfidFrequency"
              className="form-control"
              value={settings.rfidFrequency}
              onChange={handleChange}
            >
              <option value="134.2 kHz (FDX-B)">134.2 kHz (FDX-B) - Standard Animal RFID</option>
              <option value="125 kHz (ASK)">125 kHz (ASK) - Low Frequency Industrial</option>
              <option value="13.56 MHz (NFC)">13.56 MHz (NFC) - High Frequency Mifare</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="mismatchThreshold">Mismatch Cattle Tolerance Limit</label>
            <input
              type="text"
              id="mismatchThreshold"
              name="mismatchThreshold"
              className="form-control"
              value={settings.mismatchThreshold}
              onChange={handleChange}
            />
            <small className="help-text">Inspections failing by less than this percentage will not trigger fraud audit automatically.</small>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="autoRaidTrigger">Auto-Triggersurprise Audits on Re-submissions</label>
            <select
              id="autoRaidTrigger"
              name="autoRaidTrigger"
              className="form-control"
              value={settings.autoRaidTrigger}
              onChange={handleChange}
            >
              <option value="true">Yes, auto-schedule inspections</option>
              <option value="false">No, manual review only</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="alertEmails">Security Fraud Notification Emails</label>
            <input
              type="email"
              id="alertEmails"
              name="alertEmails"
              className="form-control"
              value={settings.alertEmails}
              onChange={handleChange}
            />
          </div>

          <Button type="submit" loading={loading} className="mt-4">
            Save System Configurations
          </Button>
        </form>
      </Card>
    </div>
  )
}
