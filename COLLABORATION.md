# MitraAI <-> Qoder Communication Bridge

## Cara Kerja

Bridge ini memungkinkan **MitraAI** dan **Qoder** berkomunikasi dan bekerja bersama seperti tim.

### Arsitektur

```
┌─────────────────┐                    ┌─────────────────┐
│     MitraAI     │                    │     Qoder       │
│  (Standalone/   │                    │   (AI Assistant)│
│     IDE)        │                    │                 │
└────────┬────────┘                    └────────┬────────┘
         │                                       │
         │  MCP Protocol                         │  MCP Protocol
         │  (Port 50999)                         │
         │                                       │
         └───────────┬───────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   MCP Bridge Server   │
         │   (mcp_bridge.py)     │
         │                       │
         │  Tools:               │
         │  - list_models()      │
         │  - ask_model()        │
         │  - chat_with_model()  │
         │  - delegate_task()    │
         │  - get_status()       │
         │  - introduce()        │
         └───────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  37 AI Providers      │
         │  - Ollama (local)     │
         │  - OpenAI             │
         │  - Anthropic          │
         │  - Google Gemini      │
         │  - Groq, DeepSeek...  │
         └───────────────────────┘
```

## Fitur Kolaborasi

### 1. Qoder Menggunakan Model MitraAI

Qoder bisa mengakses semua model yang dikonfigurasi di MitraAI melalui MCP tools:

```python
# Qoder memanggil MCP tool
list_available_models()  # Lihat model yang tersedia
ask_model("models/ollama-qwen", "Jelaskan quantum computing")
delegate_task("Analisis kode ini", preferred_provider="openai")
```

### 2. Delegasi Tugas Cerdas

Qoder bisa delegate tugas ke model terbaik berdasarkan:
- **Ukuran tugas**: Model kecil untuk tugas sederhana, besar untuk kompleks
- **Keahlian**: Model coding, writing, analysis, dll
- **Ketersediaan**: Jika satu provider down, switch ke yang lain
- **Cost**: Model lokal (gratis) vs cloud (berbayar)

### 3. Multi-Perspective Problem Solving

Untuk masalah kompleks, Qoder bisa:
1. Tanya model lokal (Ollama) untuk perspektif pertama
2. Tanya model cloud (GPT-4, Claude) untuk perspektif kedua
3. Bandingkan dan sintesis jawaban terbaik

### 4. Fallback & Redundancy

Jika satu model/provider tidak tersedia:
```python
# Qoder otomatis fallback
try:
    response = ask_model("models/openai-gpt4", prompt)
except:
    response = ask_model("models/anthropic-claude", prompt)  # Fallback
```

## Cara Menggunakan

### Untuk Qoder

MCP bridge sudah dikonfigurasi di:
```
C:\Users\Administrator\.gemini\antigravity\mcp_config.json
```

Qoder otomatis punya akses ke tools:
- `mcp__mitraai-bridge__list_available_models`
- `mcp__mitraai-bridge__ask_model`
- `mcp__mitraai-bridge__chat_with_model`
- `mcp__mitraai-bridge__delegate_task`
- `mcp__mitraai-bridge__get_mitraai_status`
- `mcp__mitraai-bridge__introduce_mitraai`

### Untuk MitraAI

MitraAI sudah berjalan di port 50999. MCP bridge otomatis connect ke proxy ini.

Untuk menambahkan model baru:
1. Buka browser: http://127.0.0.1:50999
2. Klik "Add Model"
3. Pilih provider (Ollama, OpenAI, dll)
4. Konfigurasi dan save

Model baru otomatis tersedia untuk Qoder!

## Contoh Skenario Kolaborasi

### Skenario 1: Code Review

**User**: "Review kode ini dan berikan saran"

**Qoder**:
1. Analisis kode sendiri
2. Delegate ke model coding (GPT-4) untuk perspektif kedua
3. Delegate ke model lokal (Ollama) untuk quick check
4. Sintesis semua feedback
5. Berikan rekomendasi komprehensif

### Skenario 2: Writing Assistance

**User**: "Bantu tulis dokumentasi untuk API ini"

**Qoder**:
1. Buat draft awal
2. Ask Claude untuk improve writing quality
3. Ask Gemini untuk verify technical accuracy
4. Finalize dengan best elements dari semua model

### Skenario 3: Problem Solving

**User**: "Bagaimana cara optimize query SQL ini?"

**Qoder**:
1. Analyze query structure
2. Ask local model for basic suggestions
3. Ask cloud model for advanced optimization
4. Compare approaches
5. Recommend best solution with explanation

### Skenario 4: Learning & Exploration

**User**: "Jelaskan konsep machine learning"

**Qoder**:
1. Explain basics dari knowledge sendiri
2. Ask different models for analogies
3. Provide multiple perspectives
4. Create comprehensive learning path

## Status & Monitoring

Cek status bridge:
```python
get_mitraai_status()
```

Output:
```json
{
  "proxy_status": "running",
  "proxy_url": "http://127.0.0.1:50999",
  "total_models": 5,
  "enabled_models": 5,
  "providers": {
    "ollama": 2,
    "openai": 1,
    "anthropic": 1,
    "gemini": 1
  }
}
```

## Troubleshooting

### Bridge Tidak Connect

1. Cek MitraAI proxy berjalan:
   ```bash
   curl http://127.0.0.1:50999/health
   ```

2. Restart proxy:
   ```bash
   cd C:\Users\Administrator\MitraAI-patch
   npm run proxy:start
   ```

3. Cek MCP config:
   ```bash
   cat C:\Users\Administrator\.gemini\antigravity\mcp_config.json
   ```

### Model Tidak Muncul

1. Buka http://127.0.0.1:50999
2. Pastikan model enabled
3. Restart MCP bridge jika perlu

### Connection Timeout

- Model lokal (Ollama): Normal 5-30 detik
- Model cloud: Normal 2-10 detik
- Jika timeout, cek koneksi internet atau model sedang busy

## Best Practices

### Kapan Gunakan Model Lokal vs Cloud

**Model Lokal (Ollama, LM Studio)**:
- Tugas sederhana (translate, summarize)
- Quick feedback
- Privacy-sensitive data
- Offline work

**Model Cloud (OpenAI, Anthropic, Gemini)**:
- Tugas kompleks (analysis, reasoning)
- Long-form writing
- Code generation
- Multi-step problems

### Cost Optimization

1. **Default ke model lokal** untuk tugas rutin
2. **Upgrade ke cloud** hanya untuk tugas kompleks
3. **Cache responses** untuk pertanyaan yang sering ditanya
4. **Use smaller models** untuk simple tasks

### Performance

1. **Parallel requests** ke multiple models untuk speed
2. **Stream responses** untuk long outputs
3. **Batch similar tasks** untuk efficiency
4. **Monitor token usage** untuk cost control

## Future Enhancements

- [ ] Auto-routing berdasarkan task type
- [ ] Response quality scoring
- [ ] Automatic model selection
- [ ] Shared memory/context antara models
- [ ] Collaborative problem solving protocols
- [ ] Real-time communication channel

## Support

Untuk pertanyaan atau issue:
- GitHub: https://github.com/qomaruddindjamal/MitraAI
- Docs: https://github.com/qomaruddindjamal/MitraAI/blob/main/docs/MCP-INTEGRATION.md

---

**MitraAI + Qoder = Tim AI yang Powerful!**
