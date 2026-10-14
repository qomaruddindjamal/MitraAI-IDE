#!/bin/bash
# ============================================
# MitraAI IDE - Setup Script (Linux/macOS)
# Membuat shortcut di Desktop setelah install
# ============================================

set -euo pipefail

echo "========================================"
echo "  MitraAI IDE - Setup"
echo "========================================"
echo

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Cek Node.js
if ! command -v node &>/dev/null; then
    echo "ERROR: Node.js tidak ditemukan."
    echo "Install dari https://nodejs.org/"
    exit 1
fi

# Install dependencies
echo "Menginstall dependencies..."
npm ci --ignore-scripts

# Build
echo "Building project..."
npm run build

# Deteksi path IDE
IDE_PATH=""
if [ -d "$HOME/.local/share/antigravity-ide" ]; then
    IDE_PATH="$HOME/.local/share/antigravity-ide"
elif [ -d "/usr/share/antigravity-ide" ]; then
    IDE_PATH="/usr/share/antigravity-ide"
elif [ -d "/Applications/Antigravity IDE.app" ]; then
    IDE_PATH="/Applications/Antigravity IDE.app/Contents/Resources"
fi

# Buat shortcut di Desktop
DESKTOP_DIR="$HOME/Desktop"
if [ ! -d "$DESKTOP_DIR" ]; then
    DESKTOP_DIR="$HOME"
fi

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    EXEC_CMD="antigravity-ide"
    if [ -n "$IDE_PATH" ] && [ -f "$IDE_PATH/antigravity-ide" ]; then
        EXEC_CMD="$IDE_PATH/antigravity-ide"
    fi

    cat > "$DESKTOP_DIR/mitraai-ide.desktop" << EOF
[Desktop Entry]
Name=MitraAI IDE
Comment=AI-Powered Code Editor with Local Models
Exec=bash -c 'cd "$SCRIPT_DIR" && npm run proxy:start > /dev/null 2>&1 & sleep 2 && $EXEC_CMD'
Icon=$SCRIPT_DIR/icon.png
Terminal=false
Type=Application
Categories=Development;IDE;
StartupNotify=true
EOF
    chmod +x "$DESKTOP_DIR/mitraai-ide.desktop"

    if command -v gio &>/dev/null; then
        gio set "$DESKTOP_DIR/mitraai-ide.desktop" metadata::trusted true 2>/dev/null || true
    fi

elif [[ "$OSTYPE" == "darwin"* ]]; then
    APP_DIR="$DESKTOP_DIR/MitraAI IDE.app"
    mkdir -p "$APP_DIR/Contents/MacOS"

    cat > "$APP_DIR/Contents/MacOS/MitraAIIDE" << EOF
#!/bin/bash
cd "$SCRIPT_DIR"
npm run proxy:start > /dev/null 2>&1 &
sleep 2
open "/Applications/Antigravity IDE.app" 2>/dev/null || echo "Antigravity IDE not found"
EOF
    chmod +x "$APP_DIR/Contents/MacOS/MitraAIIDE"

    cat > "$APP_DIR/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>MitraAIIDE</string>
    <key>CFBundleName</key>
    <string>MitraAI IDE</string>
    <key>CFBundleIdentifier</key>
    <string>com.mitraai.ide</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
</dict>
</plist>
EOF
fi

# Terapkan patch IDE jika ditemukan
if [ -n "$IDE_PATH" ]; then
    echo
    echo "Menerapkan patch IDE..."
    npm run ide:check -- --resources "$IDE_PATH" || true
    npm run ide:apply -- --resources "$IDE_PATH" || true
fi

echo
echo "========================================"
echo "  Setup selesai!"
echo "========================================"
echo
echo "Shortcut sudah dibuat di: $DESKTOP_DIR"
echo
echo "Langkah selanjutnya:"
echo "1. Start proxy: npm run proxy:start -- --open"
echo "2. Tambahkan model di browser manager"
echo "3. Klik shortcut MitraAI IDE"
echo
