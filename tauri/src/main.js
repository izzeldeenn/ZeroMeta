import { createSidebar, createSecondarySidebar } from './components/Sidebar.js';
import { renderHomePage } from './pages/HomePage.js';
import { renderSettingsPage } from './pages/SettingsPage.js';

class App {
  constructor() {
    this.isMobile = window.innerWidth <= 768;
    this.currentPage = 'home';
    this.init();
  }

  async init() {
    this.app = document.getElementById('app');
    this.setupApp();
    this.setupEventListeners();
    this.navigateTo('home');
  }

  setupApp() {
    // Create overlay for mobile
    this.overlay = document.createElement('div');
    this.overlay.className = 'overlay';
    
    // Create main layout
    this.app.innerHTML = '';
    this.app.appendChild(this.overlay);
    
    // Create main container
    this.appContainer = document.createElement('div');
    this.appContainer.className = 'app-container';
    
    // Create sidebars and content container
    this.sidebar = createSidebar();
    this.secondarySidebar = createSecondarySidebar();
    this.contentContainer = document.createElement('div');
    this.contentContainer.className = 'content-container';
    
    // Create home button in sidebar
    this.homeButton = document.createElement('div');
    this.homeButton.className = 'sidebar-item';
    this.homeButton.id = 'home-toggle';
    this.homeButton.innerHTML = `
      <i class="fas fa-home"></i>
      <span class="tooltip">الرئيسية</span>
    `;
    
    // Add home button after the logo container
    const logoContainer = this.sidebar.querySelector('.logo-container');
    if (logoContainer && logoContainer.nextSibling) {
      this.sidebar.insertBefore(this.homeButton, logoContainer.nextSibling);
    } else {
      // Fallback: add to the end if logo container is not found
      this.sidebar.appendChild(this.homeButton);
    }
    
    // Append all elements
    this.appContainer.appendChild(this.sidebar);
    this.appContainer.appendChild(this.secondarySidebar);
    this.appContainer.appendChild(this.contentContainer);
    this.app.appendChild(this.appContainer);
    
    // Cache DOM elements
    this.layersToggle = this.sidebar.querySelector('#layers-toggle');
    this.settingsToggle = this.sidebar.querySelector('#settings-toggle');
    this.supportToggle = this.sidebar.querySelector('#support-toggle');
    this.closeSidebar = this.secondarySidebar.querySelector('#close-sidebar');
  }

  setupEventListeners() {
    // Home button click handler
    this.homeButton.addEventListener('click', (e) => {
      this.navigateTo('home');
      this.closeAllSidebars();
      e.stopPropagation();
    });

    // Show layers grid in main content
    this.layersToggle.addEventListener('click', (e) => {
      this.showLayersGrid();
      this.closeAllSidebars();
      e.stopPropagation();
    });

    this.settingsToggle.addEventListener('click', (e) => {
      this.navigateTo('settings');
      e.stopPropagation();
    });

    this.supportToggle.addEventListener('click', (e) => {
      this.navigateTo('support');
      e.stopPropagation();
    });

    this.closeSidebar.addEventListener('click', (e) => {
      this.closeAllSidebars();
      e.stopPropagation();
    });

    this.overlay.addEventListener('click', () => this.closeAllSidebars());
    
    // Handle window resize
    window.addEventListener('resize', () => this.handleResize());
    
    // Close secondary sidebar when clicking outside on desktop
    document.addEventListener('click', (e) => {
      if (!this.isMobile && 
          !this.secondarySidebar.contains(e.target) && 
          !this.layersToggle.contains(e.target)) {
        this.secondarySidebar.classList.remove('active');
      }
    });
  }

  // Show layers in main content area
  showLayersGrid() {
    // Clear current content
    this.contentContainer.innerHTML = '';
    
    // Create layers grid container
    const layersGrid = document.createElement('div');
    layersGrid.className = 'layers-grid';
    
    // Sample layers data - replace with your actual layers data
    const layers = [
      { id: 'satellite', name: 'Satellite', icon: 'satellite', pinned: false },
      { id: 'terrain', name: 'Terrain', icon: 'mountain', pinned: false },
      { id: 'traffic', name: 'Traffic', icon: 'car', pinned: false },
      { id: 'weather', name: 'Weather', icon: 'cloud-sun-rain', pinned: false },
      { id: 'borders', name: 'Borders', icon: 'border-all', pinned: false },
      { id: 'places', name: 'Places', icon: 'map-marker-alt', pinned: false }
    ];
    
    // Create grid items
    layers.forEach(layer => {
      const layerItem = document.createElement('div');
      layerItem.className = 'layer-item';
      layerItem.dataset.id = layer.id;
      
      layerItem.innerHTML = `
        <div class="layer-icon">
          <i class="fas fa-${layer.icon}"></i>
        </div>
        <div class="layer-name">${layer.name}</div>
        <button class="pin-layer" data-id="${layer.id}">
          <i class="fas fa-thumbtack"></i> Pin to Sidebar
        </button>
      `;
      
      // Add click handler to show layer details in secondary sidebar
      layerItem.addEventListener('click', (e) => {
        if (!e.target.closest('.pin-layer')) {
          this.showLayerDetails(layer);
        }
      });
      
      // Add pin button handler
      const pinButton = layerItem.querySelector('.pin-layer');
      pinButton.addEventListener('click', (e) => {
        e.stopPropagation();
        this.togglePinLayer(layer);
      });
      
      layersGrid.appendChild(layerItem);
    });
    
    // Add header
    const header = document.createElement('div');
    header.className = 'page-header';
    header.innerHTML = '<h2>Available Layers</h2>';
    
    this.contentContainer.appendChild(header);
    this.contentContainer.appendChild(layersGrid);
  }
  
