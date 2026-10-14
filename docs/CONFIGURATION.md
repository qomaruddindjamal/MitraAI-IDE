# Konfigurasi Model - MitraAI

## 37 Provider yang Didukung

MitraAI mendukung **37 provider** — cloud API, lokal, dan custom endpoint.

### Cloud Providers (API Key Required)

| # | Provider | ID | API Format | Endpoint |
|---|----------|-----|-----------|----------|
| 1 | **OpenAI** | `openai` | openai | `https://api.openai.com/v1` |
| 2 | **Anthropic** | `anthropic` | anthropic | `https://api.anthropic.com` |
| 3 | **Google Gemini** | `google` | google | `https://generativelanguage.googleapis.com/v1beta` |
| 4 | **Google Cloud Code** | `google-cloudcode` | google | `https://daily-cloudcode-pa.googleapis.com` |
| 5 | **OpenRouter** | `openrouter` | openai | `https://openrouter.ai/api/v1` |
| 6 | **Cloudflare Workers AI** | `workers-ai` | openai | `https://api.cloudflare.com/client/v4/accounts/{ID}/ai/v1` |
| 7 | **Together AI** | `together` | openai | `https://api.together.ai/v1` |
| 8 | **Hugging Face** | `huggingface` | openai | `https://router.huggingface.co/v1` |
| 9 | **SambaNova** | `sambanova` | openai | `https://api.sambanova.ai/v1` |
| 10 | **SiliconFlow** | `siliconflow` | openai | `https://api.siliconflow.com/v1` |
| 11 | **Novita AI** | `novita` | openai | `https://api.novita.ai/openai/v1` |
| 12 | **Alibaba DashScope** | `dashscope` | openai | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` |
| 13 | **DeepSeek** | `deepseek` | openai | `https://api.deepseek.com/v1` |
| 14 | **Moonshot / Kimi** | `kimi` | openai | `https://api.moonshot.ai/v1` |
| 15 | **Fireworks AI** | `fireworks` | openai | `https://api.fireworks.ai/inference/v1` |
| 16 | **Groq** | `groq` | openai | `https://api.groq.com/openai/v1` |
| 17 | **Mistral** | `mistral` | openai | `https://api.mistral.ai/v1` |
| 18 | **Codestral** | `codestral` | openai | `https://codestral.mistral.ai/v1` |
| 19 | **Cerebras** | `cerebras` | openai | `https://api.cerebras.ai/v1` |
| 20 | **NVIDIA NIM** | `nvidia` | openai | `https://integrate.api.nvidia.com/v1` |
| 21 | **MiniMax** | `minimax` | anthropic | `https://api.minimax.io/anthropic/v1` |
| 22 | **OpenCode** | `opencode` | openai | `https://opencode.ai/zen/v1` |
| 23 | **OpenCode Zen** | `zen` | openai | `https://opencode.ai/zen/v1` |
| 24 | **OpenCode Go** | `opencode-go` | openai | `https://opencode.ai/zen/go/v1` |
| 25 | **Wafer** | `wafer` | anthropic | Custom endpoint |
| 26 | **Z.AI** | `zai` | anthropic | `https://api.z.ai/api/anthropic/v1` |
| 27 | **xAI (Grok)** | `xai` | openai | `https://api.x.ai/v1` |

### Local Providers (No API Key Required)

| # | Provider | ID | Port | Endpoint |
|---|----------|-----|------|----------|
| 28 | **Ollama** | `ollama` | 11434 | `http://localhost:11434/v1` |
| 29 | **LM Studio** | `lmstudio` | 1234 | `http://localhost:1234/v1` |
| 30 | **llama.cpp** | `llamacpp` | 8080 | `http://localhost:8080/v1` |
| 31 | **vLLM** | `vllm` | 8000 | `http://localhost:8000/v1` |
| 32 | **LocalAI** | `localai` | 8080 | `http://localhost:8080/v1` |
| 33 | **TabbyAPI** | `tabby` | 5000 | `http://localhost:5000/v1` |
| 34 | **Text Gen WebUI** | `textgen` | 5000 | `http://localhost:5000/v1` |
| 35 | **LiteLLM** | `litellm` | 4000 | `http://localhost:4000/v1` |
| 36 | **Aphrodite** | `aphrodite` | 2242 | `http://localhost:2242/v1` |
| 37 | **Custom Endpoint** | `custom` | - | URL apapun (OpenAI-compatible) |

## API Format

Tiga format protokol yang didukung:

| Format | Digunakan Oleh |
|--------|---------------|
| **openai** | OpenAI, Ollama, LM Studio, OpenRouter, Groq, DeepSeek, Mistral, NVIDIA, dll (30+ provider) |
| **anthropic** | Anthropic Claude, MiniMax, Wafer, Z.AI |
| **google** | Google Gemini, Google Cloud Code |

