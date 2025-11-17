#!/usr/bin/env python3
"""
Export Jupyter notebook to PDF with:
- No code cells
- Full output (no truncation)
- All cells expanded

Usage:
    python export_notebook.py your_notebook.ipynb
"""

import sys
import json
import subprocess
from pathlib import Path


def remove_output_truncation(notebook_path):
    """
    Remove output truncation from notebook by modifying metadata.
    """
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Update notebook metadata to show full outputs
    if 'metadata' not in nb:
        nb['metadata'] = {}

    # Set display options
    nb['metadata']['hide_input'] = True

    # Process each cell
    for cell in nb.get('cells', []):
        # Hide input (code) cells
        if 'metadata' not in cell:
            cell['metadata'] = {}

        if cell['cell_type'] == 'code':
            cell['metadata']['hide_input'] = True

            # Remove scrolled output metadata that causes truncation
            if 'scrolled' in cell['metadata']:
                cell['metadata']['scrolled'] = False

        # Expand all outputs
        if 'outputs' in cell:
            for output in cell['outputs']:
                if 'metadata' not in output:
                    output['metadata'] = {}
                # Remove any truncation metadata
                if 'scrolled' in output.get('metadata', {}):
                    del output['metadata']['scrolled']

    # Save modified notebook
    temp_path = notebook_path.replace('.ipynb', '_temp_export.ipynb')
    with open(temp_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2)

    return temp_path


def export_to_pdf(notebook_path, output_path=None):
    """
    Export notebook to PDF using nbconvert.
    """
    if output_path is None:
        output_path = notebook_path.replace('.ipynb', '.pdf')

    print(f"Exporting {notebook_path} to PDF...")
    print("  Settings:")
    print("    - Hide code cells: YES")
    print("    - Show all outputs: YES")
    print("    - Truncation: DISABLED")

    # Prepare temp notebook with no truncation
    print("\n  Preparing notebook...")
    temp_notebook = remove_output_truncation(notebook_path)

    # Export using nbconvert
    print("  Converting to PDF...")
    cmd = [
        'jupyter', 'nbconvert',
        '--to', 'pdf',
        '--no-input',  # Hide code cells
        '--output', output_path,
        temp_notebook
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"\n✓ Success! PDF saved to: {output_path}")

            # Clean up temp file
            Path(temp_notebook).unlink()

            return True
        else:
            print(f"\n✗ Error during conversion:")
            print(result.stderr)
            return False

    except FileNotFoundError:
        print("\n✗ Error: jupyter nbconvert not found!")
        print("Install it with: pip install nbconvert")
        print("You may also need: pip install pandoc pyppeteer")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python export_notebook.py <notebook.ipynb> [output.pdf]")
        sys.exit(1)

    notebook_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    if not Path(notebook_path).exists():
        print(f"Error: Notebook not found: {notebook_path}")
        sys.exit(1)

    success = export_to_pdf(notebook_path, output_path)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
