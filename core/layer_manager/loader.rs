//! Layer loading and management

use super::{Layer, LayerError, Result};
use libloading::{Library, Symbol};
use std::path::{Path, PathBuf};
use std::sync::Arc;
use log::{info, error, debug};

/// Represents a loaded layer's code and resources
pub struct LoadedLayer {
    /// The layer's metadata
    pub layer: Layer,
    /// The loaded library (if any)
    library: Option<Library>,
    /// Path to the layer's directory
    path: PathBuf,
}

impl Drop for LoadedLayer {
    fn drop(&mut self) {
        // When the loaded layer is dropped, unload the library
        if self.library.take().is_some() {
            info!("Unloaded layer: {}", self.layer.id);
        }
    }
}

impl LoadedLayer {
    /// Creates a new loaded layer from a layer description
    pub fn new(layer: Layer) -> Result<Self> {
        Ok(Self {
            layer,
            library: None,
            path: PathBuf::new(),
        })
    }

    /// Loads the layer's code into memory
    pub fn load(&mut self) -> Result<()> {
        if self.library.is_some() {
            return Ok(()); // Already loaded
        }

        // Skip loading if there's no library to load
        if !self.path.join("lib").exists() {
            info!("No library to load for layer: {}", self.layer.id);
            return Ok(());
        }

        // TODO: Implement platform-specific library loading
        // This is a simplified example; in a real implementation, you'd need to
        // handle different platforms and file extensions
        #[cfg(target_os = "linux")]
        let lib_path = self.path.join("lib").join(format!("lib{}.so", self.layer.id));
        
        #[cfg(target_os = "macos")]
        let lib_path = self.path.join("lib").join(format!("lib{}.dylib", self.layer.id));
        
        #[cfg(target_os = "windows")]
        let lib_path = self.path.join("lib").join(format!("{}.dll", self.layer.id));

        if !lib_path.exists() {
            return Err(LayerError::InvalidLayer(
                format!("Library not found at {}", lib_path.display())
            ));
        }

        unsafe {
            let library = Library::new(&lib_path)
                .map_err(|e| LayerError::InvalidLayer(
                    format!("Failed to load library: {}", e)
                ))?;

            // Verify the layer's entry points exist
            let _: Symbol<unsafe extern "C" fn()> = library.get(b"layer_initialize")
                .map_err(|_| LayerError::InvalidLayer(
                    "Missing required symbol: layer_initialize".to_string()
                ))?;

            self.library = Some(library);
            info!("Loaded layer: {}", self.layer.id);
        }

        Ok(())
    }

    /// Unloads the layer's code from memory
    pub fn unload(&mut self) -> Result<()> {
        if self.library.take().is_some() {
            info!("Unloaded layer: {}", self.layer.id);
        }
        Ok(())
    }

    /// Calls the layer's initialization function
    pub fn initialize(&self) -> Result<()> {
        if let Some(ref lib) = self.library {
            unsafe {
                let init: Symbol<unsafe extern "C" fn()> = lib.get(b"layer_initialize")
                    .map_err(|_| LayerError::InvalidLayer(
                        "Missing required symbol: layer_initialize".to_string()
                    ))?;
                
                init();
                info!("Initialized layer: {}", self.layer.id);
            }
        }
        Ok(())
    }
}

/// Manages loading and unloading of layers
pub struct LayerLoader {
    layers: Vec<LoadedLayer>,
}

impl Default for LayerLoader {
    fn default() -> Self {
        Self::new()
    }
}

impl LayerLoader {
    /// Creates a new LayerLoader
    pub fn new() -> Self {
        Self { layers: Vec::new() }
    }

    /// Loads a layer
    pub fn load_layer(&mut self, layer: Layer) -> Result<()> {
        let mut loaded_layer = LoadedLayer::new(layer)?;
        loaded_layer.load()?;
        loaded_layer.initialize()?;
        self.layers.push(loaded_layer);
        Ok(())
    }

    /// Unloads a layer by ID
    pub fn unload_layer(&mut self, layer_id: &str) -> Result<()> {
        if let Some(pos) = self.layers.iter().position(|l| l.layer.id == layer_id) {
            let mut layer = self.layers.remove(pos);
            layer.unload()?;
            info!("Unloaded layer: {}", layer_id);
            Ok(())
        } else {
            Err(LayerError::NotFound(layer_id.to_string()))
        }
    }

    /// Gets a reference to a loaded layer
    pub fn get_layer(&self, layer_id: &str) -> Option<&LoadedLayer> {
        self.layers.iter().find(|l| l.layer.id == layer_id)
    }

    /// Gets a mutable reference to a loaded layer
    pub fn get_layer_mut(&mut self, layer_id: &str) -> Option<&mut LoadedLayer> {
        self.layers.iter_mut().find(|l| l.layer.id == layer_id)
    }

    /// Returns an iterator over all loaded layers
    pub fn layers(&self) -> impl Iterator<Item = &LoadedLayer> {
        self.layers.iter()
    }

    /// Returns a mutable iterator over all loaded layers
    pub fn layers_mut(&mut self) -> impl Iterator<Item = &mut LoadedLayer> {
        self.layers.iter_mut()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::tempdir;
    use std::fs;

    #[test]
    fn test_loaded_layer() {
        let layer = Layer {
            id: "test".to_string(),
            name: "Test Layer".to_string(),
            description: "A test layer".to_string(),
            version: "1.0.0".to_string(),
            enabled: true,
            path: PathBuf::from("/tmp/layer"),
        };

        let loaded = LoadedLayer::new(layer).unwrap();
        assert_eq!(loaded.layer.id, "test");
    }