const bedData = {
  wards: [
    {
      name: "General Ward",
      icon: "🏥",
      total: 30,
      occupied: 18,
      available: 12
    },
    {
      name: "Emergency Ward",
      icon: "🚑",
      total: 15,
      occupied: 9,
      available: 6
    }
  ]
};

function calculateTotals() {
  let totalBeds = 0;
  let occupiedBeds = 0;
  let availableBeds = 0;

  bedData.wards.forEach(ward => {
    totalBeds += ward.total;
    occupiedBeds += ward.occupied;
    availableBeds += ward.available;
  });

  const occupancyRate = ((occupiedBeds / totalBeds) * 100).toFixed(1);

  return { totalBeds, occupiedBeds, availableBeds, occupancyRate };
}

function updateSummary() {
  const totals = calculateTotals();
  
  document.getElementById('totalBeds').textContent = totals.totalBeds;
  document.getElementById('availableBeds').textContent = totals.availableBeds;
  document.getElementById('occupiedBeds').textContent = totals.occupiedBeds;
  document.getElementById('occupancyRate').textContent = totals.occupancyRate + '%';
}

function renderWards() {
  const bedsGrid = document.getElementById('bedsGrid');
  
  bedData.wards.forEach(ward => {
    const occupancyPercentage = ((ward.occupied / ward.total) * 100).toFixed(1);
    const availabilityStatus = ward.available > 5 ? 'good' : ward.available > 0 ? 'limited' : 'full';
    
    const cardHTML = `
      <div class="bed-card">
        <div class="bed-card-header">
          <span class="bed-icon">${ward.icon}</span>
          <h3>${ward.name}</h3>
        </div>
        <div class="bed-stats">
          <div class="bed-stat">
            <span class="stat-label">Total Beds</span>
            <span class="stat-value">${ward.total}</span>
          </div>
          <div class="bed-stat available-stat">
            <span class="stat-label">Available</span>
            <span class="stat-value stat-available">${ward.available}</span>
          </div>
          <div class="bed-stat">
            <span class="stat-label">Occupied</span>
            <span class="stat-value stat-occupied">${ward.occupied}</span>
          </div>
        </div>
        <div class="bed-progress">
          <div class="progress-bar">
            <div class="progress-fill" style="width: ${occupancyPercentage}%"></div>
          </div>
          <span class="progress-label">${occupancyPercentage}% Occupied</span>
        </div>
        <div class="bed-status ${availabilityStatus}">
          ${availabilityStatus === 'good' ? '✓ Available' : 
            availabilityStatus === 'limited' ? '⚠ Limited' : 
            '✗ Full'}
        </div>
      </div>
    `;
    
    bedsGrid.innerHTML += cardHTML;
  });
}


// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
  updateSummary();
  renderWards();
  updateTimestamp();
  
});
