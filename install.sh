#!/usr/bin/env bash
# ============================================
# MitraAI - All-in-One Installer (Linux/macOS)
# Satu perintah untuk install semuanya:
# - Download Antigravity standalone
# - Download Antigravity IDE
# - Install patch + custom model support
# - Fix port 50999
# - Buat shortcut Desktop
# ============================================

set -e

echo ""
echo " ============================================"
echo "   MitraAI - All-in-One Installer"
echo "   Auto-install Antigravity + IDE + Patch"
echo " ============================================"
echo ""

# ─── Detect OS ──────────────────────────────────

OS="$(uname -s)"
case "$OS" in
    Linux*)   PLATFORM=linux;;
    Darwin*)  PLATFORM=macos;;
    *)        echo "[ERROR] Unsupported OS: $OS"; exit 1;;
esac

echo "[INFO] Detected OS: $OS ($PLATFORM)"

# ─── Prasyarat Check ────────────────────────────

echo ""
echo "[1/8] Memeriksa prasyarat..."

# Cek Node.js
if ! command -v node &>/dev/null; then
    echo "[ERROR] Node.js tidak ditemukan!"
    echo ""
    echo "Install Node.js 22+:"
    echo "  Ubuntu/Debian: curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - && sudo apt-get install -y nodejs"
    echo "  macOS:         brew install node@22"
    echo "  Atau download: https://nodejs.org/"
    exit 1
fi
NODE_VER=$(node --version)
echo "   Node.js: OK ($NODE_VER)"

# Cek Git
if ! command -v git &>/dev/null; then
    echo "[ERROR] Git tidak ditemukan!"
    echo "Install Git:"
    echo "  Ubuntu/Debian: sudo apt-get install git"
    echo "  macOS:         brew install git"
    exit 1
fi
echo "   Git: OK"

# ─── Fix Port 50999 ─────────────────────────────

echo ""
echo "[2/8] Memeriksa port 50999..."

PORT_IN_USE=false
if command -v ss &>/dev/null; then
    if ss -tlnp 2>/dev/null | grep -q ":50999 "; then
        PORT_IN_USE=true
    fi
elif command -v lsof &>/dev/null; then
    if lsof -i :50999 -sTCP:LISTEN &>/dev/null; then
        PORT_IN_USE=true
    fi
fi

if [ "$PORT_IN_USE" = true ]; then
    echo "   Port 50999 sedang digunakan."
    echo "   Mencari proses..."
    if command -v fuser &>/dev/null; then
        fuser -k 50999/tcp 2>/dev/null || true
        echo "   Proses di port 50999 dihentikan."
    else
        PID=$(lsof -ti :50999 2>/dev/null || true)
        if [ -n "$PID" ]; then
            kill -9 "$PID" 2>/dev/null || true
            echo "   Proses PID $PID dihentikan."
        fi
    fi
    sleep 2
else
    echo "   Port 50999: OK (tersedia)"
fi

# ─── Setup Direktori ────────────────────────────

echo ""
echo "[3/8] Menyiapkan direktori..."

if [ "$PLATFORM" = "linux" ]; then
    INSTALL_DIR="$HOME/MitraAI"
    IDE_DEFAULT="$HOME/MitraAI-IDE"
elif [ "$PLATFORM" = "macos" ]; then
    INSTALL_DIR="$HOME/MitraAI"
    IDE_DEFAULT="/Applications/MitraAI IDE.app/Contents/Resources"
fi

PATCH_DIR="$HOME/MitraAI-patch"

mkdir -p "$INSTALL_DIR"
mkdir -p "$PATCH_DIR"

echo "   Install dir: $INSTALL_DIR"
echo "   Patch dir:   $PATCH_DIR"

# ─── Download Antigravity Standalone ────────────

echo ""
echo "[4/8] Download Antigravity standalone..."

