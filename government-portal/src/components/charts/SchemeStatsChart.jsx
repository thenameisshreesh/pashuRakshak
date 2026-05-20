import React from 'react'
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

export default function SchemeStatsChart({ data = [] }) {
  const chartData = data.length > 0 ? data : [
    { scheme_name: 'Rashtriya Gokul Mission', applications_count: 45 },
    { scheme_name: 'National Dairy Plan II', applications_count: 32 },
    { scheme_name: 'Gaushala Dev Grant', applications_count: 24 }
  ]

  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <BarChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
          <XAxis dataKey="scheme_name" tickLine={false} tick={{ fill: '#6B7280', fontSize: 11 }} />
          <YAxis tickLine={false} tick={{ fill: '#6B7280', fontSize: 12 }} />
          <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderRadius: 8, border: '1px solid #E5E7EB' }} />
          <Legend verticalAlign="top" height={36} />
          <Bar
            name="Applications Enrolled"
            dataKey="applications_count"
            fill="#FF9933"
            radius={[4, 4, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