## File Konfigurasi

Lokasi: `~/.gemini/antigravity/custom_models.json`

**PENTING:** File harus UTF-8 **tanpa BOM**.

```json
{
  "models": [
    {
      "name": "models/unique-id",
      "displayName": "Display Name",
      "provider": "provider-id",
      "apiFormat": "openai",
      "apiUrl": "https://api.example.com/v1",
      "apiKey": "your-key",
      "externalModelName": "model-name",
      "enabled": true,
      "contextWindow": 32768,
      "maxOutputTokens": 4096,
      "timeout": 120000,
      "maxRetries": 2
    }
  ]
}
```

## Field Konfigurasi

| Field | Tipe | Required | Deskripsi |
|-------|------|----------|-----------|
| `name` | string | Ya | ID unik (format: `models/xxx`) |
| `displayName` | string | Ya | Nama di UI |
| `provider` | string | Ya | ID provider dari tabel di atas |
| `apiFormat` | string | Ya | `openai`, `anthropic`, atau `google` |
| `apiUrl` | string | Ya | Endpoint URL |
| `apiKey` | string | Tidak | API key (kosongkan untuk lokal) |
| `externalModelName` | string | Ya | Nama model di provider |
| `enabled` | boolean | Ya | Enable/disable |
| `contextWindow` | number | Ya | Context size (tokens) |
| `maxOutputTokens` | number | Ya | Max output tokens |
| `timeout` | number | Tidak | Timeout ms (default: 120000) |
| `maxRetries` | number | Tidak | Max retries (default: 2) |
| `supportsVision` | boolean | Tidak | Image input support |
| `supportsThinking` | boolean | Tidak | Reasoning/thinking support |
| `customHeaders` | object | Tidak | Custom HTTP headers |
| `fallbacks` | array | Tidak | Fallback model IDs |
| `effortVariants` | array | Tidak | Effort levels (IDE only) |

## Contoh Konfigurasi per Provider

### Ollama (Lokal - Gratis, Unlimited)

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

### OpenAI (GPT-4o, o1, o3)

```json
{
  "name": "models/gpt4o",
  "displayName": "OpenAI GPT-4o",
  "provider": "openai",
  "apiFormat": "openai",
  "apiUrl": "https://api.openai.com/v1",
  "apiKey": "sk-...",
  "externalModelName": "gpt-4o",
  "enabled": true,
  "contextWindow": 128000,
  "maxOutputTokens": 16384,
  "supportsVision": true
}
```

### Anthropic Claude

```json
{
  "name": "models/claude-sonnet",
  "displayName": "Claude 3.5 Sonnet",
  "provider": "anthropic",
  "apiFormat": "anthropic",
  "apiUrl": "https://api.anthropic.com",
  "apiKey": "sk-ant-...",
  "externalModelName": "claude-3-5-sonnet-20241022",
  "enabled": true,
  "contextWindow": 200000,
  "maxOutputTokens": 8192
}
```

### OpenRouter (100+ Model, Beberapa Gratis)

```json
{
  "name": "models/openrouter-llama",
  "displayName": "OpenRouter Llama 3.3 70B",
  "provider": "openrouter",
  "apiFormat": "openai",
  "apiUrl": "https://openrouter.ai/api/v1",
  "apiKey": "sk-or-...",
  "externalModelName": "meta-llama/llama-3.3-70b-instruct",
  "enabled": true,
  "contextWindow": 128000,
  "maxOutputTokens": 4096
}
```

### DeepSeek (Murah, Kualitas Tinggi)

```json
{
  "name": "models/deepseek",
  "displayName": "DeepSeek V3",
  "provider": "deepseek",
  "apiFormat": "openai",
  "apiUrl": "https://api.deepseek.com/v1",
  "apiKey": "sk-...",
  "externalModelName": "deepseek-chat",
  "enabled": true,
  "contextWindow": 64000,
  "maxOutputTokens": 8192
}
```

### Groq (Super Fast - Free Tier Available)

```json
{
  "name": "models/groq",
  "displayName": "Groq Llama 3.3 70B",
  "provider": "groq",
  "apiFormat": "openai",
  "apiUrl": "https://api.groq.com/openai/v1",
  "apiKey": "gsk_...",
  "externalModelName": "llama-3.3-70b-versatile",
  "enabled": true,
  "contextWindow": 128000,
  "maxOutputTokens": 8192
}
```

### Google Gemini

