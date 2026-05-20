import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext.jsx'
import DashboardLayout from './components/layout/DashboardLayout.jsx'
import Login from './pages/Login.jsx'
import Dashboard from './pages/Dashboard.jsx'
import SchemesList from './pages/Schemes/SchemesList.jsx'
import CreateScheme from './pages/Schemes/CreateScheme.jsx'
import FarmersList from './pages/Farmers/FarmersList.jsx'
import FarmerDetails from './pages/Farmers/FarmerDetails.jsx'
import VerificationPanel from './pages/Verification/VerificationPanel.jsx'
import RaidsList from './pages/Raids/RaidsList.jsx'
import ScanningDashboard from './pages/Raids/ScanningDashboard.jsx'
import AnalyticsDashboard from './pages/Analytics/AnalyticsDashboard.jsx'
import AuditLogs from './pages/AuditLogs.jsx'
import Settings from './pages/Settings.jsx'
import Support from './pages/Support.jsx'
import Profile from './pages/Profile.jsx'

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <div className="page-loader"><div className="spinner" /></div>
  if (!user) return <Navigate to="/login" replace />
  return children
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <DashboardLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Dashboard />} />
        <Route path="schemes" element={<SchemesList />} />
        <Route path="schemes/create" element={<CreateScheme />} />
        <Route path="farmers" element={<FarmersList />} />
        <Route path="farmers/:id" element={<FarmerDetails />} />
        <Route path="verification" element={<VerificationPanel />} />
        <Route path="raids" element={<RaidsList />} />
        <Route path="raids/scanning/:raidId" element={<ScanningDashboard />} />
        <Route path="analytics" element={<AnalyticsDashboard />} />
        <Route path="audit-logs" element={<AuditLogs />} />
        <Route path="settings" element={<Settings />} />
        <Route path="support" element={<Support />} />
        <Route path="profile" element={<Profile />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
