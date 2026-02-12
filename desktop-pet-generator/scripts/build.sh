#!/bin/bash
# Build and Package Script for Desktop Pet Generator outputs

set -e

OUTPUT_DIR=${1:-"./output"}

if [ ! -d "$OUTPUT_DIR" ]; then
    echo "❌ Output directory not found: $OUTPUT_DIR"
    exit 1
fi

echo "🔨 Building Desktop Pet Packages"
echo "================================"

cd "$OUTPUT_DIR"

# Package browser extension
if [ -d "extension" ]; then
    echo "📦 Packaging browser extension..."
    cd extension
    zip -r ../desktop-pet-extension.zip . -x "*.DS_Store"
    cd ..
    echo "✅ Extension package: desktop-pet-extension.zip"
fi

# Build Electron app
if [ -d "desktop-app" ]; then
    echo "🖥️  Building Electron desktop app..."
    cd desktop-app

    if [ ! -d "node_modules" ]; then
        echo "📥 Installing dependencies..."
        npm install
    fi

    echo "📦 Building executables..."
    npm run build 2>/dev/null || npm run dist 2>/dev/null || {
        echo "⚠️  No build script found. Creating installers manually..."

        # Install electron-builder if not present
        npm install --save-dev electron-builder

        # Create build script
        cat > package-tmp.json << 'EOF'
{
  "name": "desktop-pet",
  "version": "1.0.0",
  "main": "main.js",
  "scripts": {
    "start": "electron .",
    "build": "electron-builder --dir",
    "dist": "electron-builder"
  },
  "build": {
    "appId": "com.desktop-pet.app",
    "productName": "Desktop Pet",
    "directories": {
      "output": "dist"
    },
    "files": [
      "**/*",
      "!**/{.git,node_modules,dist,build}/*"
    ],
    "mac": {
      "category": "public.app-category.entertainment",
      "icon": "icon.icns",
      "target": ["dmg", "zip"]
    },
    "win": {
      "icon": "icon.ico",
      "target": ["nsis", "portable"]
    },
    "linux": {
      "icon": "icon.png",
      "target": ["AppImage", "deb"],
      "category": "Utility"
    }
  }
}
EOF

        # Merge with existing package.json
        if command -v jq &> /dev/null; then
            jq -s '.[0] * .[1]' package.json package-tmp.json > package-new.json
            mv package-new.json package.json
        else
            mv package-tmp.json package.json
        fi

        rm -f package-tmp.json

        # Run build
        npm run dist
    }

    cd ..

    if [ -d "desktop-app/dist" ]; then
        echo "✅ Desktop app builds available in: desktop-app/dist/"
        ls -lh desktop-app/dist/
    fi
fi

echo ""
echo "================================"
echo "✨ Build Complete!"
echo "================================"
echo ""
echo "📦 Generated packages:"
[ -f "desktop-pet-extension.zip" ] && echo "   - desktop-pet-extension.zip (Browser Extension)"
[ -d "desktop-app/dist" ] && echo "   - desktop-app/dist/ (Desktop Apps)"
echo ""
echo "🚀 Installation:"
echo "   Web: Open index.html"
echo "   Extension: Load unpacked from extension/ folder"
echo "   Desktop: Install from desktop-app/dist/"