```json
{
  "name": "models/gemini-flash",
  "displayName": "Gemini 2.5 Flash",
  "provider": "google",
  "apiFormat": "google",
  "apiUrl": "https://generativelanguage.googleapis.com/v1beta",
  "apiKey": "AIza...",
  "externalModelName": "gemini-2.5-flash",
  "enabled": true,
  "contextWindow": 1000000,
  "maxOutputTokens": 8192
}
```

### xAI Grok

```json
{
  "name": "models/grok",
  "displayName": "xAI Grok 2",
  "provider": "xai",
  "apiFormat": "openai",
  "apiUrl": "https://api.x.ai/v1",
  "apiKey": "xai-...",
  "externalModelName": "grok-2-latest",
  "enabled": true,
  "contextWindow": 131072,
  "maxOutputTokens": 4096
}
```

### NVIDIA NIM

```json
{
  "name": "models/nvidia",
  "displayName": "NVIDIA Llama 405B",
  "provider": "nvidia",
  "apiFormat": "openai",
  "apiUrl": "https://integrate.api.nvidia.com/v1",
  "apiKey": "nvapi-...",
  "externalModelName": "meta/llama-3.1-405b-instruct",
  "enabled": true,
  "contextWindow": 128000,
  "maxOutputTokens": 4096
}
```

### Cloudflare Workers AI (Free Tier)

```json
{
  "name": "models/cf",
  "displayName": "Workers AI Llama",
  "provider": "workers-ai",
  "apiFormat": "openai",
  "apiUrl": "https://api.cloudflare.com/client/v4/accounts/YOUR_ACCOUNT_ID/ai/v1",
  "apiKey": "your-cf-token",
  "externalModelName": "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
  "enabled": true,
  "contextWindow": 128000,
  "maxOutputTokens": 4096
}
```

### Mistral / Codestral

```json
{
  "name": "models/codestral",
  "displayName": "Codestral",
  "provider": "codestral",
  "apiFormat": "openai",
  "apiUrl": "https://codestral.mistral.ai/v1",
  "apiKey": "your-mistral-key",
  "externalModelName": "codestral-latest",
  "enabled": true,
  "contextWindow": 256000,
  "maxOutputTokens": 4096
}
```

### LM Studio (Lokal - Gratis)

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

### Custom Endpoint (OpenAI-compatible apapun)

```json
{
  "name": "models/my-server",
  "displayName": "My Custom Server",
  "provider": "custom",
  "apiFormat": "openai",
  "apiUrl": "http://my-server.local:8080/v1",
  "apiKey": "",
  "externalModelName": "my-model",
  "enabled": true,
  "contextWindow": 8192,
  "maxOutputTokens": 2048
}
```

## Advanced Settings

### Vision/Image Support
```json
{ "supportsVision": true }
```

### Reasoning/Thinking
```json
{ "supportsThinking": true }
```

### Effort Variants (IDE only)
```json
{ "effortVariants": ["low", "medium", "high"] }
```

### Custom Headers
```json
{ "customHeaders": { "X-Custom": "value" } }
```

### Fallback Chain
```json
{ "fallbacks": ["models/backup1", "models/backup2"] }
```

## Context Window Guidelines

| Model Size | Context | Max Output |
|------------|---------|------------|
| 0.5B-1B | 4096-8192 | 1024-2048 |
| 3B-7B | 8192-32768 | 2048-4096 |
| 13B-30B | 16384-65536 | 4096-8192 |
| 70B+ | 32768-131072 | 8192-16384 |

## Auto-Discovery Lokal

Proxy otomatis scan 9 port untuk local providers:

| Port | Provider |
|------|----------|
| 11434 | Ollama |
| 1234 | LM Studio |
| 8080 | llama.cpp / LocalAI |
| 8000 | vLLM |
| 5000 | TabbyAPI / TextGen |
| 4000 | LiteLLM |
| 2242 | Aphrodite |

Klik **"Discover local"** di browser manager untuk scan otomatis.

## Import/Export

Browser manager (`http://127.0.0.1:50999`): **Export/Import** - JSON atau Base64.

API keys tidak di-export untuk keamanan.

## Troubleshooting

### JSON Invalid
```bash
python -m json.tool ~/.gemini/antigravity/custom_models.json
```

### BOM Issue
File harus UTF-8 tanpa BOM:
```bash
sed -i '1s/^\xEF\xBB\xBF//' custom_models.json
```

### Model Tidak Muncul
1. Pastikan `enabled: true`
2. Restart proxy
3. Cek provider ID dan apiUrl benar
4. Cek API key valid (untuk cloud providers)

### Koneksi Gagal
1. Cek server berjalan
2. Cek firewall tidak memblokir port
3. Test manual: `curl http://localhost:11434/v1/models`
