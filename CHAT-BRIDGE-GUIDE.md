# Panduan Chat Bridge: Mengobrol antara Standalone dan IDE

## Cara Menjalankan

Buka terminal/command prompt dan jalankan:

```bash
cd C:\Users\Administrator\Documents\Qoder\2026-10-14\a5189cf2\MitraAI-docs
python chat_bridge.py
```

## Konsep Dasar

Chat Bridge adalah interface interaktif yang memungkinkan Anda berperan sebagai **Standalone** atau **IDE** dan mengirim pesan ke app lainnya, seperti orang mengobrol!

```
┌─────────────────────────────────────────────────┐
│         CHAT BRIDGE (Anda di sini)              │
│                                                 │
│  /standalone  ←→  /ide                          │
│  (R&D Mode)        (Implementation Mode)        │
│                                                 │
│         ↓ kirim pesan ↓                         │
│                                                 │
│  ┌──────────────┐         ┌──────────────┐     │
│  │  Standalone  │  ←───→  │     IDE      │     │
│  └──────────────┘         └──────────────┘     │
└─────────────────────────────────────────────────┘
```

## Skenario Obrolan

### Contoh 1: Standalone minta IDE melakukan R&D

**Sebagai Standalone:**
```
[STANDALONE] > /create myproject Project Baru Proyek aplikasi web
[Project created: Project Baru | ID: myproject]

[STANDALONE] > /use myproject
[Active project: myproject]

[STANDALONE] > Halo IDE, tolong research tentang best practices untuk API rate limiting ya
[Message sent to IDE | ID: msg_1234567890]
```

**Switch ke IDE:**
```
[STANDALONE] > /ide
[Switched to IDE mode]
```

**Sebagai IDE:**
```
[IDE] > /messages
----------------------------------------------------------------------
MESSAGES for IDE (1 total):
----------------------------------------------------------------------

1. [NEW] 2026-10-14T19:30:00
   From: STANDALONE | Type: question
   Subject: Chat message from standalone
   ID: msg_1234567890
----------------------------------------------------------------------

[IDE] > /read msg_1234567890
[Message msg_1234567890 marked as read]

[IDE] > Siap! Saya akan research tentang rate limiting algorithms dan best practices
[Message sent to STANDALONE | ID: msg_1234567891]
```

### Contoh 2: Standalone assign task ke IDE

**Sebagai Standalone:**
```
[STANDALONE] > /assign ImplementLogin Fitur login dengan JWT token dan session management
[Task assigned to IDE | ID: msg_1234567892]
```

**Sebagai IDE:**
```
[IDE] > /messages
[...lihat task assignment...]

[IDE] > Oke, saya mulai kerjakan fitur login dengan JWT
[Message sent to STANDALONE | ID: msg_1234567893]
```

### Contoh 3: IDE submit work report

**Sebagai IDE (setelah selesai mengerjakan):**
```
[IDE] > /report Login feature selesai. JWT token dengan expiry 24 jam, password hashing dengan bcrypt, test coverage 85%
[Work report submitted to Standalone | ID: msg_1234567894]
```

**Sebagai Standalone:**
```
[STANDALONE] > /messages
[...lihat work report...]

[STANDALONE] > /read msg_1234567894

[STANDALONE] > Bagus! Tapi saya temukan issue: token bisa di-reuse setelah expired
[Message sent to IDE | ID: msg_1234567895]
```

### Contoh 4: Standalone request fix

**Sebagai Standalone:**
```
[STANDALONE] > /fix Token JWT masih bisa digunakan setelah expired, perlu invalidation mechanism
[Fix request sent to IDE | ID: msg_1234567896]
```

**Sebagai IDE:**
```
[IDE] > /messages
[...lihat fix request...]

[IDE] > Oke, saya akan tambahkan token blacklist dan invalidation mechanism
[Message sent to STANDALONE | ID: msg_1234567897]
```

### Contoh 5: Check workflow status

**Sebagai Standalone atau IDE:**
```
[STANDALONE] > /status
----------------------------------------------------------------------
WORKFLOW STATUS: Project Baru
----------------------------------------------------------------------
  Project ID: myproject
  Status: active
  Task Assignments: 1
  Work Reports: 1
  Fix Requests: 1
  Total Messages: 7
  Last Activity: 2026-10-14T19:35:00
----------------------------------------------------------------------
```

## Commands Lengkap

### Switch Mode
```
/standalone   - Switch ke mode Standalone (untuk R&D, review, assign task)
/ide          - Switch ke mode IDE (untuk implementation, submit report)
```

### Project Management
```
/projects                    - List semua project
/create <id> <name> <desc>   - Buat project baru
/use <project_id>            - Set active project
/status                      - Cek status workflow project aktif
```

### Communication
```
/messages                    - Lihat semua pesan masuk
/read <message_id>           - Tandai pesan sudah dibaca
<text>                       - Kirim chat message (tanpa command)
```

