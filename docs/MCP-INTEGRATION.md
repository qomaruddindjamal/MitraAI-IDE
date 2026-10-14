# MCP Integration - MitraAI IDE

## Apa itu MCP?

**Model Context Protocol (MCP)** memungkinkan model parent (misal Gemini) di IDE mendelegasikan tugas ke model custom Anda (misal Ollama lokal) sebagai worker independen.

## Cara Kerja

```
┌─────────────────────────────────────────┐
│  Antigravity IDE (Parent: Gemini)       │
│                                         │
│  1. User mengirim prompt ke parent      │
│  2. Parent memanggil MCP tool           │
│  3. MCP → Proxy → Custom Model (Ollama) │
│  4. Hasil kembali ke parent             │
│  5. Parent menggabungkan ke response    │
└─────────────────────────────────────────┘
```

## Setup

### 1. Apply MCP Config

```bash
npm run ide:mcp -- apply
```

Ini menambahkan server `custom-models` ke `~/.gemini/config/mcp_config.json`.

### 2. Restart IDE

```bash
npm run ide:launch -- --resources "/path/to/IDE/resources"
```

### 3. Approve Tools

Di IDE, buka **... → MCP Servers → Manage MCP Servers**. Anda akan melihat server `custom-models` dengan 2 tools:

- `list_custom_models`
- `delegate_to_model`

Klik **Approve** untuk setiap tool (one-time).

## MCP Tools

### list_custom_models

List semua model custom yang enabled.

**Parameters:**
- `cursor` (opsional): Pagination cursor

**Returns:**
```json
{
  "models": [
    {"name": "models/ollama-qwen", "displayName": "Ollama qwen2.5-coder:3b"},
    {"name": "models/gpt4", "displayName": "OpenAI GPT-4"}
  ],
  "nextCursor": null
}
```

### delegate_to_model

Delegate tugas ke model custom.

**Parameters:**
- `model` (required): Nama model persis seperti di config
- `prompt` (required): Tugas yang didelegasikan
- `context` (opsional): Konteks tambahan (teks)

**Constraints:**
- Text-only (tidak ada gambar/file)
- Max task+context: 64 KiB
- Max output: 8,192 tokens
- Timeout: 120 detik
- 4 concurrent workers

**Returns:**
```json
{
  "result": "Jawaban dari model custom...",
  "model": "models/ollama-qwen",
  "truncated": false,
  "tokensUsed": 256
}
```

## Contoh Penggunaan

### Di Chat IDE

Dengan parent model (Gemini), ketik:

```
Gunakan custom-models tools untuk mendelegasikan tugas berikut ke
models/ollama-qwen:

"Buatkan fungsi Python untuk mengurutkan list menggunakan merge sort"
```

Parent akan:
1. Memanggil `delegate_to_model`
2. Menerima hasil dari Ollama
3. Menampilkan hasil di chat

### Dengan Context

```
Gunakan delegate_to_model ke models/ollama-qwen dengan:

Prompt: "Review kode ini dan berikan saran perbaikan"
Context: "def foo(x): return x + 1"
```

### List Models Dulu

```
Gunakan list_custom_models untuk melihat model apa saja yang tersedia,
lalu delegate tugas summarization ke model pertama yang kamu temukan
```

## MCP Config Manual

Jika ingin setup manual:

File: `~/.gemini/config/mcp_config.json`

```json
{
  "mcpServers": {
    "custom-models": {
      "command": "node",
      "args": [
        "/path/to/MitraAI-IDE/scripts/model-delegation-mcp.mjs",
        "--data-dir",
        "/path/to/model-data"
      ]
    }
  }
}
```

**PENTING:**
- Gunakan `node` langsung, bukan `npm run` (npm banner merusak MCP output)
- `--data-dir` harus sama dengan yang digunakan proxy
- Script path harus absolut

## Custom Data Directory

```bash
# Start proxy dengan data dir
npm run proxy:start -- --data-dir "/path/to/model-data"

# Apply MCP dengan data dir yang sama
npm run ide:mcp -- apply --data-dir "/path/to/model-data"
```

## Status dan Management

```bash
# Cek status MCP config
npm run ide:mcp -- status

# Restore original config
npm run ide:mcp -- restore

# Custom config path
npm run ide:mcp -- apply --config "/path/to/mcp_config.json"
```

## Backup dan Recovery

Backup disimpan di `~/.gemini/config/mcp_config.json.antigravity-custom-models/`

Restore akan:
- Cek backup integrity
- Restore original jika tidak ada perubahan manual
- Preserve unrelated edits
- Report conflict jika ada perubahan manual pada managed entry

## Troubleshooting

### Tools Tidak Muncul

1. Cek status: `npm run ide:mcp -- status`
2. Restart IDE
3. Buka MCP Manager dan refresh
4. Approve tools

### Delegation Gagal

1. Cek proxy berjalan: `npm run proxy:status`
2. Cek model enabled di config
3. Cek nama model persis sama
4. Cek log proxy untuk error

### Timeout

Default timeout 120 detik. Untuk model lambat:
- Gunakan model lebih kecil
- Kurangi context size
- Cek Ollama performance

### MCP Process Crash

```bash
# Cek process
ps aux | grep model-delegation-mcp

# Restart IDE akan restart MCP process
```

## Keamanan

- MCP process berkomunikasi via stdio (lokal)
- Autentikasi ke proxy via loopback token
- Tidak ada data yang dikirim ke server eksternal
- API keys tetap terenkripsi di data directory
- Model delegation adalah text-only, tidak ada akses file/command

## Limitasi

1. **Text-only**: Tidak bisa kirim gambar atau file
2. **No tools**: Worker tidak bisa call tools atau baca file
3. **No chat history**: Setiap delegation independen
4. **No fallback**: Jika model gagal, tidak ada fallback otomatis
5. **Size limit**: 64 KiB task+context, 8K output tokens
6. **Concurrency**: Max 4 workers bersamaan

## Tips

1. **Gunakan context yang relevan** - Worker tidak punya akses ke chat history
2. **Task yang spesifik** - Worker terbaik untuk tugas yang jelas dan terdefinisi
3. **Verify hasil** - Parent bisa verify dan refine hasil dari worker
4. **Pilih model yang tepat** - Gunakan model yang cocok untuk tugas
5. **Monitor usage** - Setiap delegation consume provider quota
