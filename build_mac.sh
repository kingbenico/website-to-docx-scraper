#!/bin/bash
echo "================================"
echo " Site to DOCX - macOS Builder"
echo "================================"
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Install from https://python.org"
    exit 1
fi

python3 --version

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt
pip3 install pyinstaller

echo
echo "Building .app ..."
pyinstaller site-to-docx-mac.spec --clean --noconfirm

echo
if [ -d "dist/SiteToDocx.app" ]; then
    echo "SUCCESS! Your .app is at: dist/SiteToDocx.app"
    echo
    echo "To distribute: zip the .app and share it."
    echo "  zip -r SiteToDocx-mac.zip dist/SiteToDocx.app"
else
    echo "FAILED. Check the output above for errors."
    exit 1
fi
