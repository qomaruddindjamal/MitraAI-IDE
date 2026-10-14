# Instalasi MitraAI IDE di Linux

## Distribusi yang Didukung

| Distribusi | Versi | Status |
|-----------|-------|--------|
| Ubuntu | 22.04+ | Tested |
| Debian | 12+ | Tested |
| Fedora | 39+ | Tested |
| Arch Linux | Rolling | Tested |
| Linux Mint | 21+ | Tested |

## Prasyarat

### Ubuntu/Debian

```bash
# Update
sudo apt update && sudo apt upgrade -y

# Node.js 22.x
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs git python3 curl

# Verifikasi
node --version  # v22.13+
npm --version   # 10.x+
```

### Fedora

```bash
curl -fsSL https://rpm.nodesource.com/setup_22.x | sudo bash -
sudo dnf install -y nodejs git python3 curl
```

### Arch Linux

```bash
sudo pacman -S nodejs npm git python curl
```

## Instalasi

### Langkah 1: Download Antigravity IDE

```bash
# Download .deb (Ubuntu/Debian)
wget -O ~/antigravity-ide.deb \
  "https://antigravity.google/download/ide-linux-deb"

# Install
sudo dpkg -i ~/antigravity-ide.deb
sudo apt install -f  # fix dependencies

# Atau download .tar.gz
wget -O ~/antigravity-ide.tar.gz \
  "https://antigravity.google/download/ide-linux"
mkdir -p ~/MitraAI-IDE
tar -xzf ~/antigravity-ide.tar.gz -C ~/MitraAI-IDE
```

### Langkah 2: Clone dan Build Patch

```bash
git clone https://github.com/qomaruddindjamal/MitraAI-IDE.git ~/mitraai-ide-patch
cd ~/mitraai-ide-patch

npm ci --ignore-scripts
npm run build
```

### Langkah 3: Verifikasi Kompatibilitas

```bash
# Jika install via .deb
npm run ide:check -- --resources "/usr/share/antigravity-ide/resources"

# Jika extract manual
npm run ide:check -- --resources ~/MitraAI-IDE/resources
```

### Langkah 4: Terapkan Patch

```bash
chmod +x deploy.sh

# .deb install
./deploy.sh --resources "/usr/share/antigravity-ide/resources"

# Manual extract
./deploy.sh --resources ~/MitraAI-IDE/resources
```

### Langkah 5: Konfigurasi Model

```bash
npm run proxy:start -- --open
```

### Langkah 6: MCP Setup (Opsional)

```bash
npm run ide:mcp -- apply
```

### Langkah 7: Launch

```bash
# Jika .deb install
npm run ide:launch -- --resources "/usr/share/antigravity-ide/resources"

# Manual
npm run ide:launch -- --resources ~/MitraAI-IDE/resources
```

## Launcher Script

```bash
cat > ~/start-mitraai-ide.sh << 'EOF'
#!/bin/bash
RESOURCES="/usr/share/antigravity-ide/resources"
PATCH_DIR="$HOME/mitraai-ide-patch"

echo "Starting proxy..."
cd "$PATCH_DIR"
npm run proxy:start > /dev/null 2>&1 &
sleep 3

echo "Launching MitraAI IDE..."
npm run ide:launch -- --resources "$RESOURCES"
EOF

chmod +x ~/start-mitraai-ide.sh
```

## Desktop Entry

```bash
cat > ~/.local/share/applications/mitraai-ide.desktop << 'EOF'
[Desktop Entry]
Name=MitraAI IDE
Comment=AI-powered IDE with local models
Exec=bash -c 'cd ~/mitraai-ide-patch && npm run proxy:start > /dev/null 2>&1 & sleep 3 && antigravity-ide'
Icon=antigravity-ide
Terminal=false
Type=Application
Categories=Development;IDE;
StartupNotify=true
EOF
```

## Instalasi Ollama

```bash
# Install
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull qwen2.5-coder:3b

# Verifikasi
ollama list
curl http://localhost:11434/v1/models
```

## Troubleshooting

### Permission Denied

```bash
sudo chmod +x /usr/share/antigravity-ide/antigravity-ide
sudo chmod +x ~/mitraai-ide-patch/deploy.sh
```

### Port 50999 Tidak Tersedia

```bash
sudo lsof -i :50999
sudo kill -9 <PID>
```

### IDE Tidak Terbuka

```bash
# Cek log
journalctl --user -u antigravity-ide

# Atau jalankan dari terminal untuk melihat error
antigravity-ide --verbose
```

### MCP Config Error

```bash
# Cek config
cat ~/.gemini/config/mcp_config.json | python3 -m json.tool

# Restore
cd ~/mitraai-ide-patch
npm run ide:mcp -- restore
```

## Uninstall

```bash
# Stop proxy
cd ~/mitraai-ide-patch
npm run proxy:stop

# Restore IDE
./deploy.sh --restore --resources "/usr/share/antigravity-ide/resources"

# Remove patch
rm -rf ~/mitraai-ide-patch

# Remove config
rm -rf ~/.gemini/antigravity

# Uninstall IDE
sudo apt remove antigravity-ide
rm ~/.local/share/applications/mitraai-ide.desktop
```
