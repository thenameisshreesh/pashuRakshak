import React, { useState, useEffect } from 'react'
import { listSchemes, deleteScheme } from '../../api/schemes'
import Table from '../../components/common/Table'
import Card from '../../components/common/Card'
import Badge from '../../components/common/Badge'
import SearchFilter from '../../components/common/SearchFilter'
import { Link } from 'react-router-dom'

export default function SchemesList() {
  const [schemes, setSchemes] = useState([])
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchSchemes() {
      try {
        const res = await listSchemes()
        setSchemes(res.data || res || [])
      } catch (err) {
        console.error(err)
        // Fallback
        setSchemes([
          { _id: '1', name: 'Rashtriya Gokul Mission', sponsor: 'Dept of Animal Husbandry', required_cattle_count: 10, required_validations: 2, active: true },
          { _id: '2', name: 'National Dairy Plan Phase-II', sponsor: 'NDDB', required_cattle_count: 5, required_validations: 1, active: true },
          { _id: '3', name: 'Gaushala Development Grant', sponsor: 'State Govt', required_cattle_count: 100, required_validations: 4, active: true }
        ])
      } finally {
        setLoading(false)
      }
    }
    fetchSchemes()
  }, [])

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to deactivate this scheme?')) {
      try {
        await deleteScheme(id)
        setSchemes(prev => prev.map(s => s._id === id ? { ...s, active: false } : s))
      } catch (err) {
        alert(err.message)
      }
    }
  }

  const filteredSchemes = schemes.filter(s =>
    s.name.toLowerCase().includes(search.toLowerCase()) ||
    s.sponsor.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="schemes-list-page">
      <div className="page-header-actions">
        <div>
          <h2>Government Cattle Schemes</h2>
          <p className="page-subtitle">Configure Cattle Count subsidies and verification requirements</p>
        </div>
        <Link to="/schemes/create" className="btn btn-primary">
          ➕ Create New Scheme
        </Link>
      </div>

      <Card className="mt-4">
        <SearchFilter
          search={search}
          onSearchChange={setSearch}
          placeholder="Search schemes by name or sponsor..."
        />

        <Table
          headers={['Scheme Name', 'Sponsoring Body', 'Min Cattle Count', 'Annual Audits', 'Status', 'Actions']}
          data={filteredSchemes}
          loading={loading}
          renderRow={(scheme) => (
            <tr key={scheme._id}>
              <td><strong>{scheme.name}</strong></td>
              <td>{scheme.sponsor}</td>
              <td>{scheme.required_cattle_count} cows</td>
              <td>{scheme.required_validations} scans / year</td>
              <td>
                <Badge status={scheme.active ? 'approved' : 'rejected'}>
                  {scheme.active ? 'Active' : 'Inactive'}
                </Badge>
              </td>
              <td>
                <div className="actions-cell">
                  <button className="btn btn-sm btn-outline text-danger" onClick={() => handleDelete(scheme._id)} disabled={!scheme.active}>
                    Deactivate
                  </button>
                </div>
              </td>
            </tr>
          )}
        />
      </Card>
    </div>
  )
}