  // Show layer details in secondary sidebar
  showLayerDetails(layer) {
    const title = this.secondarySidebar.querySelector('#sidebar-title');
    const content = this.secondarySidebar.querySelector('.sidebar-content');
    
    title.textContent = layer.name;
    content.innerHTML = `
      <div class="layer-details">
        <div class="layer-preview">
          <i class="fas fa-${layer.icon} fa-3x"></i>
        </div>
        <h3>${layer.name} Layer</h3>
        <p>Layer details and configuration options will appear here.</p>
        <div class="layer-actions">
          <button class="btn btn-primary">
            <i class="fas fa-eye"></i> Preview
          </button>
          <button class="btn btn-secondary">
            <i class="fas fa-cog"></i> Settings
          </button>
        </div>
      </div>
    `;
    
    // Show the secondary sidebar
    this.secondarySidebar.classList.add('active');
    if (this.isMobile) {
      this.overlay.classList.add('active');
    }
  }
  
  // Toggle layer pin to main sidebar
  togglePinLayer(layer) {
    // Find the layer in the sidebar or add it if not present
    const sidebarItem = document.querySelector(`.sidebar-item[data-layer-id="${layer.id}"]`);
    
    if (sidebarItem) {
      // If already pinned, remove it
      sidebarItem.remove();
    } else {
      // Create a deep copy of the layer object to avoid reference issues
      const layerCopy = JSON.parse(JSON.stringify(layer));
      
      // Add to sidebar
      const newItem = document.createElement('div');
      newItem.className = 'sidebar-item';
      newItem.dataset.layerId = layer.id;
      newItem.innerHTML = `
        <i class="fas fa-${layer.icon}"></i>
        <span class="tooltip">${layer.name}</span>
      `;
      
      // Store the layer data as a data attribute
      newItem.setAttribute('data-layer', JSON.stringify(layerCopy));
      
      // Add click handler to show layer details
      newItem.addEventListener('click', (e) => {
        e.stopPropagation();
        const layerData = JSON.parse(newItem.getAttribute('data-layer'));
        this.showLayerDetails(layerData);
      });
      
      // Insert before the settings item in the sidebar
      this.settingsToggle.parentNode.insertBefore(newItem, this.settingsToggle);
    }
  }

  // Close all sidebars
  closeAllSidebars() {
    this.secondarySidebar.classList.remove('active');
    if (this.isMobile) {
      this.overlay.classList.remove('active');
    }
  }

  // Handle window resize
  handleResize() {
    const wasMobile = this.isMobile;
    this.isMobile = window.innerWidth <= 768;
    
    if (wasMobile !== this.isMobile) {
      if (!this.isMobile) {
        this.overlay.classList.remove('active');
      }
    }
  }

  navigateTo(page) {
    this.currentPage = page;
    this.contentContainer.innerHTML = '';
    
    // Update active state
    document.querySelectorAll('.sidebar-item').forEach(item => {
      item.classList.remove('active');
    });
    
    // Add active class to current page
    if (page === 'settings') {
      this.settingsToggle.classList.add('active');
      this.contentContainer.appendChild(renderSettingsPage());
    } else if (page === 'support') {
      this.supportToggle.classList.add('active');
      this.contentContainer.innerHTML = `
        <div class="page-content">
          <div class="page-header">
            <h2>دعم المشروع</h2>
          </div>
          <div class="support-container">
            <div class="support-option">
              <i class="fas fa-heart"></i>
              <h3>دعم مادي</h3>
              <p>ساعدنا في استمرارية التطوير والتحسين</p>
              <button class="btn btn-donate">تبرع الآن</button>
            </div>
            <div class="support-option">
              <i class="fas fa-code"></i>
              <h3>دعم فني</h3>
              <p>ساهم في تطوير الكود المصدري</p>
              <a href="#" class="btn btn-secondary">المساهمة</a>
            </div>
            <div class="support-option">
              <i class="fas fa-share-alt"></i>
              <h3>مشاركة</h3>
              <p>انشر التطبيق بين أصدقائك</p>
              <div class="social-share">
                <button><i class="fab fa-twitter"></i></button>
                <button><i class="fab fa-facebook"></i></button>
                <button><i class="fab fa-whatsapp"></i></button>
              </div>
            </div>
          </div>
        </div>
      `;
    } else {
      // Home page
      this.contentContainer.appendChild(renderHomePage());
      this.toggleSidebar = this.contentContainer.querySelector('.toggle-sidebar') || this.toggleSidebar;
    }
    
    // No need for toggle button anymore as sidebar is always visible
  }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.app = new App();
});