# Build & Compile Guide - MitraAI IDE

## Prasyarat

| Tool | Versi | Catatan |
|------|-------|---------|
| **Node.js** | 22.13+ | Required |
| **npm** | 10.x+ | Termasuk Node.js |
| **Git** | 2.30+ | Required |
| **TypeScript** | 6.x+ | Auto-installed |
| **Python** | 3.8+ | Untuk MCP server (opsional) |

## Quick Build

```bash
# 1. Clone
git clone https://github.com/qomaruddindjamal/MitraAI-IDE.git
cd MitraAI-IDE

# 2. Install
npm ci --ignore-scripts

# 3. Build
npm run build

# 4. Test
npm test
```

## Perintah Build

### Build Utama

```bash
# Compile TypeScript → JavaScript
npm run build

# Output: dist/

# Watch mode
npm run dev

# Clean
npm run clean
```

### Testing

```bash
# Semua test
npm test

# Watch mode
npm run test:watch

# Integration test
npm run test:integration
```

### Code Quality

```bash
npm run lint
npm run lint:fix
npm run format
npm run format:check
```

## IDE Commands

```bash
# Cek kompatibilitas
npm run ide:check -- --resources "/path/to/IDE/resources"

# Apply patch
npm run ide:apply -- --resources "/path/to/IDE/resources"

# Restore
npm run ide:restore -- --resources "/path/to/IDE/resources"

# Status
npm run ide:status -- --resources "/path/to/IDE/resources"

# Launch
npm run ide:launch -- --resources "/path/to/IDE/resources"
```

### IDE Options

| Option | Deskripsi |
|--------|-----------|
| `--resources "/path"` | Path ke resources IDE |
| `--settings "/path/settings.json"` | Explicit settings file |
| `--data-dir "/path"` | Data directory untuk proxy & models |
| `--port 51001` | Custom proxy port (default: 50999) |
| `--executable "/path/exe"` | Custom executable path |

## Proxy Commands

```bash
# Start
npm run proxy:start

# Start dengan browser manager
npm run proxy:start -- --open

# Custom port
npm run proxy:start -- --port 51001

# Custom data dir
npm run proxy:start -- --data-dir "/path/to/data"

# Status
npm run proxy:status

# Stop
npm run proxy:stop
```

## MCP Commands

```bash
# Apply MCP config
npm run ide:mcp -- apply

# Status
npm run ide:mcp -- status

# Restore
npm run ide:mcp -- restore

# Custom config path
npm run ide:mcp -- apply --config "/path/to/config.json"

# Custom data dir
npm run ide:mcp -- apply --data-dir "/path/to/data"
```

## Gateway (Opsional)

```bash
# Install
npm run gateway:install

# Build
npm run gateway:build

# Test
npm run gateway:test

# Run
npm run gateway
```

## Development Workflow

```bash
# 1. Setup
git clone https://github.com/qomaruddindjamal/MitraAI-IDE.git
cd MitraAI-IDE
npm ci --ignore-scripts

# 2. Development
npm run dev           # Watch TypeScript (terminal 1)
npm run proxy:start   # Start proxy (terminal 2)

# 3. Edit source di src/

# 4. Test
npm test

# 5. Build
npm run build

# 6. Deploy
npm run ide:apply -- --resources "/path/to/IDE/resources"
```

## Build Output

```
MitraAI-IDE/
├── src/              # TypeScript source
│   ├── main.ts
│   ├── ide/
│   ├── proxy/
│   └── mcp/
├── dist/             # Compiled output
│   ├── main.js
│   ├── ide/
│   ├── proxy/
│   └── mcp/
├── scripts/          # Runtime scripts
└── package.json
```

## Platform-Specific Notes

### Windows

```powershell
# PowerShell
npm ci --ignore-scripts
npm run build

# Deploy
npm run ide:apply -- --resources "C:\path\to\IDE\resources"
```

### Linux

```bash
npm ci --ignore-scripts
npm run build
chmod +x deploy.sh
./deploy.sh --resources "/path/to/IDE/resources"
```

### macOS

```bash
npm ci --ignore-scripts
npm run build
chmod +x deploy.sh
./deploy.sh --resources "/Applications/MitraAI IDE.app/Contents/Resources"
xattr -cr "/Applications/MitraAI IDE.app"
```

## Troubleshooting Build

### TypeScript Errors

```bash
npm run clean
rm -rf node_modules
npm ci --ignore-scripts
npm run build
```

### Permission Errors

```bash
chmod +x deploy.sh scripts/*.mjs
```

### Node Version

```bash
node --version  # Harus 22.13+
nvm install 22
nvm use 22
```

## Diagnostic Tools

```bash
# Doctor
npm run doctor

# Integration smoke test
npm run test:integration

# IDE check
npm run ide:check -- --resources "/path/to/IDE/resources"
```

## Distribution

```bash
# Bundle
tar -czf mitraai-ide-patch.tar.gz \
  dist/ scripts/ package.json package-lock.json \
  deploy.sh deploy.ps1 README.md LICENSE
```