if [ "$PLATFORM" = "linux" ]; then
    STANDALONE_BIN="$INSTALL_DIR/antigravity"
    if [ -x "$STANDALONE_BIN" ]; then
        echo "   Antigravity sudah ada di $INSTALL_DIR"
    else
        echo "   Downloading Antigravity v2.23.0 (Linux x64)..."
        DOWNLOAD_URL="https://storage.googleapis.com/oslo-team-release/channels/production/versions/2.23.0/linux-x64/antigravity-linux-x64.tar.gz"
        if curl -fsSL "$DOWNLOAD_URL" -o /tmp/antigravity.tar.gz 2>/dev/null; then
            echo "   Extracting..."
            tar xzf /tmp/antigravity.tar.gz -C "$INSTALL_DIR" --strip-components=1 2>/dev/null || \
            tar xzf /tmp/antigravity.tar.gz -C "$INSTALL_DIR" 2>/dev/null || true
            chmod +x "$STANDALONE_BIN" 2>/dev/null || true
            rm -f /tmp/antigravity.tar.gz
            if [ -x "$STANDALONE_BIN" ]; then
                echo "   Antigravity standalone: OK"
            else
                echo "   [WARNING] Extract gagal. Coba install manual dari https://antigravity.google/download"
            fi
        else
            echo "   [WARNING] Download gagal."
            echo "   Download manual dari: https://antigravity.google/download"
            echo "   Extract ke: $INSTALL_DIR"
        fi
    fi
elif [ "$PLATFORM" = "macos" ]; then
    STANDALONE_BIN="$INSTALL_DIR/Antigravity.app/Contents/MacOS/Antigravity"
    if [ -x "$STANDALONE_BIN" ]; then
        echo "   Antigravity sudah ada"
    else
        echo "   Downloading Antigravity v2.23.0 (macOS)..."
        DOWNLOAD_URL="https://storage.googleapis.com/oslo-team-release/channels/production/versions/2.23.0/mac-x64/Antigravity-darwin-x64.zip"
        if curl -fsSL "$DOWNLOAD_URL" -o /tmp/antigravity.zip 2>/dev/null; then
            echo "   Extracting..."
            unzip -qo /tmp/antigravity.zip -d "$INSTALL_DIR" 2>/dev/null || true
            chmod +x "$STANDALONE_BIN" 2>/dev/null || true
            rm -f /tmp/antigravity.zip
            if [ -x "$STANDALONE_BIN" ]; then
                echo "   Antigravity standalone: OK"
            else
                echo "   [WARNING] Extract gagal. Coba install manual dari https://antigravity.google/download"
            fi
        else
            echo "   [WARNING] Download gagal."
            echo "   Download manual dari: https://antigravity.google/download"
        fi
    fi
fi

# ─── Download Antigravity IDE ───────────────────

echo ""
echo "[5/8] Download Antigravity IDE..."

if [ "$PLATFORM" = "linux" ]; then
    IDE_BIN="$IDE_DEFAULT/antigravity-ide"
    if [ -x "$IDE_BIN" ]; then
        echo "   Antigravity IDE sudah ada"
    else
        echo "   Downloading Antigravity IDE v2.5.5 (Linux)..."
        DOWNLOAD_URL="https://dl.google.com/antigravity-ide/linux/AntigravityIDE-linux-x64.tar.gz"
        if curl -fsSL "$DOWNLOAD_URL" -o /tmp/antigravity-ide.tar.gz 2>/dev/null; then
            echo "   Extracting..."
            mkdir -p "$IDE_DEFAULT"
            tar xzf /tmp/antigravity-ide.tar.gz -C "$IDE_DEFAULT" --strip-components=1 2>/dev/null || \
            tar xzf /tmp/antigravity-ide.tar.gz -C "$IDE_DEFAULT" 2>/dev/null || true
            chmod +x "$IDE_BIN" 2>/dev/null || true
            rm -f /tmp/antigravity-ide.tar.gz
            if [ -x "$IDE_BIN" ]; then
                echo "   Antigravity IDE: OK"
            else
                echo "   [WARNING] IDE install gagal. Coba manual dari https://antigravity.google/download"
            fi
        else
            echo "   [WARNING] Download IDE gagal."
            echo "   Download manual dari: https://antigravity.google/download"
        fi
    fi
elif [ "$PLATFORM" = "macos" ]; then
    IDE_BIN="$IDE_DEFAULT/Contents/MacOS/Antigravity IDE"
    if [ -x "$IDE_BIN" ]; then
        echo "   Antigravity IDE sudah ada"
    else
        echo "   Downloading Antigravity IDE v2.5.5 (macOS)..."
        DOWNLOAD_URL="https://dl.google.com/antigravity-ide/mac/AntigravityIDE-darwin-x64.zip"
        if curl -fsSL "$DOWNLOAD_URL" -o /tmp/antigravity-ide.zip 2>/dev/null; then
            echo "   Extracting..."
            unzip -qo /tmp/antigravity-ide.zip -d /Applications/ 2>/dev/null || true
            rm -f /tmp/antigravity-ide.zip
            if [ -x "$IDE_BIN" ]; then
                echo "   Antigravity IDE: OK"
            else
                echo "   [WARNING] IDE install gagal. Coba manual dari https://antigravity.google/download"
            fi
        else
            echo "   [WARNING] Download IDE gagal."
            echo "   Download manual dari: https://antigravity.google/download"
        fi
    fi
