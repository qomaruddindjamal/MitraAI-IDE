# Instalasi MitraAI IDE di macOS

## Prasyarat

| Software | Versi Minimum | Cara Install |
|----------|---------------|--------------|
| **macOS** | 12 (Monterey)+ | - |
| **Node.js** | 22.13+ | `brew install node@22` |
| **Git** | 2.30+ | `brew install git` |
| **Antigravity IDE** | 2.5.5 | [antigravity.google/download](https://antigravity.google/download) |
| **Python** | 3.8+ | `brew install python` (opsional) |

## Instalasi

### Langkah 1: Install Homebrew & Dependencies

```bash
# Homebrew (jika belum ada)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Dependencies
brew install node@22 git python3
brew link node@22 --overwrite --force
```

### Langkah 2: Download Antigravity IDE

```bash
# Download .dmg
hdiutil attach ~/Downloads/Antigravity-IDE-darwin.dmg

# Copy ke Applications
cp -R "/Volumes/Antigravity IDE/Antigravity IDE.app" "/Applications/MitraAI IDE.app"
hdiutil detach "/Volumes/Antigravity IDE"

# Hapus quarantine
xattr -cr "/Applications/MitraAI IDE.app"
```

### Langkah 3: Clone dan Build

```bash
git clone https://github.com/qomaruddindjamal/MitraAI-IDE.git ~/MitraAI-IDE-patch
cd ~/MitraAI-IDE-patch

npm ci --ignore-scripts
npm run build
```

### Langkah 4: Terapkan Patch

```bash
chmod +x deploy.sh
./deploy.sh --resources "/Applications/MitraAI IDE.app/Contents/Resources"
```

### Langkah 5: Konfigurasi & Launch

```bash
# Start proxy dengan browser manager
npm run proxy:start -- --open

# MCP setup (opsional)
npm run ide:mcp -- apply

# Launch IDE
npm run ide:launch -- --resources "/Applications/MitraAI IDE.app/Contents/Resources"
```

## Launcher Script

```bash
cat > ~/start-mitraai-ide.sh << 'EOF'
#!/bin/bash
RESOURCES="/Applications/MitraAI IDE.app/Contents/Resources"
PATCH_DIR="$HOME/MitraAI-IDE-patch"

echo "Starting proxy..."
cd "$PATCH_DIR"
npm run proxy:start > /dev/null 2>&1 &
sleep 3

echo "Launching MitraAI IDE..."
open "/Applications/MitraAI IDE.app"
EOF

chmod +x ~/start-mitraai-ide.sh
```

## Instalasi Ollama

```bash
brew install ollama
brew services start ollama
ollama pull qwen2.5-coder:3b
```

## Troubleshooting

### Gatekeeper Warning

```bash
xattr -cr "/Applications/MitraAI IDE.app"
```

### Port 50999

```bash
lsof -i :50999
kill -9 <PID>
```

### Patch Invalid After Move

Patch IDE terikat path. Harus restore dari path lama sebelum apply di path baru.

## Uninstall

```bash
cd ~/MitraAI-IDE-patch
npm run proxy:stop
./deploy.sh --restore --resources "/Applications/MitraAI IDE.app/Contents/Resources"
npm run ide:mcp -- restore

rm -rf "/Applications/MitraAI IDE.app"
rm -rf ~/MitraAI-IDE-patch
rm -rf ~/.gemini/antigravity
rm ~/start-mitraai-ide.sh
```
