import React, { useState, useEffect } from 'react'
import { listApplications, updateApplicationStatus } from '../../api/farmers'
import Card from '../../components/common/Card'
import Table from '../../components/common/Table'
import Badge from '../../components/common/Badge'
import Modal from '../../components/common/Modal'
import FilePreview from '../../components/common/FilePreview'
import SearchFilter from '../../components/common/SearchFilter'

export default function VerificationPanel() {
  const [apps, setApps] = useState([])
  const [selectedApp, setSelectedApp] = useState(null)
  const [reviewModalOpen, setReviewModalOpen] = useState(false)
  const [rejectReason, setRejectReason] = useState('')
  const [rejectNotes, setRejectNotes] = useState('')
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchApps() {
      try {
        const res = await listApplications({ status: 'pending' })
        setApps(res.data || res || [])
      } catch (err) {
        console.error(err)
        // Fallback mockup
        setApps([
          {
            _id: '65db4a52c0e86b0012abc888',
            farmer_name: 'Rahul Deshmukh',
            farmer_id: '65db4a52c0e86b0012abc123',
            scheme_name: 'Rashtriya Gokul Mission',
            scheme_id: '1',
            status: 'pending',
            created_at: new Date().toISOString(),
            step1_data: { name: 'Rahul Deshmukh', state: 'Maharashtra', district: 'Pune', acres: 5, cattle_count: 8 },
            step2_data: { aadhaar_file_id: 'aadhaar_mock_id', doc_712_file_id: 'doc_712_mock_id', mobile: '9876543210', cattle_count: 8 }
          },
          {
            _id: '65db4a52c0e86b0012abc889',
            farmer_name: 'Sanjay Pawar',
            farmer_id: '65db4a52c0e86b0012abc124',
            scheme_name: 'Gaushala Dev Grant',
            scheme_id: '3',
            status: 'under_review',
            created_at: new Date().toISOString(),
            step1_data: { name: 'Sanjay Pawar', state: 'Maharashtra', district: 'Nagpur', acres: 10, cattle_count: 104 },
            step2_data: { aadhaar_file_id: 'aadhaar_mock_id2', doc_712_file_id: 'doc_712_mock_id2', mobile: '9876543211', cattle_count: 104 }
          }
        ])
      } finally {
        setLoading(false)
      }
    }
    fetchApps()
  }, [])

  const handleOpenReview = (app) => {
    setSelectedApp(app)
    setReviewModalOpen(true)
  }

  const handleApprove = async () => {
    if (window.confirm('Are you sure you want to approve this application and allocate RFID tags?')) {
      try {
        await updateApplicationStatus(selectedApp._id, { status: 'approved' })
        setApps(prev => prev.filter(a => a._id !== selectedApp._id))
        setReviewModalOpen(false)
        alert('Application approved successfully! RFID tags allocated.')
      } catch (err) {
        alert(err.message)
      }
    }
  }

  const handleReject = async () => {
    if (!rejectReason) {
      alert('Please select a rejection reason.')
      return
    }
    if (window.confirm('Are you sure you want to reject this application?')) {
      try {
        await updateApplicationStatus(selectedApp._id, {
          status: 'rejected',
          reason: rejectReason,
          notes: rejectNotes
        })
        setApps(prev => prev.filter(a => a._id !== selectedApp._id))
        setReviewModalOpen(false)
        alert('Application rejected.')
      } catch (err) {
        alert(err.message)
      }
    }
  }

  const filteredApps = apps.filter(a =>
    a.farmer_name.toLowerCase().includes(search.toLowerCase()) ||
    a.scheme_name.toLowerCase().includes(search.toLowerCase())
  )

  const rejectionReasons = [
    { value: 'invalid_aadhaar', label: 'Aadhaar copy is invalid/unclear' },
    { value: 'unclear_document', label: '7/12 Land extract document is blurry' },
    { value: 'mismatch_cattle_count', label: 'Cattle count mismatch in details' },
    { value: 'image_issue', label: 'Cattle images are missing or not clear' },
    { value: 'proof_missing', label: 'Land ownership certificate is missing' },
    { value: 'other', label: 'Other details mismatch (see remarks)' }
  ]

  return (
    <div className="verification-panel-page">
      <div>
        <h2>Subsidy Verification Board</h2>
        <p className="page-subtitle">Verify land records, identities, and allocate electronic RFID tracking boundaries</p>
      </div>

      <Card className="mt-4">
        <SearchFilter
          search={search}
          onSearchChange={setSearch}
          placeholder="Search by farmer name or scheme..."
        />

        <Table
          headers={['Farmer', 'Scheme', 'Reported Cows', 'Submitted Date', 'Status', 'Actions']}
          data={filteredApps}
          loading={loading}
          renderRow={(app) => (
            <tr key={app._id}>
              <td><strong>{app.farmer_name}</strong></td>
              <td>{app.scheme_name}</td>
              <td><strong>{app.step1_data?.cattle_count}</strong> cows</td>
              <td>{app.created_at ? new Date(app.created_at).toLocaleDateString() : 'N/A'}</td>
              <td><Badge status={app.status} /></td>
              <td>
                <button className="btn btn-sm btn-primary" onClick={() => handleOpenReview(app)}>
                  🔎 Review Files
                </button>
              </td>
            </tr>
          )}
        />
      </Card>

      <Modal
        isOpen={reviewModalOpen}
        onClose={() => setReviewModalOpen(false)}
        title={`Verification: ${selectedApp?.farmer_name}`}
        size="lg"
        footer={
          <div className="verification-actions">
            <div className="rejection-form">
              <select
                className="form-control"
                value={rejectReason}
                onChange={e => setRejectReason(e.target.value)}
              >
                <option value="">Select Rejection Reason...</option>
                {rejectionReasons.map(r => (
                  <option key={r.value} value={r.value}>{r.label}</option>
                ))}
              </select>
              <input
                type="text"
                className="form-control"
                placeholder="Remarks/notes..."
                value={rejectNotes}
                onChange={e => setRejectNotes(e.target.value)}
              />
              <button className="btn btn-danger" onClick={handleReject}>
                ❌ Reject Application
              </button>
            </div>
            <button className="btn btn-success ml-auto" onClick={handleApprove}>
              ✓ Approve & Generate RFIDs
            </button>
          </div>
        }
      >
        {selectedApp && (
          <div className="review-modal-body">
            <div className="review-meta">
              <h4>Cattle Owner Details</h4>
              <div className="meta-grid">
                <div><strong>Farmer Name:</strong> {selectedApp.step1_data?.name}</div>
                <div><strong>State/District:</strong> {selectedApp.step1_data?.state}, {selectedApp.step1_data?.district}</div>
                <div><strong>Reported Cows:</strong> {selectedApp.step1_data?.cattle_count}</div>
                <div><strong>Acres of Land:</strong> {selectedApp.step1_data?.acres} Acres</div>
              </div>
            </div>

            <div className="review-documents-section mt-4">
              <h4>Review Submitted Files</h4>
              <div className="documents-flex mt-3">
                <div className="doc-item">
                  <h5>Aadhaar Identity Proof</h5>
                  <FilePreview fileId={selectedApp.step2_data?.aadhaar_file_id} fileName="aadhaar_card.pdf" contentType="application/pdf" />
                </div>
                <div className="doc-item">
                  <h5>7/12 Land Extract Document</h5>
                  <FilePreview fileId={selectedApp.step2_data?.doc_712_file_id} fileName="land_712.pdf" contentType="application/pdf" />
                </div>
              </div>
            </div>
          </div>
        )}
      </Modal>
    </div>
  )
}