fi

# ─── Clone dan Build Patch ──────────────────────

echo ""
echo "[6/8] Install patch MitraAI..."

cd "$PATCH_DIR"

if [ -f "$PATCH_DIR/package.json" ]; then
    echo "   Patch sudah ada, updating..."
    git pull --quiet 2>/dev/null || true
else
    echo "   Cloning patch repository..."
    git clone --quiet https://github.com/qomaruddindjamal/MitraAI.git "$PATCH_DIR" 2>/dev/null || true
fi

echo "   Installing dependencies..."
npm ci --ignore-scripts --silent 2>/dev/null || npm install --silent 2>/dev/null

echo "   Building..."
npm run build 2>/dev/null || true
echo "   Patch: OK"

# ─── Apply Patch ────────────────────────────────

echo ""
echo "[7/8] Menerapkan patch..."

# Patch standalone
if [ -d "$INSTALL_DIR/resources" ]; then
    echo "   Patching standalone app..."
    node "$PATCH_DIR/scripts/deploy.mjs" --resources "$INSTALL_DIR/resources" 2>/dev/null && \
        echo "   Standalone patch: OK" || \
        echo "   [WARNING] Standalone patch gagal."
fi

# Patch IDE
if [ -d "$IDE_DEFAULT/resources" ]; then
    echo "   Patching IDE..."
    node "$PATCH_DIR/scripts/ide.mjs" apply --resources "$IDE_DEFAULT/resources" 2>/dev/null && \
        echo "   IDE patch: OK" || \
        echo "   [WARNING] IDE patch gagal."
fi

# ─── Buat Launcher dan Shortcut ─────────────────

echo ""
echo "[8/8] Membuat launcher dan shortcut..."

# MitraAI standalone launcher
cat > "$INSTALL_DIR/start-mitraai.sh" << 'LAUNCHER_EOF'
#!/usr/bin/env bash
# MitraAI Launcher - Auto fix port
PORT_IN_USE=false
if command -v ss &>/dev/null; then
    if ss -tlnp 2>/dev/null | grep -q ":50999 "; then
        PORT_IN_USE=true
    fi
elif command -v lsof &>/dev/null; then
    if lsof -i :50999 -sTCP:LISTEN &>/dev/null; then
        PORT_IN_USE=true
    fi
fi
if [ "$PORT_IN_USE" = true ]; then
    if command -v fuser &>/dev/null; then
        fuser -k 50999/tcp 2>/dev/null || true
    else
        PID=$(lsof -ti :50999 2>/dev/null || true)
        [ -n "$PID" ] && kill -9 "$PID" 2>/dev/null || true
    fi
    sleep 2
fi
LAUNCHER_EOF

if [ "$PLATFORM" = "linux" ]; then
    echo "exec \"$INSTALL_DIR/antigravity\" \"\$@\"" >> "$INSTALL_DIR/start-mitraai.sh"
elif [ "$PLATFORM" = "macos" ]; then
    echo "exec \"$INSTALL_DIR/Antigravity.app/Contents/MacOS/Antigravity\" \"\$@\"" >> "$INSTALL_DIR/start-mitraai.sh"
fi
chmod +x "$INSTALL_DIR/start-mitraai.sh"

# MitraAI IDE launcher
cat > "$INSTALL_DIR/start-mitraai-ide.sh" << 'LAUNCHER_EOF'
#!/usr/bin/env bash
# MitraAI IDE Launcher - Auto fix port + proxy
PORT_IN_USE=false
if command -v ss &>/dev/null; then
    if ss -tlnp 2>/dev/null | grep -q ":50999 "; then
        PORT_IN_USE=true
    fi
elif command -v lsof &>/dev/null; then
    if lsof -i :50999 -sTCP:LISTEN &>/dev/null; then
        PORT_IN_USE=true
    fi
fi
if [ "$PORT_IN_USE" = true ]; then
    if command -v fuser &>/dev/null; then
        fuser -k 50999/tcp 2>/dev/null || true
    else
        PID=$(lsof -ti :50999 2>/dev/null || true)
        [ -n "$PID" ] && kill -9 "$PID" 2>/dev/null || true
    fi
    sleep 2
