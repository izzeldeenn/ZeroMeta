//! Layer management system for ZeroMeta
//! 
//! This module provides functionality for discovering, loading, and managing
//! layers in the ZeroMeta system.

pub mod installer;
pub mod loader;
pub mod registry;
pub mod sandbox;

// Re-exports
pub use installer::*;
pub use loader::*;
pub use registry::*;
pub use sandbox::*;

use serde::{Deserialize, Serialize};
use std::path::PathBuf;

/// Represents a layer in the ZeroMeta system
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Layer {
    /// Unique identifier for the layer
    pub id: String,
    /// Human-readable name
    pub name: String,
    /// Description of the layer's functionality
    pub description: String,
    /// Version string (semver compatible)
    pub version: String,
    /// Whether the layer is currently active
    pub enabled: bool,
    /// Path to the layer's directory
    pub path: PathBuf,
}

/// Error type for layer operations
#[derive(Debug, thiserror::Error)]
pub enum LayerError {
    #[error("I/O error: {0}")]
    Io(#[from] std::io::Error),
    
    #[error("JSON error: {0}")]
    Json(#[from] serde_json::Error),
    
    #[error("Layer not found: {0}")]
    NotFound(String),
    
    #[error("Layer already exists: {0}")]
    AlreadyExists(String),
    
    #[error("Invalid layer: {0}")]
    InvalidLayer(String),
    
    #[error("Permission denied: {0}")]
    PermissionDenied(String),
}

/// Result type for layer operations
pub type Result<T> = std::result::Result<T, LayerError>;
