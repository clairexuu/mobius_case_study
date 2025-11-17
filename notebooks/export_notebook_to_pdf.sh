#!/bin/bash
# Export Jupyter notebook to PDF without code cells and with full output

# Usage: ./export_notebook_to_pdf.sh your_notebook.ipynb

if [ $# -eq 0 ]; then
    echo "Usage: $0 <notebook.ipynb>"
    exit 1
fi

NOTEBOOK=$1
OUTPUT="${NOTEBOOK%.ipynb}.pdf"

echo "Exporting $NOTEBOOK to $OUTPUT..."
echo "  - Hiding code cells"
echo "  - Showing all outputs (no truncation)"

# Method 1: Direct nbconvert with options
jupyter nbconvert "$NOTEBOOK" \
    --to pdf \
    --no-input \
    --output "$OUTPUT"

echo "Done! PDF saved as: $OUTPUT"
