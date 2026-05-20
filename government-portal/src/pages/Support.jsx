import React from 'react'
import Card from '../components/common/Card'

export default function Support() {
  return (
    <div className="support-page">
      <div>
        <h2>Helpdesk & Technical Support</h2>
        <p className="page-subtitle">Submit tickets or view manuals for ESP32 tag scanning hardware integrations</p>
      </div>

      <div className="profile-grid mt-4">
        <Card title="Need Help? Contact Technical Desk">
          <div className="details-list">
            <div className="details-item"><span className="details-label">Toll Free:</span> 1800-419-8800 (Mon-Sat, 9AM to 6PM)</div>
            <div className="details-item"><span className="details-label">Help Desk:</span> support-pashurakshak@nic.in</div>
            <div className="details-item"><span className="details-label">Central Office:</span> Krishi Bhawan, Dr. Rajendra Prasad Road, New Delhi</div>
          </div>
        </Card>

        <Card title="Quick Integration FAQ">
          <div className="details-list">
            <div className="details-item">
              <strong>How do I configure the ESP32 handheld scanner?</strong>
              <p className="text-sm mt-1 text-gray-500">Configure your scanner's firmware to point to the backend scan API: <code>/api/scanning/tag</code> using HTTP POST requests containing <code>{`{session_id, tag_id}`}</code>.</p>
            </div>
            <div className="details-item mt-2">
              <strong>What is suspicious status?</strong>
              <p className="text-sm mt-1 text-gray-500">This occurs when an RFID tag scanned on a farmer's cow is registered to another farmer's cattle registry under database records, flagging livestock counts manipulation.</p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
}
