import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getFarmerById, getFarmerApplications } from '../../api/farmers'
import Card from '../../components/common/Card'
import Badge from '../../components/common/Badge'
import Table from '../../components/common/Table'
import FilePreview from '../../components/common/FilePreview'
import Loader from '../../components/common/Loader'

export default function FarmerDetails() {
  const { id } = useParams()
  const [farmer, setFarmer] = useState(null)
  const [applications, setApplications] = useState([])
  const [activeTab, setActiveTab] = useState('profile')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadFarmerData() {
      try {
        const [farmerRes, appsRes] = await Promise.all([
          getFarmerById(id).catch(() => null),
          getFarmerApplications(id).catch(() => [])
        ])

        if (farmerRes) {
          setFarmer(farmerRes.data || farmerRes)
        } else {
          // Fallback mock
          setFarmer({
            _id: id,
            name: 'Ramesh Patil',
            mobile: '9876543210',
            state: 'Maharashtra',
            district: 'Pune',
            city: 'Baramati',
            address: 'Gat No. 412, Patil Vasti, Baramati, Pune 413102',
            cattle_count: 12,
            land_acres: 4.5,
            aadhaar: '1234 5678 9012',
            bank_account: '998877665544',
            ifsc: 'SBIN0001234',
            created_at: new Date().toISOString()
          })
        }
        setApplications(appsRes.data || appsRes || [])
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    loadFarmerData()
  }, [id])

  if (loading) return <Loader fullPage />

  return (
    <div className="farmer-details-page">
      <div className="page-header-actions">
        <div>
          <Link to="/farmers" className="back-link">← Back to Farmers</Link>
          <h2>{farmer?.name}</h2>
          <p className="page-subtitle">Farmer Profile & Livestock Registry</p>
        </div>
      </div>

      <div className="tabs-container mt-4">
        <div className="tab-headers">
          <button className={`tab-header ${activeTab === 'profile' ? 'active' : ''}`} onClick={() => setActiveTab('profile')}>
            👤 Profile Info
          </button>
          <button className={`tab-header ${activeTab === 'documents' ? 'active' : ''}`} onClick={() => setActiveTab('documents')}>
            📄 Verified Documents
          </button>
          <button className={`tab-header ${activeTab === 'applications' ? 'active' : ''}`} onClick={() => setActiveTab('applications')}>
            📜 Subsidy Applications
          </button>
        </div>

        <div className="tab-content mt-3">
          {activeTab === 'profile' && (
            <div className="profile-grid">
              <Card title="Personal Details">
                <div className="details-list">
                  <div className="details-item"><span className="details-label">Full Name:</span> {farmer?.name}</div>
                  <div className="details-item"><span className="details-label">Mobile Number:</span> {farmer?.mobile}</div>
                  <div className="details-item"><span className="details-label">State:</span> {farmer?.state}</div>
                  <div className="details-item"><span className="details-label">District:</span> {farmer?.district}</div>
                  <div className="details-item"><span className="details-label">Village / City:</span> {farmer?.city}</div>
                  <div className="details-item"><span className="details-label">Residential Address:</span> {farmer?.address}</div>
                </div>
              </Card>

              <Card title="Land & Livestock Limits">
                <div className="details-list">
                  <div className="details-item"><span className="details-label">Acres of Land:</span> {farmer?.land_acres} Acres</div>
                  <div className="details-item"><span className="details-label">Registered Cattle:</span> {farmer?.cattle_count} Cows</div>
                  <div className="details-item"><span className="details-label">Registered Since:</span> {farmer?.created_at ? new Date(farmer.created_at).toLocaleDateString() : 'N/A'}</div>
                </div>
              </Card>
            </div>
          )}

          {activeTab === 'documents' && (
            <div className="documents-grid">
              <Card title="Identity proof (Aadhaar)">
                <div className="details-list mb-3">
                  <div className="details-item"><span className="details-label">Aadhaar Number:</span> {farmer?.aadhaar}</div>
                </div>
                <FilePreview fileId={farmer?.aadhaar_file_id} fileName="aadhaar_card.pdf" contentType="application/pdf" />
              </Card>

              <Card title="Land Holding proof (7/12 Extract)">
                <div className="details-list mb-3">
                  <div className="details-item"><span className="details-label">Land Record No:</span> {farmer?.land_record_no || '7/12 Extract'}</div>
                </div>
                <FilePreview fileId={farmer?.doc_712_file_id} fileName="land_712.pdf" contentType="application/pdf" />
              </Card>

              <Card title="Bank Account Details">
                <div className="details-list">
                  <div className="details-item"><span className="details-label">Bank Account:</span> {farmer?.bank_account}</div>
                  <div className="details-item"><span className="details-label">IFSC Code:</span> {farmer?.ifsc}</div>
                </div>
              </Card>
            </div>
          )}

          {activeTab === 'applications' && (
            <Card title="Subsidy Enrollments">
              <Table
                headers={['Scheme Name', 'Date Submitted', 'Status', 'RFID Allocated', 'Actions']}
                data={applications}
                emptyMessage="No subsidy applications submitted by this farmer."
                renderRow={(app) => (
                  <tr key={app._id}>
                    <td><strong>{app.scheme_name || 'Cattle Grant'}</strong></td>
                    <td>{app.created_at ? new Date(app.created_at).toLocaleDateString() : 'N/A'}</td>
                    <td><Badge status={app.status} /></td>
                    <td>{app.rfid_tags_allocated || 0} tags</td>
                    <td>
                      <Link to={`/verification`} className="btn btn-sm btn-outline">
                        Review Details
                      </Link>
                    </td>
                  </tr>
                )}
              />
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}
