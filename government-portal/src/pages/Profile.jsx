import React from 'react'
import { useAuth } from '../context/AuthContext'
import Card from '../components/common/Card'

export default function Profile() {
  const { user } = useAuth()

  return (
    <div className="profile-page">
      <div>
        <h2>My Officer Profile</h2>
        <p className="page-subtitle">Your credentials and official registration details on PashuRakshak</p>
      </div>

      <Card className="mt-4 max-w-2xl" title="Official Profile Details">
        <div className="details-list">
          <div className="details-item"><span className="details-label">Full Name:</span> {user?.name || 'Gov Officer'}</div>
          <div className="details-item"><span className="details-label">Role:</span> <span className="uppercase">{user?.role || 'OFFICER'}</span></div>
          <div className="details-item"><span className="details-label">Department:</span> {user?.department || 'Animal Husbandry'}</div>
          <div className="details-item"><span className="details-label">Designation:</span> {user?.designation || 'Field Inspector'}</div>
          <div className="details-item"><span className="details-label">Email:</span> {user?.email || 'officer@pashurakshak.gov.in'}</div>
          <div className="details-item"><span className="details-label">Mobile:</span> {user?.mobile || '9876543210'}</div>
        </div>
      </Card>
    </div>
  )
}
