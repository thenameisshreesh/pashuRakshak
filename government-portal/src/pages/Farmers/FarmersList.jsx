import React, { useState, useEffect } from 'react'
import { listFarmers } from '../../api/farmers'
import Table from '../../components/common/Table'
import Card from '../../components/common/Card'
import SearchFilter from '../../components/common/SearchFilter'
import { Link } from 'react-router-dom'

export default function FarmersList() {
  const [farmers, setFarmers] = useState([])
  const [search, setSearch] = useState('')
  const [districtFilter, setDistrictFilter] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchFarmers() {
      try {
        const res = await listFarmers()
        setFarmers(res.data || res || [])
      } catch (err) {
        console.error(err)
        // Fallback mock
        setFarmers([
          { _id: '65db4a52c0e86b0012abc123', name: 'Ramesh Patil', mobile: '9876543210', district: 'Pune', state: 'Maharashtra', cattle_count: 12 },
          { _id: '65db4a52c0e86b0012abc124', name: 'Sanjay Pawar', mobile: '9876543211', district: 'Nagpur', state: 'Maharashtra', cattle_count: 8 },
          { _id: '65db4a52c0e86b0012abc125', name: 'Shreesh Pitambare', mobile: '9876543212', district: 'Mumbai', state: 'Maharashtra', cattle_count: 104 }
        ])
      } finally {
        setLoading(false)
      }
    }
    fetchFarmers()
  }, [])

  const filteredFarmers = farmers.filter(f => {
    const matchesSearch = f.name.toLowerCase().includes(search.toLowerCase()) || f.mobile.includes(search)
    const matchesDistrict = districtFilter ? f.district === districtFilter : true
    return matchesSearch && matchesDistrict
  })

  const districts = Array.from(new Set(farmers.map(f => f.district))).map(d => ({ value: d, label: d }))

  return (
    <div className="farmers-list-page">
      <div>
        <h2>Registered Cattle Farmers</h2>
        <p className="page-subtitle">Track registered livestock count limits and contact details</p>
      </div>

      <Card className="mt-4">
        <SearchFilter
          search={search}
          onSearchChange={setSearch}
          placeholder="Search by farmer name or mobile..."
          filters={[
            { key: 'district', label: 'All Districts', value: districtFilter, options: districts }
          ]}
          onFilterChange={(key, value) => {
            if (key === 'district') setDistrictFilter(value)
          }}
        />

        <Table
          headers={['Farmer Name', 'Mobile Number', 'Location', 'Registered Cattle', 'Actions']}
          data={filteredFarmers}
          loading={loading}
          renderRow={(farmer) => (
            <tr key={farmer._id}>
              <td><strong>{farmer.name}</strong></td>
              <td>{farmer.mobile}</td>
              <td>{farmer.district}, {farmer.state}</td>
              <td><strong>{farmer.cattle_count}</strong> cows</td>
              <td>
                <Link to={`/farmers/${farmer._id}`} className="btn btn-sm btn-outline">
                  🔎 View Profile
                </Link>
              </td>
            </tr>
          )}
        />
      </Card>
    </div>
  )
}
