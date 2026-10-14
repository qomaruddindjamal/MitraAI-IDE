# Konfigurasi MitraAI IDE

## File Konfigurasi

### custom_models.json

Lokasi: `~/.gemini/antigravity/custom_models.json`

```json
{
  "models": [
    {
      "name": "models/unique-id",
      "displayName": "Display Name",
      "provider": "ollama",
      "apiFormat": "openai",
      "apiUrl": "http://localhost:11434/v1",
      "apiKey": "",
      "externalModelName": "model:tag",
      "enabled": true,
      "contextWindow": 32768,
      "maxOutputTokens": 4096,
      "timeout": 120000,
      "maxRetries": 2
    }
  ]
}
```

**PENTING:** UTF-8 tanpa BOM.

## Field Konfigurasi

| Field | Tipe | Required | Deskripsi |
|-------|------|----------|-----------|
| `name` | string | Ya | ID unik (`models/xxx`) |
| `displayName` | string | Ya | Nama di UI |
| `provider` | string | Ya | Provider ID |
| `apiFormat` | string | Ya | `openai` atau `anthropic` |
| `apiUrl` | string | Ya | Endpoint URL |
| `apiKey` | string | Tidak | API key |
| `externalModelName` | string | Ya | Nama model di provider |
| `enabled` | boolean | Ya | Enable/disable |
| `contextWindow` | number | Ya | Context size (tokens) |
| `maxOutputTokens` | number | Ya | Max output tokens |
| `timeout` | number | Tidak | Timeout (ms) |
| `maxRetries` | number | Tidak | Max retries |
| `supportsVision` | boolean | Tidak | Image input support |
| `reasoning` | object | Tidak | Reasoning settings |
| `effortVariants` | array | Tidak | Effort levels |
| `customHeaders` | object | Tidak | Custom HTTP headers |
| `fallbacks` | array | Tidak | Fallback models |

## Contoh per Provider

### Ollama

```json
{
  "name": "models/ollama-qwen",
  "displayName": "Ollama Qwen 2.5 Coder 3B",
  "provider": "ollama",
  "apiFormat": "openai",
  "apiUrl": "http://localhost:11434/v1",
  "apiKey": "",
  "externalModelName": "qwen2.5-coder:3b",
  "enabled": true,
  "contextWindow": 32768,
  "maxOutputTokens": 4096
}
```

### LM Studio

```json
{
  "name": "models/lmstudio",
  "displayName": "LM Studio Local",
  "provider": "lmstudio",
  "apiFormat": "openai",
  "apiUrl": "http://localhost:1234/v1",
  "apiKey": "",
  "externalModelName": "local-model",
  "enabled": true,
  "contextWindow": 8192,
  "maxOutputTokens": 2048
}
```

### OpenAI

```json
{
  "name": "models/gpt4",
  "displayName": "OpenAI GPT-4",
  "provider": "openai",
  "apiFormat": "openai",
  "apiUrl": "https://api.openai.com/v1",
  "apiKey": "sk-...",
  "externalModelName": "gpt-4-turbo-preview",
  "enabled": true,
  "contextWindow": 128000,
  "maxOutputTokens": 4096
}
```

### Anthropic

```json
{
  "name": "models/claude3",
  "displayName": "Anthropic Claude 3",
  "provider": "anthropic",
  "apiFormat": "anthropic",
  "apiUrl": "https://api.anthropic.com",
  "apiKey": "sk-ant-...",
  "externalModelName": "claude-3-opus-20240229",
  "enabled": true,
  "contextWindow": 200000,
  "maxOutputTokens": 4096
}
```

### OpenRouter

```json
{
  "name": "models/openrouter",
  "displayName": "OpenRouter Mixtral",
  "provider": "openrouter",
  "apiFormat": "openai",
  "apiUrl": "https://openrouter.ai/api/v1",
  "apiKey": "sk-or-...",
  "externalModelName": "mistralai/mixtral-8x7b-instruct",
  "enabled": true,
  "contextWindow": 32768,
  "maxOutputTokens": 4096
}
```

