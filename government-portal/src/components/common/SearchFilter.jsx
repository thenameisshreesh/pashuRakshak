import React from 'react'

export default function SearchFilter({ search, onSearchChange, filters = [], onFilterChange, placeholder = 'Search...' }) {
  return (
    <div className="search-filter-container">
      <div className="search-input-wrapper">
        <span className="search-icon">🔍</span>
        <input
          type="text"
          className="search-input"
          placeholder={placeholder}
          value={search}
          onChange={e => onSearchChange(e.target.value)}
        />
      </div>
      
      {filters.length > 0 && (
        <div className="filters-wrapper">
          {filters.map((filter, i) => (
            <select
              key={i}
              className="filter-select"
              value={filter.value}
              onChange={e => onFilterChange(filter.key, e.target.value)}
            >
              <option value="">{filter.label}</option>
              {filter.options.map((opt, idx) => (
                <option key={idx} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          ))}
        </div>
      )}
    </div>
  )
}
