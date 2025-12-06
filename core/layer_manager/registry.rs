//! Layer registry for discovering and managing installed layers

use super::{Layer, LayerError, Result};
use std::collections::HashMap;
use std::path::{Path, PathBuf};
use std::sync::RwLock;
use log::{info, error};

/// Manages the registry of installed layers
#[derive(Debug, Default)]
pub struct LayerRegistry {
    layers: RwLock<HashMap<String, Layer>>,
    layers_dir: PathBuf,
}

impl LayerRegistry {
    /// Creates a new LayerRegistry that will look for layers in the specified directory
    pub fn new(layers_dir: impl AsRef<Path>) -> Self {
        Self {
            layers: RwLock::new(HashMap::new()),
            layers_dir: layers_dir.as_ref().to_path_buf(),
        }
    }

    /// Discovers and loads all layers from the layers directory
    pub fn discover_layers(&self) -> Result<()> {
        let mut layers = self.layers.write().map_err(|_| LayerError::Io(std::io::Error::new(
            std::io::ErrorKind::Other,
            "Failed to acquire write lock on layers"
        )))?;

        layers.clear();

        if !self.layers_dir.exists() {
            std::fs::create_dir_all(&self.layers_dir).map_err(LayerError::Io)?;
            info!("Created layers directory at: {:?}", self.layers_dir);
            return Ok(());
        }

        for entry in std::fs::read_dir(&self.layers_dir).map_err(LayerError::Io)? {
            let entry = entry.map_err(LayerError::Io)?;
            let path = entry.path();
            
            if path.is_dir() {
                if let Ok(layer) = self.load_layer(&path) {
                    info!("Discovered layer: {} (v{})", layer.name, layer.version);
                    layers.insert(layer.id.clone(), layer);
                } else {
                    error!("Failed to load layer from: {:?}", path);
                }
            }
        }

        Ok(())
    }

    /// Loads a layer from a directory
    fn load_layer(&self, path: &Path) -> Result<Layer> {
        let manifest_path = path.join("manifest.json");
        if !manifest_path.exists() {
            return Err(LayerError::InvalidLayer(
                format!("Manifest not found in {}", path.display())
            ));
        }

        let manifest_content = std::fs::read_to_string(&manifest_path).map_err(LayerError::Io)?;
        let mut layer: Layer = serde_json::from_str(&manifest_content).map_err(LayerError::Json)?;
        
        // Store the full path to the layer
        layer.path = path.to_path_buf();
        
        Ok(layer)
    }

    /// Registers a new layer in the registry
    pub fn register_layer(&self, layer: Layer) -> Result<()> {
        let mut layers = self.layers.write().map_err(|_| LayerError::Io(std::io::Error::new(
            std::io::ErrorKind::Other,
            "Failed to acquire write lock on layers"
        )))?;

        if layers.contains_key(&layer.id) {
            return Err(LayerError::AlreadyExists(layer.id));
        }

        layers.insert(layer.id.clone(), layer);
        Ok(())
    }

    /// Unregisters a layer from the registry
    pub fn unregister_layer(&self, layer_id: &str) -> Result<()> {
        let mut layers = self.layers.write().map_err(|_| LayerError::Io(std::io::Error::new(
            std::io::ErrorKind::Other,
            "Failed to acquire write lock on layers"
        )))?;

        layers.remove(layer_id)
            .ok_or_else(|| LayerError::NotFound(layer_id.to_string()))?;
            
        Ok(())
    }

    /// Gets a layer by ID
    pub fn get_layer(&self, layer_id: &str) -> Result<Option<Layer>> {
        let layers = self.layers.read().map_err(|_| LayerError::Io(std::io::Error::new(
            std::io::ErrorKind::Other,
            "Failed to acquire read lock on layers"
        )))?;
        
        Ok(layers.get(layer_id).cloned())
    }

    /// Lists all registered layers
    pub fn list_layers(&self) -> Result<Vec<Layer>> {
        let layers = self.layers.read().map_err(|_| LayerError::Io(std::io::Error::new(
            std::io::ErrorKind::Other,
            "Failed to acquire read lock on layers"
        )))?;
        
        Ok(layers.values().cloned().collect())
    }

    /// Enables a layer
    pub fn enable_layer(&self, layer_id: &str) -> Result<()> {
        let mut layers = self.layers.write().map_err(|_| LayerError::Io(std::io::Error::new(
            std::io::ErrorKind::Other,
            "Failed to acquire write lock on layers"
        )))?;

        if let Some(layer) = layers.get_mut(layer_id) {
            layer.enabled = true;
            info!("Enabled layer: {}", layer_id);
            Ok(())
        } else {
            Err(LayerError::NotFound(layer_id.to_string()))
        }
    }

    /// Disables a layer
    pub fn disable_layer(&self, layer_id: &str) -> Result<()> {
        let mut layers = self.layers.write().map_err(|_| LayerError::Io(std::io::Error::new(
            std::io::ErrorKind::Other,
            "Failed to acquire write lock on layers"
        )))?;

        if let Some(layer) = layers.get_mut(layer_id) {
            layer.enabled = false;
            info!("Disabled layer: {}", layer_id);
            Ok(())
        } else {
            Err(LayerError::NotFound(layer_id.to_string()))
        }
    }
}