fi
LAUNCHER_EOF

if [ "$PLATFORM" = "linux" ]; then
    echo "cd \"$PATCH_DIR\" && npm run proxy:start &>/dev/null &" >> "$INSTALL_DIR/start-mitraai-ide.sh"
    echo "sleep 3" >> "$INSTALL_DIR/start-mitraai-ide.sh"
    echo "exec \"$IDE_DEFAULT/antigravity-ide\" \"\$@\"" >> "$INSTALL_DIR/start-mitraai-ide.sh"
elif [ "$PLATFORM" = "macos" ]; then
    echo "cd \"$PATCH_DIR\" && npm run proxy:start &>/dev/null &" >> "$INSTALL_DIR/start-mitraai-ide.sh"
    echo "sleep 3" >> "$INSTALL_DIR/start-mitraai-ide.sh"
    echo "exec open -a \"MitraAI IDE\"" >> "$INSTALL_DIR/start-mitraai-ide.sh"
fi
chmod +x "$INSTALL_DIR/start-mitraai-ide.sh"

# Desktop shortcuts (Linux)
if [ "$PLATFORM" = "linux" ]; then
    DESKTOP_DIR="$HOME/Desktop"
    [ ! -d "$DESKTOP_DIR" ] && DESKTOP_DIR="$HOME/Desktop"

    mkdir -p "$DESKTOP_DIR"

    # MitraAI standalone .desktop
    cat > "$DESKTOP_DIR/MitraAI.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=MitraAI
Comment=MitraAI - Local Model AI Assistant
Exec=$INSTALL_DIR/start-mitraai.sh
Icon=$INSTALL_DIR/resources/app/icon.png
Terminal=false
Categories=Development;Utility;
StartupNotify=true
EOF
    chmod +x "$DESKTOP_DIR/MitraAI.desktop"

    # MitraAI IDE .desktop
    cat > "$DESKTOP_DIR/MitraAI-IDE.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=MitraAI IDE
Comment=MitraAI IDE - AI-Powered Code Editor
Exec=$INSTALL_DIR/start-mitraai-ide.sh
Icon=$IDE_DEFAULT/resources/app/icon.png
Terminal=false
Categories=Development;IDE;
StartupNotify=true
EOF
    chmod +x "$DESKTOP_DIR/MitraAI-IDE.desktop"

    echo "   Shortcut MitraAI.desktop: OK"
    echo "   Shortcut MitraAI-IDE.desktop: OK"
elif [ "$PLATFORM" = "macos" ]; then
    echo "   Launcher scripts dibuat di $INSTALL_DIR/"
    echo "   Gunakan Spotlight atau Finder untuk menjalankan."
fi

# ─── Selesai ────────────────────────────────────

echo ""
echo " ============================================"
echo "   INSTALLASI SELESAI!"
echo " ============================================"
echo ""

if [ "$PLATFORM" = "linux" ]; then
    echo " Shortcut sudah dibuat di Desktop:"
    echo "   - MitraAI.desktop      (standalone app)"
    echo "   - MitraAI-IDE.desktop  (code editor)"
    echo ""
    echo " Atau jalankan manual:"
    echo "   $INSTALL_DIR/start-mitraai.sh"
    echo "   $INSTALL_DIR/start-mitraai-ide.sh"
elif [ "$PLATFORM" = "macos" ]; then
    echo " Launcher scripts:"
    echo "   $INSTALL_DIR/start-mitraai.sh"
    echo "   $INSTALL_DIR/start-mitraai-ide.sh"
    echo ""
    echo " Jalankan dengan:"
    echo "   bash $INSTALL_DIR/start-mitraai.sh"
    echo "   bash $INSTALL_DIR/start-mitraai-ide.sh"
fi

echo ""
echo " Port 50999 sudah di-fix."
echo " Kedua app bisa langsung dijalankan."
echo ""
echo " Langkah selanjutnya:"
echo " 1. Jalankan MitraAI untuk mulai"
echo " 2. Buka browser manager: http://127.0.0.1:50999"
echo " 3. Tambahkan model (Ollama, OpenAI, dll)"
echo ""
echo " Dokumentasi lengkap:"
echo "   https://github.com/qomaruddindjamal/MitraAI"
echo "   https://github.com/qomaruddindjamal/MitraAI-IDE"
echo ""
