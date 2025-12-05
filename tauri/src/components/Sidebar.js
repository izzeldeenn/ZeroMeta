export function createSidebar() {
  const sidebar = document.createElement('div');
  sidebar.className = 'sidebar';
  
  sidebar.innerHTML = `
    <div class="logo-container">
      <img src="/assets/logo.png" alt="Logo" class="logo" />
    </div>
    
    <div class="sidebar-item" id="layers-toggle">
      <i class="fas fa-layer-group"></i>
      <span class="tooltip">Layers</span>
    </div>
    
    <div class="sidebar-item" id="settings-toggle">
      <i class="fas fa-cog"></i>
      <span class="tooltip">Settings</span>
    </div>
    
    <div class="sidebar-item" id="support-toggle">
      <i class="fas fa-hands-helping"></i>
      <span class="tooltip">Support Us</span>
    </div>
  `;
  
  return sidebar;
}

export function createSecondarySidebar() {
  const secondarySidebar = document.createElement('div');
  secondarySidebar.className = 'secondary-sidebar';
  secondarySidebar.id = 'secondary-sidebar';
  
  secondarySidebar.innerHTML = `
    <div class="sidebar-header">
      <h3 id="sidebar-title">Layers Store</h3>
      <button class="close-sidebar" id="close-sidebar">
        <i class="fas fa-times"></i>
      </button>
    </div>
    <div class="sidebar-content">
      <div class="sidebar-section">
        <h4>Base Maps</h4>
        <div class="sidebar-subitem">
          <i class="fas fa-satellite"></i>
          <span>Satellite</span>
        </div>
        <div class="sidebar-subitem">
          <i class="fas fa-mountain"></i>
          <span>Terrain</span>
        </div>
      </div>
      <div class="sidebar-section">
        <h4>Overlays</h4>
        <div class="sidebar-subitem">
          <i class="fas fa-car"></i>
          <span>Traffic</span>
        </div>
        <div class="sidebar-subitem">
          <i class="fas fa-cloud-sun-rain"></i>
          <span>Weather</span>
        </div>
      </div>
    </div>
  `;
  
  return secondarySidebar;
}
