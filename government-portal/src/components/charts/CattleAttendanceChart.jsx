import React from 'react'
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

export default function CattleAttendanceChart({ data = [] }) {
  // If no data, show mock 12-month data
  const chartData = data.length > 0 ? data : [
    { month: 'Jan', attendance_rate: 94.5 },
    { month: 'Feb', attendance_rate: 95.2 },
    { month: 'Mar', attendance_rate: 93.8 },
    { month: 'Apr', attendance_rate: 96.1 },
    { month: 'May', attendance_rate: 94.0 },
    { month: 'Jun', attendance_rate: 95.7 },
    { month: 'Jul', attendance_rate: 93.2 },
    { month: 'Aug', attendance_rate: 96.5 },
    { month: 'Sep', attendance_rate: 97.1 },
    { month: 'Oct', attendance_rate: 95.9 },
    { month: 'Nov', attendance_rate: 96.3 },
    { month: 'Dec', attendance_rate: 97.8 }
  ]

  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <LineChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
          <XAxis dataKey="month" tickLine={false} tick={{ fill: '#6B7280', fontSize: 12 }} />
          <YAxis domain={[80, 100]} tickLine={false} tick={{ fill: '#6B7280', fontSize: 12 }} />
          <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderRadius: 8, border: '1px solid #E5E7EB' }} />
          <Legend verticalAlign="top" height={36} />
          <Line
            name="Cattle Attendance Rate (%)"
            type="monotone"
            dataKey="attendance_rate"
            stroke="#000080"
            strokeWidth={3}
            activeDot={{ r: 8 }}
            dot={{ strokeWidth: 2, r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
