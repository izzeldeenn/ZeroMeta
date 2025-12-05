export function renderHomePage() {
  const mainContent = document.createElement('div');
  mainContent.className = 'main-content';
  mainContent.id = 'main-content';
  
  mainContent.innerHTML = `
    <button class="toggle-sidebar" id="toggle-sidebar">
      <i class="fas fa-bars"></i>
    </button>
    <h1>Welcome to ZeroMeta</h1>
    <p>Select layers from the sidebar to get started.</p>
  `;
  
  return mainContent;
}
