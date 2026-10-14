# MitraAI IDE

**MitraAI IDE** adalah versi kustom dari Antigravity IDE (berbasis VS Code) yang mendukung model AI lokal dan provider pihak ketiga. IDE ini menggabungkan kekuatan Antigravity IDE dengan kemampuan menambahkan model custom.

<p align="center">
  <strong>IDE AI dengan model lokal Anda. Di dalam editor favorit Anda.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Lisensi-Apache--2.0-2563eb" alt="Apache License 2.0">
  <img src="https://img.shields.io/badge/VS_Code-1.107.0-007ACC?logo=visualstudiocode&logoColor=white" alt="VS Code 1.107.0">
  <img src="https://img.shields.io/badge/IDE_Version-2.5.5-007ACC" alt="IDE Version 2.5.5">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-0078D4" alt="Platform">
</p>

## Instalasi All-in-One (Recommended)

Satu perintah untuk install **semuanya** - bahkan di PC yang belum ada Antigravity IDE:

- Download & install Antigravity IDE
- Download & install Antigravity standalone
- Install patch + custom model support (37 provider)
- Fix port 50999 permanen (Hyper-V/WinNAT)
- Buat shortcut Desktop

### Windows (Run as Administrator)

```powershell
powershell -Command "Invoke-WebRequest -Uri https://raw.githubusercontent.com/qomaruddindjamal/MitraAI-IDE/main/install.bat -OutFile install.bat"; .\install.bat
```

Atau jika sudah clone:
```powershell
cd MitraAI-IDE
.\install.bat
```

### Linux / macOS

```bash
curl -fsSL https://raw.githubusercontent.com/qomaruddindjamal/MitraAI-IDE/main/install.sh | bash
```

Atau jika sudah clone:
```bash
cd MitraAI-IDE
chmod +x install.sh
./install.sh
```

Setelah instalasi, shortcut **"MitraAI IDE"** dan **"MitraAI"** muncul di Desktop. Langsung bisa dijalankan tanpa error!


## Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| **Model Lokal** | Ollama, LM Studio, vLLM langsung di IDE |
| **Native Picker** | Model custom muncul di model picker native IDE |
| **MCP Delegation** | Delegate tugas ke model custom via MCP tools |
| **Streamed Chat** | Streaming response dari model custom |
| **Effort Variants** | Low/medium/high effort untuk reasoning models |
| **Multi-Provider** | **37 provider**: OpenAI, Anthropic, Gemini, Groq, DeepSeek, xAI, NVIDIA, OpenRouter, Mistral, dll + 10 local server |
| **Browser Manager** | Kelola model dari browser dengan UI lengkap |
| **Multi-Provider** | OpenAI, Anthropic, Gemini, OpenRouter, dll |

## Perbedaan dengan MitraAI Standalone

| Aspek | MitraAI (Standalone) | MitraAI IDE |
|-------|---------------------|-------------|
| **Base** | Electron desktop app | VS Code 1.107.0 |
| **UI** | Chat interface | Full IDE + chat |
| **Model Picker** | Custom picker | Native IDE picker |
| **Agent Mode** | Terbatas untuk custom model | Full agent via MCP delegation |
| **MCP Support** | Via proxy | Native IDE MCP + custom delegation |
| **Use Case** | Quick chat & tasks | Development dengan AI assistance |

## Dokumentasi

| Platform | Panduan |
|----------|---------|
| Windows | [docs/INSTALL-WINDOWS.md](docs/INSTALL-WINDOWS.md) |
| Linux | [docs/INSTALL-LINUX.md](docs/INSTALL-LINUX.md) |
| macOS | [docs/INSTALL-MACOS.md](docs/INSTALL-MACOS.md) |
| Konfigurasi | [docs/CONFIGURATION.md](docs/CONFIGURATION.md) |
| MCP Integration | [docs/MCP-INTEGRATION.md](docs/MCP-INTEGRATION.md) |
| Build & Compile | [docs/BUILD.md](docs/BUILD.md) |

## Instalasi Cepat

### Auto-Setup (Recommended)

Script ini akan install dependencies, build, detect IDE, apply patch, dan **otomatis membuat shortcut di Desktop**.

**Windows:**
```powershell
git clone https://github.com/qomaruddindjamal/MitraAI-IDE.git
cd MitraAI-IDE
setup.bat
```

**Linux/macOS:**
```bash
git clone https://github.com/qomaruddindjamal/MitraAI-IDE.git
cd MitraAI-IDE
chmod +x setup.sh
./setup.sh
```

