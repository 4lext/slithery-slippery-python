"""
PNG to SVG Converter
====================

This module provides functionality to convert PNG images to SVG vector graphics
using the Potrace library for bitmap tracing.

Dependencies:
    - Python 3.6+
    - PIL/Pillow (for image processing)
    - potrace (external command-line tool for bitmap tracing)

Installation:
    1. Install Python dependencies:
       pip install pillow

    2. Install potrace:
       - Ubuntu/Debian: sudo apt-get install potrace
       - macOS: brew install potrace
       - Windows: Download from http://potrace.sourceforge.net or use WSL

Usage:
    As a command-line tool:
        python png_to_svg.py input.png -o output.svg
        
    As a module:
        from png_to_svg import png_to_svg
        png_to_svg('input.png', 'output.svg')

Command-line Arguments:
    input_file      : Path to the input PNG file (required)
    -o, --output    : Path to the output SVG file (optional)
    --keep-temp     : Keep temporary files created during conversion (optional)

Notes:
    - The conversion process works best with high contrast images
    - Images are converted to grayscale before processing
    - Complex images may result in large SVG files
    - For better results with detailed images, pre-process the PNG to increase contrast

Author: Alex Towery
Version: 1.0.0
License: MIT
"""
import os
import subprocess
import tempfile
from PIL import Image
import argparse

def png_to_svg(input_file, output_file=None, keep_temp_files=False):
    """
    Convert a PNG file to SVG using potrace.
    
    Args:
        input_file (str): Path to the input PNG file
        output_file (str, optional): Path to the output SVG file. If None, uses the same name as input with .svg extension
        keep_temp_files (bool): Whether to keep temporary files created during conversion
    
    Returns:
        str: Path to the output SVG file
    """
    # Validate input file
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Set default output file if none specified
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + '.svg'
    
    # Create a temporary directory for processing
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Step 1: Open the PNG and convert to BMP (potrace requires BMP or PNM)
        img = Image.open(input_file)
        
        # Convert to grayscale if it's not already
        if img.mode != 'L':
            img = img.convert('L')
        
        # Save as BMP in temp directory
        bmp_path = os.path.join(temp_dir, 'temp.bmp')
        img.save(bmp_path)
        
        # Step 2: Use potrace to convert BMP to SVG
        subprocess.run(['potrace', 
                        '--svg', 
                        '--output', output_file, 
                        bmp_path], 
                       check=True)
        
        print(f"Successfully converted {input_file} to {output_file}")
        return output_file
    
    except Exception as e:
        print(f"Error during conversion: {e}")
        raise
    
    finally:
        # Clean up temporary files
        if not keep_temp_files:
            try:
                bmp_path = os.path.join(temp_dir, 'temp.bmp')
                if os.path.exists(bmp_path):
                    os.remove(bmp_path)
                os.rmdir(temp_dir)
            except Exception as e:
                print(f"Warning: Could not clean up temporary files: {e}")

def main():
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Convert PNG to SVG')
    parser.add_argument('input_file', help='Path to the input PNG file')
    parser.add_argument('-o', '--output', help='Path to the output SVG file')
    parser.add_argument('--keep-temp', action='store_true', 
                        help='Keep temporary files created during conversion')
    
    args = parser.parse_args()
    
    # Run the conversion
    png_to_svg(args.input_file, args.output, args.keep_temp)

if __name__ == "__main__":
    main()
