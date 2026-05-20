import React, { useState, useEffect } from 'react'
import { getDashboard, getCattleAttendance, getSchemeStats, getValidationStats } from '../api/analytics'
import StatsCard from '../components/common/StatsCard'
import Card from '../components/common/Card'
import Table from '../components/common/Table'
import Badge from '../components/common/Badge'
import CattleAttendanceChart from '../components/charts/CattleAttendanceChart'
import SchemeStatsChart from '../components/charts/SchemeStatsChart'
import ValidationPieChart from '../components/charts/ValidationPieChart'
import Loader from '../components/common/Loader'
import { Link } from 'react-router-dom'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [attendanceData, setAttendanceData] = useState([])
  const [schemeData, setSchemeData] = useState([])
  const [validationData, setValidationData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadData() {
      try {
        const [dashRes, attRes, schemeRes, valRes] = await Promise.all([
          getDashboard().catch(() => null),
          getCattleAttendance().catch(() => []),
          getSchemeStats().catch(() => []),
          getValidationStats().catch(() => [])
        ])

        if (dashRes) {
          setStats(dashRes)
        } else {
          // Mock fallback
          setStats({
            total_farmers: 156,
            total_schemes: 3,
            pending_applications: 18,
            active_raids: 4,
            recent_applications: [
              { _id: '1', farmer_name: 'Rahul Deshmukh', scheme_name: 'Rashtriya Gokul Mission', status: 'pending', created_at: new Date().toISOString() },
              { _id: '2', farmer_name: 'Amit Patel', scheme_name: 'Gaushala Dev Grant', status: 'approved', created_at: new Date().toISOString() },
              { _id: '3', farmer_name: 'Sanjay Pawar', scheme_name: 'National Dairy Plan II', status: 'rejected', created_at: new Date().toISOString() }
            ]
          })
        }

        setAttendanceData(attRes)
        setSchemeData(schemeRes)
        setValidationData(valRes)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  if (loading) return <Loader fullPage />

  return (
    <div className="dashboard-page">
      {/* Overview Cards */}
      <div className="stats-grid">
        <StatsCard title="Total Farmers" value={stats?.total_farmers} icon="👥" trend="12%" trendType="up" />
        <StatsCard title="Active Schemes" value={stats?.total_schemes} icon="📜" trend="0%" trendType="up" />
        <StatsCard title="Pending Applications" value={stats?.pending_applications} icon="⏳" trend="8%" trendType="down" />
        <StatsCard title="Scheduled Raids" value={stats?.active_raids} icon="🚨" trend="25%" trendType="up" />
      </div>

      {/* Charts Grid */}
      <div className="charts-grid mt-4">
        <Card title="Cattle Attendance Rate (RFID Checks)" subtitle="Average monthly scans verification rate">
          <CattleAttendanceChart data={attendanceData} />
        </Card>
        <Card title="Applications by Scheme" subtitle="Total farmer enrollments count per scheme">
          <SchemeStatsChart data={schemeData} />
        </Card>
      </div>

      <div className="charts-grid mt-4">
        <Card title="Inspection Pass vs Fail Ratio" subtitle="Overall validation audits outcome">
          <ValidationPieChart data={validationData} />
        </Card>
        
        <Card
          title="Recent Applications"
          subtitle="Latest submissions awaiting verification"
          actions={<Link to="/verification" className="btn btn-sm btn-outline">Review All</Link>}
        >
          <Table
            headers={['Farmer', 'Scheme', 'Status', 'Date']}
            data={stats?.recent_applications || []}
            renderRow={(app) => (
              <tr key={app._id}>
                <td><strong>{app.farmer_name}</strong></td>
                <td>{app.scheme_name}</td>
                <td><Badge status={app.status} /></td>
                <td>{app.created_at ? new Date(app.created_at).toLocaleDateString() : 'N/A'}</td>
              </tr>
            )}
          />
        </Card>
      </div>
    </div>
  )
}
