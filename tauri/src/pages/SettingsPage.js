export function renderSettingsPage() {
  const settingsPage = document.createElement('div');
  settingsPage.className = 'page-content';
  
  settingsPage.innerHTML = `
    <div class="page-header">
      <h2>Settings</h2>
    </div>
    <div class="settings-container">
      <div class="settings-section">
        <h3>General Settings</h3>
        <div class="setting-item">
          <label>Theme</label>
          <select>
            <option>Light</option>
            <option>Dark</option>
            <option>System</option>
          </select>
        </div>
        <div class="setting-item">
          <label>Language</label>
          <select>
            <option>English</option>
            <option>العربية</option>
          </select>
        </div>
      </div>
      
      <div class="settings-section">
        <h3>Map Settings</h3>
        <div class="setting-item">
          <label>Default Zoom Level</label>
          <input type="range" min="1" max="20" value="10" class="slider">
        </div>
        <div class="setting-item">
          <label>Cache Size</label>
          <button class="btn btn-secondary">Clear Cache</button>
        </div>
      </div>
    </div>
  `;
  
  return settingsPage;
}