Setelah setup, shortcut **"MitraAI IDE"** akan muncul di Desktop.

### Manual Installation

### Windows

```powershell
# 1. Clone repositori
git clone https://github.com/qomaruddindjamal/MitraAI-IDE.git
cd MitraAI-IDE

# 2. Install dependencies
npm ci --ignore-scripts

# 3. Build
npm run build

# 4. Download Antigravity IDE dari https://antigravity.google/download

# 5. Cek kompatibilitas
npm run ide:check -- --resources "C:\Users\<User>\AppData\Local\Programs\Antigravity IDE\resources"

# 6. Terapkan patch
npm run ide:apply -- --resources "C:\Users\<User>\AppData\Local\Programs\Antigravity IDE\resources"

# 7. Start proxy
npm run proxy:start -- --open

# 8. Launch IDE
npm run ide:launch -- --resources "C:\Users\<User>\AppData\Local\Programs\Antigravity IDE\resources"
```

### Linux

```bash
# 1. Clone
git clone https://github.com/qomaruddindjamal/MitraAI-IDE.git
cd MitraAI-IDE

# 2. Install & build
npm ci --ignore-scripts
npm run build

# 3. Download Antigravity IDE Linux

# 4. Terapkan patch
chmod +x deploy.sh
./deploy.sh --resources "/opt/mitraai-ide/resources"

# 5. Start proxy & launch
npm run proxy:start -- --open
npm run ide:launch -- --resources "/opt/mitraai-ide/resources"
```

### macOS

```bash
# 1. Clone
git clone https://github.com/qomaruddindjamal/MitraAI-IDE.git
cd MitraAI-IDE

# 2. Install & build
npm ci --ignore-scripts
npm run build

# 3. Download Antigravity IDE macOS

# 4. Terapkan patch
./deploy.sh --resources "/Applications/MitraAI IDE.app/Contents/Resources"

# 5. Start proxy & launch
npm run proxy:start -- --open
npm run ide:launch -- --resources "/Applications/MitraAI IDE.app/Contents/Resources"
```

## Menambahkan Model Lokal

### Via Browser Manager

1. Start proxy: `npm run proxy:start -- --open`
2. Browser terbuka di `http://127.0.0.1:50999`
3. Pilih provider (Ollama, LM Studio, dll)
4. Masukkan endpoint dan API key
5. Klik **Fetch provider models**
6. Pilih model dari daftar
7. Klik **Save**

### Via Konfigurasi Manual

Edit `~/.gemini/antigravity/custom_models.json`:

```json
{
  "models": [
    {
      "name": "models/ollama-qwen-ide",
      "displayName": "Ollama qwen2.5-coder:3b (IDE)",
      "provider": "ollama",
      "apiFormat": "openai",
      "apiUrl": "http://localhost:11434/v1",
      "apiKey": "",
      "externalModelName": "qwen2.5-coder:3b",
      "enabled": true,
      "contextWindow": 32768,
      "maxOutputTokens": 4096,
      "timeout": 120000,
      "maxRetries": 2
    }
  ]
}
```

## Menggunakan Model Custom di IDE

### 1. Native Model Picker

Setelah patch diterapkan dan proxy berjalan:

1. Buka Antigravity IDE
2. Klik model picker di pojok kanan bawah
3. Model custom Anda akan muncul di daftar
4. Pilih model custom
5. Mulai chat atau gunakan agent mode

### 2. MCP Delegation (Advanced)

IDE 2.5.5 mendukung delegasi tugas ke model custom via MCP:

```
# Di chat IDE, gunakan parent model (Gemini)
"Gunakan custom-models tools untuk delegate summary teks ini ke models/ollama-qwen-ide"
```

Atau setup MCP server:

```bash
# Apply MCP config
npm run ide:mcp -- apply

# Check status
npm run ide:mcp -- status
```

Tools yang tersedia:
- `list_custom_models`: List semua model custom yang enabled
- `delegate_to_model`: Delegate tugas ke model custom tertentu

## Effort Variants

Untuk model yang mendukung reasoning, Anda bisa membuat effort variants:

```json
{
  "name": "models/reasoning-model",
  "displayName": "Reasoning Model",
  "provider": "openai",
  "apiFormat": "openai",
  "apiUrl": "https://api.openai.com/v1",
  "apiKey": "sk-...",
  "externalModelName": "o1-preview",
  "enabled": true,
  "contextWindow": 128000,
  "maxOutputTokens": 32768,
  "effortVariants": ["low", "medium", "high"]
}
```

