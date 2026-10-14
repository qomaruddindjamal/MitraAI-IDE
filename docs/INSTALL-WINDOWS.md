# Instalasi MitraAI IDE di Windows

## Prasyarat

| Software | Versi Minimum | Cara Install |
|----------|---------------|--------------|
| **Node.js** | 22.13+ | [nodejs.org](https://nodejs.org/) atau `winget install OpenJS.NodeJS.LTS` |
| **Git** | 2.30+ | `winget install Git.Git` |
| **Antigravity IDE** | 2.5.5 | [antigravity.google/download](https://antigravity.google/download) |
| **Python** | 3.8+ | Untuk MCP server (opsional) |
| **Ollama** (opsional) | 0.5+ | [ollama.com/download](https://ollama.com/download) |

### Verifikasi

```powershell
node --version    # v22.13.0+
npm --version     # 10.x+
git --version     # 2.30+
python --version  # 3.8+ (opsional)
```

## Instalasi

### Langkah 1: Install Antigravity IDE

1. Download dari [antigravity.google/download](https://antigravity.google/download)
2. Install ke lokasi default: `C:\Users\<User>\AppData\Local\Programs\Antigravity IDE`
3. Selesaikan setup awal dan login Google (jika mau)
4. Tutup IDE sebelum melanjutkan

### Langkah 2: Clone dan Build Patch

```powershell
git clone https://github.com/qomaruddindjamal/MitraAI-IDE.git
cd MitraAI-IDE

npm ci --ignore-scripts
npm run build
```

### Langkah 3: Verifikasi Kompatibilitas

```powershell
npm run ide:check -- --resources "C:\Users\$env:USERNAME\AppData\Local\Programs\Antigravity IDE\resources"
```

Output yang diharapkan:
```
IDE version: 2.5.5
VS Code version: 1.107.0
Preflight: PASS
```

### Langkah 4: Terapkan Patch IDE

```powershell
npm run ide:apply -- --resources "C:\Users\$env:USERNAME\AppData\Local\Programs\Antigravity IDE\resources"
```

### Langkah 5: Konfigurasi Model

Buka browser model manager:

```powershell
npm run proxy:start -- --open
```

Tambahkan model (Ollama, OpenAI, dll) dari browser manager.

### Langkah 6: Setup MCP (Opsional)

Untuk menggunakan custom model delegation via MCP:

```powershell
npm run ide:mcp -- apply
```

### Langkah 7: Launch IDE

```powershell
npm run ide:launch -- --resources "C:\Users\$env:USERNAME\AppData\Local\Programs\Antigravity IDE\resources"
```

Atau buat launcher batch:

```powershell
# Buat START-MitraAI-IDE.bat
@echo off
echo Starting proxy...
cd /d "C:\path\to\MitraAI-IDE"
call npm run proxy:start >nul 2>&1
echo Launching MitraAI IDE...
start "" "C:\Users\%USERNAME%\AppData\Local\Programs\Antigravity IDE\Antigravity IDE.exe"
```

## Instalasi Ollama

```powershell
# Install Ollama
winget install Ollama.Ollama

# Pull model
ollama pull qwen2.5-coder:3b

# Verifikasi
ollama list
curl http://localhost:11434/v1/models
```

## Konfigurasi Model

### Via Browser Manager

1. `npm run proxy:start -- --open`
2. Pilih provider **Ollama**
3. Endpoint: `http://localhost:11434/v1`
4. Klik **Fetch provider models**
5. Pilih model
6. Save

### Via File Manual

Buat `C:\Users\<User>\.gemini\antigravity\custom_models.json`:

```json
{
  "models": [
    {
      "name": "models/ollama-ide",
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

## Menggunakan Model Custom

### Di Native Picker

1. Buka MitraAI IDE
2. Klik model picker (pojok kanan bawah)
3. Model custom muncul di daftar
4. Pilih dan mulai chat

### Via MCP Delegation

Di chat dengan parent model (misal Gemini):

```
Gunakan custom-models tools untuk delegate tugas ini ke models/ollama-ide:
[deskripsi tugas]
```

## Troubleshooting

### Port 50999 Diblokir Hyper-V

```powershell
net stop winnat
net start winnat
```

### Patch Manifest Invalid

Patch IDE terikat path. Jika IDE dipindahkan:

```powershell
# Restore dari path lama
npm run ide:restore -- --resources "C:\old\path\resources"

# Apply di path baru
npm run ide:apply -- --resources "C:\new\path\resources"
```

### MCP Tools Tidak Muncul

1. `npm run ide:mcp -- apply`
2. Restart IDE
3. Buka **... → MCP Servers → Manage MCP Servers**
4. Refresh
5. Approve tool usage

### JSON Parse Error (BOM)

```powershell
$content = Get-Content "$env:USERPROFILE\.gemini\antigravity\custom_models.json" -Raw
[System.IO.File]::WriteAllText(
  "$env:USERPROFILE\.gemini\antigravity\custom_models.json",
  $content,
  (New-Object System.Text.UTF8Encoding $false)
)
```

## Status dan Recovery

```powershell
# Cek status IDE
npm run ide:status -- --resources "C:\path\to\IDE\resources"

# Cek status proxy
npm run proxy:status

# Restore original IDE
npm run ide:restore -- --resources "C:\path\to\IDE\resources"

# Stop proxy
npm run proxy:stop
```

## Uninstall

```powershell
# 1. Stop proxy
cd MitraAI-IDE
npm run proxy:stop

# 2. Restore IDE
npm run ide:restore -- --resources "C:\path\to\IDE\resources"

# 3. Restore MCP config
npm run ide:mcp -- restore

# 4. Hapus konfigurasi (opsional)
Remove-Item -Recurse "$env:USERPROFILE\.gemini\antigravity"

# 5. Uninstall Antigravity IDE dari Control Panel
```

## Update

```powershell
cd MitraAI-IDE
git pull
npm ci --ignore-scripts
npm run build

# Terapkan ulang patch
npm run ide:apply -- --resources "C:\path\to\IDE\resources"
```
