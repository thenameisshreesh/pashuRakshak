import React, { useState, useEffect } from 'react'
import { listRaids, scheduleRaid } from '../../api/raids'
import { listFarmers } from '../../api/farmers'
import { listSchemes } from '../../api/schemes'
import Card from '../../components/common/Card'
import Table from '../../components/common/Table'
import Badge from '../../components/common/Badge'
import Modal from '../../components/common/Modal'
import SearchFilter from '../../components/common/SearchFilter'
import { Link } from 'react-router-dom'

export default function RaidsList() {
  const [raids, setRaids] = useState([])
  const [farmers, setFarmers] = useState([])
  const [schemes, setSchemes] = useState([])
  const [scheduleModalOpen, setScheduleModalOpen] = useState(false)
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)

  // Form states
  const [targetFarmerId, setTargetFarmerId] = useState('')
  const [targetSchemeId, setTargetSchemeId] = useState('')
  const [raidDate, setRaidDate] = useState('')
  const [raidTime, setRaidTime] = useState('')

  useEffect(() => {
    async function loadData() {
      try {
        const [raidsRes, farmersRes, schemesRes] = await Promise.all([
          listRaids().catch(() => null),
          listFarmers().catch(() => null),
          listSchemes().catch(() => null)
        ])

        if (raidsRes) {
          setRaids(raidsRes.raids || raidsRes.data || raidsRes || [])
        } else {
          // Fallback mockup
          setRaids([
            { _id: 'r1', farmer_name: 'Ramesh Patil', farmer_mobile: '9876543210', scheme_name: 'Rashtriya Gokul Mission', officer_name: 'Amit Kumar', date: '2026-05-25', time: '10:00', status: 'scheduled' },
            { _id: 'r2', farmer_name: 'Sanjay Pawar', farmer_mobile: '9876543211', scheme_name: 'Gaushala Dev Grant', officer_name: 'Suresh Patil', date: '2026-05-26', time: '14:30', status: 'scheduled' }
          ])
        }

        setFarmers(farmersRes?.data || farmersRes || [
          { _id: '65db4a52c0e86b0012abc123', name: 'Ramesh Patil' },
          { _id: '65db4a52c0e86b0012abc124', name: 'Sanjay Pawar' }
        ])

        setSchemes(schemesRes?.data || schemesRes || [
          { _id: '1', name: 'Rashtriya Gokul Mission' },
          { _id: '3', name: 'Gaushala Dev Grant' }
        ])
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  const handleOpenSchedule = () => {
    setScheduleModalOpen(true)
  }

  const handleScheduleRaid = async (e) => {
    e.preventDefault()
    if (!targetFarmerId || !targetSchemeId || !raidDate || !raidTime) {
      alert('All fields are required.')
      return
    }

    try {
      const data = {
        farmer_id: targetFarmerId,
        scheme_id: targetSchemeId,
        officer_id: '65db4a52c0e86b0012abc999', // mockup current officer
        application_id: '65db4a52c0e86b0012abc888', // mockup application
        date: raidDate,
        time: raidTime
      }
      await scheduleRaid(data)
      alert('Raid inspection scheduled successfully!')
      setScheduleModalOpen(false)
      // Refresh list (mock add)
      const selectedFarmer = farmers.find(f => f._id === targetFarmerId)
      const selectedScheme = schemes.find(s => s._id === targetSchemeId)
      setRaids(prev => [
        {
          _id: Math.random().toString(),
          farmer_name: selectedFarmer?.name || 'Unknown Farmer',
          farmer_mobile: '9876543210',
          scheme_name: selectedScheme?.name || 'Cattle Grant',
          officer_name: 'Current Officer',
          date: raidDate,
          time: raidTime,
          status: 'scheduled'
        },
        ...prev
      ])
    } catch (err) {
      alert(err.message)
    }
  }

  const filteredRaids = raids.filter(r =>
    r.farmer_name.toLowerCase().includes(search.toLowerCase()) ||
    r.scheme_name.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="raids-list-page">
      <div className="page-header-actions">
        <div>
          <h2>Surprise Audit Raids</h2>
          <p className="page-subtitle">Schedule surprise spot-inspections to verify cattle attendance using mobile RFID scan gates</p>
        </div>
        <button className="btn btn-primary" onClick={handleOpenSchedule}>
          🚨 Schedule Surprise Inspection
        </button>
      </div>

      <Card className="mt-4">
        <SearchFilter
          search={search}
          onSearchChange={setSearch}
          placeholder="Search raids by farmer or scheme..."
        />

        <Table
          headers={['Farmer', 'Mobile', 'Scheme Name', 'Assigned Officer', 'Inspection Time', 'Status', 'Actions']}
          data={filteredRaids}
          loading={loading}
          renderRow={(raid) => (
            <tr key={raid._id}>
              <td><strong>{raid.farmer_name}</strong></td>
              <td>{raid.farmer_mobile}</td>
              <td>{raid.scheme_name}</td>
              <td>{raid.officer_name}</td>
              <td>{raid.date} at {raid.time}</td>
              <td><Badge status={raid.status} /></td>
              <td>
                <div className="actions-cell">
                  <Link to={`/raids/scanning/${raid._id}`} className="btn btn-sm btn-primary">
                    📶 Launch RFID Scanner
                  </Link>
                </div>
              </td>
            </tr>
          )}
        />
      </Card>

      <Modal
        isOpen={scheduleModalOpen}
        onClose={() => setScheduleModalOpen(false)}
        title="Schedule surprise inspection raid"
        footer={
          <div className="form-actions">
            <button className="btn btn-outline" onClick={() => setScheduleModalOpen(false)}>
              Cancel
            </button>
            <button className="btn btn-primary" onClick={handleScheduleRaid}>
              Schedule Surprise Raid
            </button>
          </div>
        }
      >
        <form onSubmit={handleScheduleRaid} className="raid-form">
          <div className="form-group">
            <label className="form-label" htmlFor="target_farmer">Target Cattle Owner / Gaushala</label>
            <select
              id="target_farmer"
              className="form-control"
              value={targetFarmerId}
              onChange={e => setTargetFarmerId(e.target.value)}
              required
            >
              <option value="">Select Farmer...</option>
              {farmers.map(f => (
                <option key={f._id} value={f._id}>{f.name}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="target_scheme">Under Subsidy Scheme</label>
            <select
              id="target_scheme"
              className="form-control"
              value={targetSchemeId}
              onChange={e => setTargetSchemeId(e.target.value)}
              required
            >
              <option value="">Select Scheme...</option>
              {schemes.map(s => (
                <option key={s._id} value={s._id}>{s.name}</option>
              ))}
            </select>
          </div>

          <div className="form-row">
            <div className="form-group col-6">
              <label className="form-label" htmlFor="raid_date">Date</label>
              <input
                type="date"
                id="raid_date"
                className="form-control"
                value={raidDate}
                onChange={e => setRaidDate(e.target.value)}
                required
              />
            </div>
            <div className="form-group col-6">
              <label className="form-label" htmlFor="raid_time">Time</label>
              <input
                type="time"
                id="raid_time"
                className="form-control"
                value={raidTime}
                onChange={e => setRaidTime(e.target.value)}
                required
              />
            </div>
          </div>
        </form>
      </Modal>
    </div>
  )
}