Di IDE picker, Anda akan melihat:
- Reasoning Model (low)
- Reasoning Model (medium)
- Reasoning Model (high)

## Perintah Lengkap

### IDE Management

```bash
# Cek kompatibilitas IDE
npm run ide:check -- --resources "/path/to/IDE/resources"

# Terapkan patch
npm run ide:apply -- --resources "/path/to/IDE/resources"

# Restore original
npm run ide:restore -- --resources "/path/to/IDE/resources"

# Cek status
npm run ide:status -- --resources "/path/to/IDE/resources"

# Launch IDE
npm run ide:launch -- --resources "/path/to/IDE/resources"
```

### Proxy Management

```bash
# Start proxy
npm run proxy:start

# Start dengan browser manager
npm run proxy:start -- --open

# Custom port
npm run proxy:start -- --port 51001

# Custom data directory
npm run proxy:start -- --data-dir "/path/to/data"

# Status
npm run proxy:status

# Stop
npm run proxy:stop
```

### MCP Integration

```bash
# Apply MCP config
npm run ide:mcp -- apply

# Status
npm run ide:mcp -- status

# Restore
npm run ide:mcp -- restore

# Custom config path
npm run ide:mcp -- apply --config "/path/to/mcp_config.json"
```

## Build & Compile

```bash
# Install dependencies
npm ci --ignore-scripts

# Build TypeScript
npm run build

# Development mode
npm run dev

# Test
npm test

# Lint
npm run lint
```

Lihat [docs/BUILD.md](docs/BUILD.md) untuk detail lengkap.

## Troubleshooting

### Model Tidak Muncul di Native Picker

1. Pastikan proxy berjalan: `npm run proxy:status`
2. Cek `custom_models.json` valid
3. Restart IDE
4. Cek IDE status: `npm run ide:status -- --resources "..."`
5. Pastikan patch diterapkan: `npm run ide:check -- --resources "..."`

### Error "Invalid IDE Patch Manifest"

Patch IDE terikat ke path absolut. Jika Anda memindahkan IDE:

```bash
# Restore dulu dari path lama
npm run ide:restore -- --resources "/old/path/resources"

# Terapkan ulang di path baru
npm run ide:apply -- --resources "/new/path/resources"
```

### MCP Tools Tidak Muncul

1. Apply MCP config: `npm run ide:mcp -- apply`
2. Restart IDE
3. Buka **... → MCP Servers → Manage MCP Servers**
4. Refresh atau restart IDE
5. Approve tool usage saat diminta

### Streamed Response Tidak Muncul

1. Cek proxy log
2. Pastikan `apiUrl` benar
3. Test koneksi: `curl http://localhost:11434/v1/models`
4. Cek firewall tidak memblokir

### IDE Tidak Bisa Dibuka Setelah Patch

**Windows:**
```powershell
# Hapus quarantine jika ada
# Cek signature
Get-AuthenticodeSignature "Antigravity IDE.exe"
```

**macOS:**
```bash
# Hapus quarantine
xattr -cr "/Applications/MitraAI IDE.app"
```

**Linux:**
```bash
# Pastikan executable
chmod +x "Antigravity IDE"
```

## Validasi dan Testing

| Check | Status |
|-------|--------|
| IDE 2.5.5 Windows | Verified |
| Native picker dengan custom model | Verified |
| Streamed chat dari custom model | Verified |
| Effort variant routing | Verified |
| MCP delegation (parent → custom) | Verified |
| Live OpenRouter integration | Verified |

## Struktur Proyek

```
MitraAI-IDE/
├── scripts/
│   ├── ide.mjs              # IDE adapter
│   ├── ide-mcp.mjs          # MCP integration
│   ├── desktop-service.mjs  # Proxy service
│   └── model-delegation-mcp.mjs
├── src/                     # TypeScript source
├── dist/                    # Compiled JavaScript
├── docs/                    # Dokumentasi
├── gateway/                 # Web dashboard (opsional)
├── deploy.sh                # Linux/macOS
├── deploy.ps1               # Windows
└── package.json
```

## Kredit

- Berdasarkan [vahapogut/antigravity-add-model](https://github.com/vahapogut/antigravity-add-model) (Apache-2.0)
- Antigravity IDE - [antigravity.google](https://antigravity.google)
- VS Code 1.107.0

## Lisensi

Apache License 2.0 - Lihat [LICENSE](LICENSE)

## Kontribusi

Kontribusi diterima! Silakan buka issue atau pull request.
