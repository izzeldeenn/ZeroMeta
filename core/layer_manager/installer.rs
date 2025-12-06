//! Layer installation and management

use super::{Layer, LayerError, Result};
use std::fs;
use std::path::{Path, PathBuf};
use log::{info, error, warn};
use semver::Version;
use serde_json;
use flate2::read::GzDecoder;
use tar::Archive;
use zip::ZipArchive;
use std::io::{self, Read, Write};
use std::fs::File;

/// Manages installation and removal of layers
pub struct LayerInstaller {
    /// Directory where layers are installed
    layers_dir: PathBuf,
}

impl LayerInstaller {
    /// Creates a new LayerInstaller that will install layers to the specified directory
    pub fn new(layers_dir: impl AsRef<Path>) -> Self {
        Self {
            layers_dir: layers_dir.as_ref().to_path_buf(),
        }
    }

    /// Installs a layer from a local directory
    pub fn install_from_dir(&self, source_dir: &Path, overwrite: bool) -> Result<Layer> {
        info!("Installing layer from directory: {}", source_dir.display());
        
        // Validate the layer directory
        let layer = self.validate_layer_dir(source_dir)?;
        
        // Create the target directory
        let target_dir = self.layers_dir.join(&layer.id);
        
        if target_dir.exists() {
            if !overwrite {
                return Err(LayerError::AlreadyExists(layer.id));
            }
            fs::remove_dir_all(&target_dir).map_err(LayerError::Io)?;
        }
        
        // Copy the layer files
        self.copy_dir_all(source_dir, &target_dir)?;
        
        info!("Installed layer: {} v{}", layer.name, layer.version);
        Ok(layer)
    }
    
    /// Installs a layer from a tarball (.tar.gz)
    pub fn install_from_tar_gz<R: Read>(&self, source: R, overwrite: bool) -> Result<Layer> {
        info!("Installing layer from tarball");
        
        let temp_dir = tempfile::tempdir().map_err(LayerError::Io)?;
        let gz = GzDecoder::new(source);
        let mut archive = Archive::new(gz);
        
        archive.unpack(temp_dir.path()).map_err(|e| {
            LayerError::InvalidLayer(format!("Failed to extract tarball: {}", e))
        })?;
        
        // Find the layer directory in the extracted files
        let layer_dir = self.find_layer_dir(temp_dir.path())?;
        self.install_from_dir(&layer_dir, overwrite)
    }
    
    /// Installs a layer from a zip file
    pub fn install_from_zip<R: Read + io::Seek>(&self, source: R, overwrite: bool) -> Result<Layer> {
        info!("Installing layer from zip file");
        
        let temp_dir = tempfile::tempdir().map_err(LayerError::Io)?;
        let mut archive = ZipArchive::new(source).map_err(|e| {
            LayerError::InvalidLayer(format!("Invalid zip file: {}", e))
        })?;
        
        archive.extract(temp_dir.path()).map_err(|e| {
            LayerError::InvalidLayer(format!("Failed to extract zip file: {}", e))
        })?;
        
        // Find the layer directory in the extracted files
        let layer_dir = self.find_layer_dir(temp_dir.path())?;
        self.install_from_dir(&layer_dir, overwrite)
    }
    
    /// Uninstalls a layer by ID
    pub fn uninstall_layer(&self, layer_id: &str) -> Result<()> {
        let layer_dir = self.layers_dir.join(layer_id);
        
        if !layer_dir.exists() {
            return Err(LayerError::NotFound(layer_id.to_string()));
        }
        
        // Read the manifest to get layer info before deleting
        let manifest_path = layer_dir.join("manifest.json");
        let layer: Layer = if let Ok(manifest) = fs::read_to_string(&manifest_path) {
            serde_json::from_str(&manifest).unwrap_or_else(|_| Layer {
                id: layer_id.to_string(),
                name: layer_id.to_string(),
                description: "Unknown".to_string(),
                version: "0.0.0".to_string(),
                enabled: false,
                path: layer_dir.clone(),
            })
        } else {
            Layer {
                id: layer_id.to_string(),
                name: layer_id.to_string(),
                description: "Unknown".to_string(),
                version: "0.0.0".to_string(),
                enabled: false,
                path: layer_dir.clone(),
            }
        };
        
        // Remove the layer directory
        fs::remove_dir_all(&layer_dir).map_err(LayerError::Io)?;
        
        info!("Uninstalled layer: {} v{}", layer.name, layer.version);
        Ok(())
    }
    
    /// Validates a layer directory and returns the layer information
    fn validate_layer_dir(&self, dir: &Path) -> Result<Layer> {
        let manifest_path = dir.join("manifest.json");
        if !manifest_path.exists() {
            return Err(LayerError::InvalidLayer(
                format!("Manifest not found in {}", dir.display())
            ));
        }
        
        let manifest_content = fs::read_to_string(&manifest_path).map_err(LayerError::Io)?;
        let mut layer: Layer = serde_json::from_str(&manifest_content).map_err(|e| {
            LayerError::InvalidLayer(format!("Invalid manifest: {}", e))
        })?;
        
        // Validate the version string
        if Version::parse(&layer.version).is_err() {
            return Err(LayerError::InvalidLayer(
                format!("Invalid version format: {}", layer.version)
            ));
        }
        
        // Store the full path
        layer.path = dir.to_path_buf();
        
        Ok(layer)
    }
    
    /// Recursively copies a directory
    fn copy_dir_all(&self, src: &Path, dst: &Path) -> Result<()> {
        fs::create_dir_all(dst).map_err(LayerError::Io)?;
        
        for entry in fs::read_dir(src).map_err(LayerError::Io)? {
            let entry = entry.map_err(LayerError::Io)?;
            let ty = entry.file_type().map_err(LayerError::Io)?;
            let src_path = entry.path();
            let dst_path = dst.join(entry.file_name());
            
            if ty.is_dir() {
                self.copy_dir_all(&src_path, &dst_path)?;
            } else {
                fs::copy(&src_path, &dst_path).map_err(LayerError::Io)?;
            }
        }
        
        Ok(())
    }
    
    /// Finds the layer directory in the extracted archive
    fn find_layer_dir(&self, dir: &Path) -> Result<PathBuf> {
        // Check if the directory itself contains a manifest
        if dir.join("manifest.json").exists() {
            return Ok(dir.to_path_buf());
        }
        
        // Look for a single subdirectory that contains a manifest
        let mut entries = fs::read_dir(dir).map_err(LayerError::Io)?;
        
        if let Some(entry) = entries.next() {
            let entry = entry.map_err(LayerError::Io)?;
            let path = entry.path();
            
            if path.is_dir() && path.join("manifest.json").exists() {
                return Ok(path);
            }
        }
        
        Err(LayerError::InvalidLayer(
            "Could not find layer directory in archive".to_string()
        ))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::tempdir;
    
    #[test]
    fn test_validate_layer_dir() {
        let temp_dir = tempdir().unwrap();
        let layer_dir = temp_dir.path().join("test-layer");
        fs::create_dir_all(&layer_dir).unwrap();
        
        let manifest = r#"{
            "id": "test-layer",
            "name": "Test Layer",
            "description": "A test layer",
            "version": "1.0.0",
            "enabled": false
        }"#;
        
        fs::write(layer_dir.join("manifest.json"), manifest).unwrap();
        
        let installer = LayerInstaller::new("/tmp/layers");
        let layer = installer.validate_layer_dir(&layer_dir).unwrap();
        
        assert_eq!(layer.id, "test-layer");
        assert_eq!(layer.name, "Test Layer");
        assert_eq!(layer.version, "1.0.0");
    }
}