### Task Management (Standalone only)
```
/assign <title> <desc>       - Assign task ke IDE
/fix <issue_description>     - Request fix ke IDE
```

### Work Reporting (IDE only)
```
/report <summary>            - Submit work report ke Standalone
```

### Other
```
/help                        - Show help
/quit                        - Exit chat bridge
```

## Contoh Conversation Lengkap

Berikut contoh obrolan lengkap antara Standalone dan IDE:

```
=== DAY 1: Planning ===

[STANDALONE] > /create webapp WebApp Aplikasi web dengan authentication
[STANDALONE] > /use webapp
[STANDALONE] > Halo IDE, kita mulai project baru nih
[STANDALONE] > /assign UserAuth Buat sistem authentication dengan JWT, registration, login, password reset
[STANDALONE] > Tolong kerjakan sesuai best practices ya

[IDE] > /ide
[IDE] > /messages
[IDE] > /read msg_xxx
[IDE] > Siap! Saya mulai kerjakan user authentication
[IDE] > Akan pakai JWT + bcrypt + email verification

=== DAY 2-3: Implementation ===

[IDE] > Progress: User model dan registration API selesai
[IDE] > Lanjut login API dan password reset

=== DAY 4: Report ===

[IDE] > /report User authentication selesai. Fitur: registration, login JWT, password reset, role-based access. Test coverage 85%. Files: User.js, authController.js, auth.js, jwt.js

=== DAY 5: Review ===

[STANDALONE] > /standalone
[STANDALONE] > /messages
[STANDALONE] > /read msg_yyy
[STANDALONE] > Bagus! Tapi saya test ada issue: password reset token bisa di-reuse
[STANDALONE] > /fix Password reset token tidak expire setelah digunakan, security risk

=== DAY 6: Fix ===

[IDE] > /ide
[IDE] > /messages
[IDE] > Oke, saya fix token reuse issue
[IDE] > Tambahin token invalidation setelah digunakan

[IDE] > /report Fix applied: token sekarang single-use only. Test coverage naik ke 88%

=== DAY 7: Approval ===

[STANDALONE] > /standalone
[STANDALONE] > /messages
[STANDALONE] > Perfect! Semua issue fixed
[STANDALONE] > /status
[STANDALONE] > APPROVED! Siap deployment
```

## Tips untuk Obrolan Efektif

### Untuk Standalone:
1. **Jelas dan Spesifik**: Jelaskan requirements dengan detail
2. **Berikan Konteks**: Kenapa fitur ini penting
3. **Acceptance Criteria**: Apa yang diharapkan
4. **Review Teliti**: Test sebelum approve
5. **Feedback Konstruktif**: Jelaskan issue dengan jelas

### Untuk IDE:
1. **Konfirmasi Understanding**: Ulangi requirements untuk memastikan
2. **Update Progress**: Beritahu progress secara berkala
3. **Ask Questions**: Jika ada yang unclear, tanya
4. **Detailed Report**: Jelaskan apa yang dikerjakan
5. **Suggest Improvements**: Beritahu jika ada saran

### Contoh Obrolan Natural:

```
[STANDALONE] > IDE, kita perlu fitur search yang bisa filter by date dan category
[STANDALONE] > User sering complain susah cari data lama

[IDE] > Oke, saya bisa pakai Elasticsearch untuk performance
[IDE] > Atau kita bisa pakai PostgreSQL full-text search dulu?

[STANDALONE] > PostgreSQL dulu aja, kalau nanti perlu scale up baru migrate
[STANDALONE] > Yang penting user bisa filter by date range dan multiple categories

[IDE] > Siap! Estimasi 2 hari kerja
[IDE] > Akan saya buat API endpoint /search dengan query params

[STANDALONE] > Perfect! Jangan lupa test dengan data besar ya
[STANDALONE] > Minimal 10k records

[IDE] > Oke, saya akan buat test dataset dan benchmark
[IDE] > Target response time < 500ms

[STANDALONE] > Great! Kerjakan ya
[STANDALONE] > Kalau ada kendala, kabari aja
```

## Workflow Nyata

Dalam penggunaan nyata:

1. **Buka Chat Bridge** di terminal
2. **Switch mode** sesuai peran Anda
3. **Kirim pesan** seperti mengobrol biasa
4. **Check messages** secara berkala
5. **Use commands** untuk task assignment, report, dll
6. **Track progress** dengan /status

## Integration dengan Apps

Chat Bridge terintegrasi dengan:
- **Antigravity Standalone** (port 50999)
- **Antigravity IDE**
- **Shared Workspace** (C:/MitraAI/workspace/)

Semua pesan disimpan di workspace dan bisa diakses oleh kedua apps melalui MCP tools.

## Next Steps

1. Jalankan `python chat_bridge.py`
2. Buat project baru
3. Mulai obrolan antara Standalone dan IDE
4. Experience kolaborasi seperti tim yang solid!

---

**Selamat mengobrol antara Standalone dan IDE!** 🗨️
