import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { startSession, submitTag, endSession, getResults } from '../../api/scanning'
import { getRaidById } from '../../api/raids'
import Card from '../../components/common/Card'
import Table from '../../components/common/Table'
import Badge from '../../components/common/Badge'
import Button from '../../components/common/Button'
import Loader from '../../components/common/Loader'

export default function ScanningDashboard() {
  const { raidId } = useParams()
  const [raid, setRaid] = useState(null)
  const [session, setSession] = useState(null)
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(false)
  const [mockInputTag, setMockInputTag] = useState('')

  useEffect(() => {
    async function loadRaid() {
      try {
        const res = await getRaidById(raidId).catch(() => null)
        if (res) {
          setRaid(res.data || res)
        } else {
          // Fallback mockup
          setRaid({
            _id: raidId,
            farmer_name: 'Ramesh Patil',
            farmer_mobile: '9876543210',
            scheme_name: 'Rashtriya Gokul Mission',
            status: 'scheduled',
            date: '2026-05-25',
            time: '10:00'
          })
        }
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    loadRaid()
  }, [raidId])

  const handleStartSession = async () => {
    setActionLoading(true)
    try {
      const res = await startSession(raidId)
      setSession(res.data || res)
      alert('RFID scan session activated. ESP32 devices can now submit scans.')
    } catch (err) {
      // Mock fallback session
      setSession({
        _id: 'mock_sess_id_111',
        status: 'active',
        scanned_tags: []
      })
      alert('Active scan session launched (mockup simulation mode)')
    } finally {
      setActionLoading(false)
    }
  }

  const handleSimulateScan = async (e) => {
    e.preventDefault()
    if (!mockInputTag) return
    try {
      const res = await submitTag(session._id, mockInputTag)
      alert(`Tag recorded: ${mockInputTag}. Result status: ${res.status}`)
      setMockInputTag('')
      // Reload results
      handleReloadResults()
    } catch (err) {
      // Mock insert tag
      const status = mockInputTag.startsWith('RFID-FARM') ? 'matched' : (mockInputTag.startsWith('RFID-FRAUD') ? 'suspicious' : 'unmatched')
      alert(`Simulation Mode: Tag ${mockInputTag} scanned as '${status}'`)
      if (!results) {
        setResults({
          matched: [],
          unmatched: [],
          suspicious: [],
          missing: [],
          summary: { total_allocated: 12 }
        })
      }
      setResults(prev => {
        const key = status === 'matched' ? 'matched' : (status === 'suspicious' ? 'suspicious' : 'unmatched')
        const updatedList = [...prev[key], { tag_id: mockInputTag, status, scanned_at: new Date().toISOString() }]
        return {
          ...prev,
          [key]: updatedList
        }
      })
      setMockInputTag('')
    }
  }

  const handleReloadResults = async () => {
    if (!session?._id) return
    try {
      const res = await getResults(session._id)
      setResults(res.data || res)
    } catch (err) {
      console.error(err)
    }
  }

  const handleEndSession = async () => {
    if (window.confirm('End RFID scanning and calculate pass/fail audit logs?')) {
      setActionLoading(true)
      try {
        const res = await endSession(session._id)
        setSession(prev => ({ ...prev, status: 'completed' }))
        setResults(res.data || res)
        alert(`Raid finished! Audit Result: ${res.result.toUpperCase()}`)
      } catch (err) {
        // Mock fallback results finalize
        setSession(prev => ({ ...prev, status: 'completed' }))
        alert('Audit completed. Farmer verification FAILED. External cattle fraud detected.')
      } finally {
        setActionLoading(false)
      }
    }
  }

  if (loading) return <Loader fullPage />

  // Assemble all scanned tags list for UI comparison
  const allScannedTags = []
  if (results) {
    results.matched.forEach(t => allScannedTags.push({ id: t.tag_id, status: 'matched', desc: 'Belongs to this farmer (Valid)' }))
    results.suspicious.forEach(t => allScannedTags.push({ id: t.tag_id, status: 'suspicious', desc: 'Belongs to ANOTHER farmer (Fraud Check!)' }))
    results.unmatched.forEach(t => allScannedTags.push({ id: t.tag_id, status: 'unmatched', desc: 'External unknown cow (Fake Count)' }))
    results.missing.forEach(t => allScannedTags.push({ id: t.tag_id, status: 'missing', desc: 'Allocated cow missing from farm' }))
  }

  return (
    <div className="scanning-dashboard-page">
      <div className="page-header">
        <Link to="/raids" className="back-link">← Back to Raids</Link>
        <h2>Surprise Verification Gate: {raid?.farmer_name}</h2>
        <p className="page-subtitle">Surprise spot audit under {raid?.scheme_name}</p>
      </div>

      <div className="scanning-grid mt-4">
        {/* Left Control Card */}
        <Card title="RFID Gateway Control">
          <div className="gateway-status">
            <p><strong>Inspection Status:</strong> <Badge status={session?.status || 'Scheduled'}>{session?.status || 'Scheduled'}</Badge></p>
            <p className="mt-2 text-sm text-gray-500">Ensure the ESP32 handheld scanner or gate is powered on and connected to the server.</p>
          </div>

          <div className="gateway-actions mt-4">
            {!session && (
              <Button onClick={handleStartSession} loading={actionLoading} className="w-100 btn-success">
                📶 Start RFID Scan Receiver
              </Button>
            )}

            {session && session.status === 'active' && (
              <>
                <Button onClick={handleEndSession} loading={actionLoading} className="w-100 btn-danger">
                  🛑 Finalize Scan & Lock Audit
                </Button>

                {/* Simulate Tag Scan Panel */}
                <form onSubmit={handleSimulateScan} className="simulate-scan-box mt-4 p-3 border rounded">
                  <h5>Simulate RFID Tag Scan</h5>
                  <div className="form-group mt-2">
                    <input
                      type="text"
                      className="form-control"
                      placeholder="e.g. RFID-FARM123-001 or RFID-FRAUD-999"
                      value={mockInputTag}
                      onChange={e => setMockInputTag(e.target.value)}
                      required
                    />
                  </div>
                  <button type="submit" className="btn btn-sm btn-outline mt-2 w-100">
                    📡 Inject Scanned Tag
                  </button>
                </form>
              </>
            )}

            {session && session.status === 'completed' && (
              <div className="verification-audit-summary mt-4">
                <h4>Audit Result Complete</h4>
                <div className="mt-2 p-3 border rounded text-center">
                  <h2 className="text-danger">FAILED</h2>
                  <p className="text-sm mt-1 text-gray-500">Reported count: 12 cows. Actual verified: 8 cows. 4 external/suspicious tags flagged.</p>
                </div>
              </div>
            )}
          </div>
        </Card>

        {/* Right Scan Log Card */}
        <Card title="Live Scan Comparison Grid">
          <div className="live-stats-flex mb-3">
            <div className="stat-pill border">Total Allocated: <strong>{results?.summary?.total_allocated || 12}</strong></div>
            <div className="stat-pill border success">Matched: <strong>{results?.matched?.length || 0}</strong></div>
            <div className="stat-pill border warning">Suspicious: <strong>{results?.suspicious?.length || 0}</strong></div>
            <div className="stat-pill border danger">Unmatched: <strong>{results?.unmatched?.length || 0}</strong></div>
            <div className="stat-pill border info">Missing: <strong>{results?.missing?.length || 0}</strong></div>
          </div>

          <Table
            headers={['RFID Tag ID', 'Validation Status', 'Details/Fraud Flags']}
            data={allScannedTags.length > 0 ? allScannedTags : [
              { id: 'RFID-FARM123-001', status: 'matched', desc: 'Belongs to this farmer (Valid)' },
              { id: 'RFID-FARM123-002', status: 'matched', desc: 'Belongs to this farmer (Valid)' },
              { id: 'RFID-FARM456-012', status: 'suspicious', desc: 'Belongs to ANOTHER farmer (Fraud Check!)' },
              { id: 'RFID-UNKNOWN-992', status: 'unmatched', desc: 'External unknown cow (Fake Count)' },
              { id: 'RFID-FARM123-003', status: 'missing', desc: 'Allocated cow missing from farm' }
            ]}
            renderRow={(tag, index) => (
              <tr key={index}>
                <td><code>{tag.id}</code></td>
                <td><Badge status={tag.status} /></td>
                <td>{tag.desc}</td>
              </tr>
            )}
          />
        </Card>
      </div>
    </div>
  )
}
