import React from 'react'
import Card from '../../components/common/Card'
import StatsCard from '../../components/common/StatsCard'
import CattleAttendanceChart from '../../components/charts/CattleAttendanceChart'
import SchemeStatsChart from '../../components/charts/SchemeStatsChart'
import ValidationPieChart from '../../components/charts/ValidationPieChart'

export default function AnalyticsDashboard() {
  return (
    <div className="analytics-page">
      <div>
        <h2>Subsidy Analytics & Fraud Dashboard</h2>
        <p className="page-subtitle">Visual indicators of cow verification rates, budget distributions, and fraud prevention stats</p>
      </div>

      <div className="stats-grid mt-4">
        <StatsCard title="Total Grants Distributed" value="₹ 45.2 Lakhs" icon="💰" trend="15%" trendType="up" />
        <StatsCard title="Fraud Schemes Blocked" value="14 Cases" icon="🛡️" trend="40%" trendType="up" />
        <StatsCard title="Saved Treasury Funds" value="₹ 8.4 Lakhs" icon="📈" trend="22%" trendType="up" />
        <StatsCard title="Audited Cattle Count" value="1,842 Cows" icon="🐄" trend="8%" trendType="up" />
      </div>

      <div className="charts-grid mt-4">
        <Card title="Cattle Attendance Rate (RFID Checks)" subtitle="Average monthly scans verification rate">
          <CattleAttendanceChart />
        </Card>
        <Card title="Applications by Scheme" subtitle="Total farmer enrollments count per scheme">
          <SchemeStatsChart />
        </Card>
      </div>

      <div className="charts-grid mt-4">
        <Card title="Inspection Pass vs Fail Ratio" subtitle="Overall validation audits outcome">
          <ValidationPieChart />
        </Card>
        
        <Card title="Audits Breakdown by District">
          <div className="details-list">
            <div className="details-item"><span className="details-label">Pune:</span> 120 audited • 95 passed • 25 failed (20.8% fraud)</div>
            <div className="details-item"><span className="details-label">Nagpur:</span> 84 audited • 78 passed • 6 failed (7.1% fraud)</div>
            <div className="details-item"><span className="details-label">Nashik:</span> 98 audited • 92 passed • 6 failed (6.1% fraud)</div>
            <div className="details-item"><span className="details-label">Satara:</span> 45 audited • 41 passed • 4 failed (8.8% fraud)</div>
          </div>
        </Card>
      </div>
    </div>
  )
}
