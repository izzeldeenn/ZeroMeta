#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Metadata Remover - A command-line tool to remove metadata from files.

Features:
- Remove metadata from various file types
- Process single files or entire directories
- Preserve or overwrite original files
- Show metadata before removal
"""

import os
import sys
import click
import shutil
from pathlib import Path
from typing import Tuple, Optional, List

# Third-party imports
try:
    from PIL import Image, PngImagePlugin, JpegImagePlugin, ExifTags
    from PIL.ExifTags import TAGS, GPSTAGS
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

class MetadataRemover:
    """Handle metadata removal operations."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.supported_formats = {
            'images': ['.jpg', '.jpeg', '.png', '.tiff', '.webp', '.bmp', '.gif'],
            'documents': ['.pdf', '.doc', '.docx', '.odt', '.xls', '.xlsx', '.odp', '.ppt', '.pptx'],
            'archives': ['.zip', '.tar', '.gz', '.7z', '.rar'],
            'audio': ['.mp3', '.wav', '.ogg', '.flac', '.m4a'],
            'video': ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv']
        }

    def get_supported_extensions(self) -> List[str]:
        """Return a flat list of all supported file extensions."""
        return [ext for exts in self.supported_formats.values() for ext in exts]
    
    def is_supported_file(self, file_path: str) -> bool:
        """Check if the file type is supported."""
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.get_supported_extensions()
    
    def get_metadata(self, file_path: str) -> dict:
        """
        Get metadata from a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary containing the file's metadata
        """
        if not PILLOW_AVAILABLE:
            return {"error": "Pillow library not available. Install with: pip install Pillow"}
            
        try:
            with Image.open(file_path) as img:
                metadata = {
                    "file_info": {
                        "format": img.format,
                        "mode": img.mode,
                        "size": img.size,
                        "width": img.width,
                        "height": img.height
                    },
                    "exif_data": {},
                    "png_metadata": {}
                }
                
                # Get EXIF data if available
                if hasattr(img, '_getexif') and img._getexif():
                    for tag_id, value in img._getexif().items():
                        tag = TAGS.get(tag_id, tag_id)
                        metadata["exif_data"][str(tag)] = value
                
                # Get PNG metadata if available
                if img.format == 'PNG' and hasattr(img, 'info') and img.info:
                    for key, value in img.info.items():
                        if key != 'exif':  # Skip binary EXIF data
                            metadata["png_metadata"][str(key)] = str(value)
                
                return metadata
                
        except Exception as e:
            return {"error": f"Error reading metadata: {str(e)}"}
    
    def show_metadata(self, file_path: str) -> None:
        """Display metadata of an image file using Pillow."""
        metadata = self.get_metadata(file_path)
        if "error" in metadata:
            click.echo(metadata["error"])
            return
            
        click.echo(f"\nMetadata for {file_path}:")
        
        # Show basic info
        if "file_info" in metadata:
            click.echo("\nFile Information:")
            for key, value in metadata["file_info"].items():
                click.echo(f"  {key}: {value}")
        
        # Show EXIF data if available
        if metadata.get("exif_data"):
            click.echo("\nEXIF Data:")
            for tag, value in metadata["exif_data"].items():
                click.echo(f"  {tag}: {value}")
        
        # Show PNG metadata if available
        if metadata.get("png_metadata"):
            click.echo("\nPNG Metadata:")
            for key, value in metadata["png_metadata"].items():
                click.echo(f"  {key}: {value}")
    
    def remove_metadata(self, file_path: str, output_path: Optional[str] = None, 
                       overwrite: bool = False) -> Tuple[bool, str]:
        """
        Remove metadata from a file by creating a clean copy.
        
        Args:
            file_path: Path to the source file
            output_path: Optional output path (default: add '_clean' suffix)
            overwrite: If True, overwrite the original file
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            file_path = os.path.abspath(file_path)
            
            if not os.path.exists(file_path):
                return False, f"File not found: {file_path}"
                
            if not self.is_supported_file(file_path):
                return False, f"Unsupported file type: {file_path}"
            
            if output_path and os.path.isdir(output_path):
                output_path = os.path.join(output_path, os.path.basename(file_path))
            
            if not output_path and not overwrite:
                path = Path(file_path)
                output_path = str(path.parent / f"{path.stem}_clean{path.suffix}")
            elif overwrite:
                output_path = file_path
                
            # Create a clean copy by reading and writing the file
            if self.verbose:
                click.echo(f"Processing: {file_path}")
            
            # Handle image files with Pillow
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                if not PILLOW_AVAILABLE:
                    return False, "Pillow library not available. Install with: pip install Pillow"
                    
                try:
                    with Image.open(file_path) as img:
                        # Create a new image with the same mode and size
                        clean_img = Image.new(img.mode, img.size)
                        # Copy the pixel data
                        clean_img.putdata(list(img.getdata()))
                        
                        # Save without metadata
                        clean_img.save(output_path, exif=img.info.get('exif'))
                        
                except Exception as e:
                    return False, f"Error processing image: {str(e)}"            
            else:
                # For non-image files, just make a copy for now
                shutil.copy2(file_path, output_path)
                
            if self.verbose:
                self.show_metadata(output_path)
                
            return True, output_path
            
        except Exception as e:
            return False, f"Error processing {file_path}: {str(e)}"

    def process_directory(self, directory: str, recursive: bool = False, 
                        output_dir: Optional[str] = None, overwrite: bool = False) -> None:
        """Process all supported files in a directory."""
        if not os.path.isdir(directory):
            click.echo(f"Error: {directory} is not a valid directory")
            return
            
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            
        processed = 0
        errors = 0
        
        for root, _, files in os.walk(directory):
            for file in files:
                if self.is_supported_file(file):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, directory)
                    
                    if output_dir:
                        out_path = os.path.join(output_dir, rel_path)
                        os.makedirs(os.path.dirname(out_path), exist_ok=True)
                    else:
                        out_path = None
                        
                    success, message = self.remove_metadata(
                        file_path, out_path, overwrite
                    )
                    
                    if success:
                        processed += 1
                        if self.verbose:
                            click.echo(message)
                    else:
                        errors += 1
                        click.echo(f"Error: {message}", err=True)
            
            if not recursive:
                break
                
        click.echo(f"\nProcessing complete. {processed} files processed, {errors} errors.")

@click.group(invoke_without_command=True)
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, verbose):
    """Metadata Remover - Remove metadata from files."""
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose
    
    # If no command provided, show help
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file or directory')
@click.option('--overwrite', is_flag=True, help='Overwrite the original file')
@click.option('--show-metadata', is_flag=True, help='Show metadata before removal')
@click.pass_context
def remove(ctx, path, output, overwrite, show_metadata):
    """Remove metadata from a file or directory."""
    remover = MetadataRemover(verbose=ctx.obj['VERBOSE'])
    path = os.path.abspath(path)
    
    if os.path.isfile(path):
        if show_metadata:
            remover.show_metadata(path)
            if not click.confirm('Do you want to proceed with metadata removal?'):
                return
                
        success, message = remover.remove_metadata(path, output, overwrite)
        click.echo(message)
    elif os.path.isdir(path):
        if output and not os.path.isdir(output):
            click.echo("Error: Output must be a directory when processing a directory")
            return
            
        if not click.confirm(f'Process all supported files in {path}? This may modify files.'):
            return
            
        remover.process_directory(path, recursive=True, output_dir=output, overwrite=overwrite)
    else:
        click.echo(f"Error: {path} is not a valid file or directory")

@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.pass_context
def info(ctx, path):
    """Show metadata information for a file."""
    remover = MetadataRemover(verbose=ctx.obj['VERBOSE'])
    path = os.path.abspath(path)
    
    if not os.path.exists(path):
        click.echo(f"Error: {path} does not exist")
        return
        
    if os.path.isfile(path):
        remover.show_metadata(path)
    else:
        click.echo("Error: Please specify a file, not a directory")

@cli.command()
@click.pass_context
def formats(ctx):
    """List supported file formats."""
    remover = MetadataRemover()
    click.echo("Supported file formats:")
    for category, extensions in remover.supported_formats.items():
        click.echo(f"\n{category.capitalize()}:")
        click.echo(", ".join(extensions))

if __name__ == "__main__":
    cli(obj={})