### Google Gemini

```json
{
  "name": "models/gemini",
  "displayName": "Google Gemini Pro",
  "provider": "gemini",
  "apiFormat": "openai",
  "apiUrl": "https://generativelanguage.googleapis.com/v1beta/openai",
  "apiKey": "AIza...",
  "externalModelName": "gemini-pro",
  "enabled": true,
  "contextWindow": 32768,
  "maxOutputTokens": 8192
}
```

## Advanced Configuration

### Effort Variants

```json
{
  "name": "models/reasoning",
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

Di IDE picker akan muncul:
- Reasoning Model (low)
- Reasoning Model (medium)
- Reasoning Model (high)

### Vision Support

```json
{
  "name": "models/vision",
  "displayName": "Vision Model",
  "provider": "openai",
  "apiFormat": "openai",
  "apiUrl": "https://api.openai.com/v1",
  "apiKey": "sk-...",
  "externalModelName": "gpt-4-vision-preview",
  "enabled": true,
  "contextWindow": 128000,
  "maxOutputTokens": 4096,
  "supportsVision": true
}
```

### Custom Headers

```json
{
  "name": "models/custom",
  "displayName": "Custom API",
  "provider": "custom",
  "apiFormat": "openai",
  "apiUrl": "https://api.example.com/v1",
  "apiKey": "key",
  "externalModelName": "model",
  "enabled": true,
  "contextWindow": 8192,
  "maxOutputTokens": 2048,
  "customHeaders": {
    "X-Custom": "value"
  }
}
```

### Fallback Chain

```json
{
  "name": "models/primary",
  "displayName": "Primary Model",
  "provider": "openai",
  "apiFormat": "openai",
  "apiUrl": "https://api.openai.com/v1",
  "apiKey": "sk-...",
  "externalModelName": "gpt-4",
  "enabled": true,
  "contextWindow": 128000,
  "maxOutputTokens": 4096,
  "fallbacks": ["models/backup1", "models/backup2"]
}
```

## Context Window Guidelines

| Model Size | Context | Max Output |
|------------|---------|------------|
| 0.5B-1B | 4096-8192 | 1024-2048 |
| 3B-7B | 8192-32768 | 2048-4096 |
| 13B-30B | 16384-65536 | 4096-8192 |
| 70B+ | 32768-131072 | 8192-16384 |

## Native Picker Capacity

IDE 2.5.5 memiliki **651 slot** untuk native model identities. Custom model mengambil slot dari pool ini. Jika slot habis, model tetap bisa diakses via direct API alias tapi tidak muncul di native picker.

Assignments disimpan di `<data-dir>/custom_model_identities.json`. Backup file ini bersama `custom_models.json`.

## MCP Configuration

File: `~/.gemini/config/mcp_config.json`

```json
{
  "mcpServers": {
    "custom-models": {
      "command": "node",
      "args": [
        "/path/to/MitraAI-IDE/scripts/model-delegation-mcp.mjs",
        "--data-dir",
        "/path/to/data"
      ]
    }
  }
}
```

## Import/Export

### Export

Dari browser manager:
1. Klik **Export**
2. Pilih JSON atau Base64
3. Simpan

### Import

1. Klik **Import**
2. Pilih file atau paste
3. Review dan confirm

**Catatan:** API keys tidak di-export untuk keamanan.

## Troubleshooting

### Invalid JSON

```bash
# Validate
python3 -m json.tool ~/.gemini/antigravity/custom_models.json

# Atau
node -e "JSON.parse(require('fs').readFileSync('custom_models.json','utf8'))"
```

### BOM Issue

```bash
# Cek
hexdump -C custom_models.json | head -1

# Hapus BOM
sed -i '1s/^\xEF\xBB\xBF//' custom_models.json
```

### Model Tidak Muncul

1. `enabled: true`?
2. Restart proxy
3. Restart IDE
4. Cek log

### Koneksi Gagal

1. Cek `apiUrl`
2. Cek server berjalan
3. Cek firewall
4. Cek API key
