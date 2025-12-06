//! Sandboxing for secure layer execution

use super::{Layer, LayerError, Result};
use std::path::{Path, PathBuf};
use std::collections::HashSet;
use std::fs;
use log::{info, warn, error};

/// Represents the permissions granted to a sandboxed layer
#[derive(Debug, Clone)]
pub struct SandboxPermissions {
    /// Whether the layer can access the network
    pub network_access: bool,
    /// Allowed filesystem paths (whitelist)
    pub allowed_paths: HashSet<PathBuf>,
    /// Maximum memory usage in bytes (None for unlimited)
    pub max_memory: Option<usize>,
    /// Maximum CPU usage as a percentage (1-100, None for unlimited)
    pub max_cpu: Option<u8>,
}

impl Default for SandboxPermissions {
    fn default() -> Self {
        Self {
            network_access: false,
            allowed_paths: HashSet::new(),
            max_memory: Some(256 * 1024 * 1024), // 256MB default
            max_cpu: Some(50), // 50% CPU max by default
        }
    }
}

/// Represents a sandboxed execution environment for a layer
pub struct LayerSandbox {
    layer: Layer,
    permissions: SandboxPermissions,
    working_dir: PathBuf,
}

impl LayerSandbox {
    /// Creates a new sandbox for the given layer
    pub fn new(layer: Layer, permissions: SandboxPermissions) -> Result<Self> {
        // Create a working directory for the sandbox
        let working_dir = std::env::temp_dir()
            .join("zerometa")
            .join(&layer.id);
        
        if !working_dir.exists() {
            fs::create_dir_all(&working_dir).map_err(|e| {
                LayerError::Io(std::io::Error::new(
                    std::io::ErrorKind::Other,
                    format!("Failed to create sandbox directory: {}", e)
                ))
            })?;
        }
        
        Ok(Self {
            layer,
            permissions,
            working_dir,
        })
    }
    
    /// Executes a command within the sandbox
    pub fn execute(&self, command: &str, args: &[&str]) -> Result<std::process::Output> {
        self.check_permissions(command, args)?;
        
        let output = std::process::Command::new(command)
            .args(args)
            .current_dir(&self.working_dir)
            .output()
            .map_err(|e| LayerError::Io(e))?;
            
        Ok(output)
    }
    
    /// Checks if the requested operation is allowed by the sandbox permissions
    fn check_permissions(&self, command: &str, args: &[&str]) -> Result<()> {
        // Check if the command is in an allowed path
        let command_path = Path::new(command);
        if command_path.is_absolute() && !self.is_path_allowed(command_path) {
            return Err(LayerError::PermissionDenied(
                format!("Command not in allowed paths: {}", command)
            ));
        }
        
        // Check for any file access in arguments
        for arg in args {
            if let Some(path) = self.extract_path(arg) {
                if !self.is_path_allowed(&path) {
                    return Err(LayerError::PermissionDenied(
                        format!("Access to path not allowed: {}", path.display())
                    ));
                }
            }
        }
        
        Ok(())
    }
    
    /// Extracts a path from a command-line argument if it looks like a file path
    fn extract_path(&self, arg: &str) -> Option<PathBuf> {
        // Simple heuristic: if it looks like a path (starts with /, ./, or ~/)
        if arg.starts_with('/') || arg.starts_with("./") || arg.starts_with("~/") {
            Some(PathBuf::from(arg))
        } else {
            None
        }
    }
    
    /// Checks if a path is allowed by the sandbox permissions
    fn is_path_allowed(&self, path: &Path) -> bool {
        // Always allow access to the sandbox working directory
        if path.starts_with(&self.working_dir) {
            return true;
        }
        
        // Check against allowed paths
        self.permissions.allowed_paths.iter().any(|allowed| {
            path.starts_with(allowed)
        })
    }
    
    /// Gets the working directory of the sandbox
    pub fn working_dir(&self) -> &Path {
        &self.working_dir
    }
    
    /// Gets a reference to the layer
    pub fn layer(&self) -> &Layer {
        &self.layer
    }
    
    /// Gets a reference to the permissions
    pub fn permissions(&self) -> &SandboxPermissions {
        &self.permissions
    }
}

/// Manages multiple sandboxes
pub struct SandboxManager {
    sandboxes: std::collections::HashMap<String, LayerSandbox>,
}

impl SandboxManager {
    /// Creates a new SandboxManager
    pub fn new() -> Self {
        Self {
            sandboxes: std::collections::HashMap::new(),
        }
    }
    
    /// Creates a new sandbox for a layer
    pub fn create_sandbox(
        &mut self,
        layer: Layer,
        permissions: SandboxPermissions,
    ) -> Result<()> {
        if self.sandboxes.contains_key(&layer.id) {
            return Err(LayerError::AlreadyExists(layer.id));
        }
        
        let sandbox = LayerSandbox::new(layer, permissions)?;
        self.sandboxes.insert(sandbox.layer().id.clone(), sandbox);
        
        Ok(())
    }
    
    /// Removes a sandbox
    pub fn remove_sandbox(&mut self, layer_id: &str) -> Result<()> {
        self.sandboxes.remove(layer_id)
            .ok_or_else(|| LayerError::NotFound(layer_id.to_string()))?;
        
        Ok(())
    }
    
    /// Gets a reference to a sandbox
    pub fn get_sandbox(&self, layer_id: &str) -> Option<&LayerSandbox> {
        self.sandboxes.get(layer_id)
    }
    
    /// Gets a mutable reference to a sandbox
    pub fn get_sandbox_mut(&mut self, layer_id: &str) -> Option<&mut LayerSandbox> {
        self.sandboxes.get_mut(layer_id)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::tempdir;
    
    fn create_test_layer() -> Layer {
        Layer {
            id: "test-layer".to_string(),
            name: "Test Layer".to_string(),
            description: "A test layer".to_string(),
            version: "1.0.0".to_string(),
            enabled: true,
            path: PathBuf::from("/tmp/layer"),
        }
    }
    
    #[test]
    fn test_sandbox_creation() {
        let layer = create_test_layer();
        let permissions = SandboxPermissions::default();
        let sandbox = LayerSandbox::new(layer, permissions).unwrap();
        
        assert_eq!(sandbox.layer().id, "test-layer");
        assert!(sandbox.working_dir().to_string_lossy().contains("zerometa/test-layer"));
    }
    
    #[test]
    fn test_sandbox_manager() {
        let mut manager = SandboxManager::new();
        let layer = create_test_layer();
        let permissions = SandboxPermissions::default();
        
        manager.create_sandbox(layer, permissions).unwrap();
        assert!(manager.get_sandbox("test-layer").is_some());
        
        manager.remove_sandbox("test-layer").unwrap();
        assert!(manager.get_sandbox("test-layer").is_none());
    }
}