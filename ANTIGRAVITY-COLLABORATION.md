# Antigravity Collaboration System
## Standalone <-> IDE Communication Guide

Sistem kolaborasi yang memungkinkan **Antigravity Standalone** dan **Antigravity IDE** bekerja bersama seperti rekan kerja yang berkomunikasi setiap hari.

## Konsep

```
┌─────────────────────────┐
│  Antigravity Standalone │
│  (R&D & Analysis)       │
│                         │
│  - Research             │
│  - Planning             │
│  - Review               │
│  - Quality Control      │
└───────────┬─────────────┘
            │
            │ Messages
            │ (Task, Report, Fix Request)
            │
            ▼
┌─────────────────────────┐
│   Shared Workspace      │
│   C:/MitraAI/workspace/ │
│                         │
│   - messages/           │
│   - projects/           │
│   - reports/            │
└───────────┬─────────────┘
            │
            │ Messages
            │ (Work Report, Answer, Question)
            │
            ▼
┌─────────────────────────┐
│   Antigravity IDE       │
│   (Implementation)      │
│                         │
│   - Coding              │
│   - Testing             │
│   - Documentation       │
│   - Bug Fixing          │
└─────────────────────────┘
```

## Workflow

### Phase 1: R&D (Standalone)
1. **Research**: Standalone menganalisis kebutuhan
2. **Planning**: Membuat spesifikasi dan requirements
3. **Assignment**: Assign task ke IDE dengan acceptance criteria

### Phase 2: Implementation (IDE)
1. **Development**: IDE mengerjakan task sesuai spesifikasi
2. **Testing**: Write unit tests dan integration tests
3. **Reporting**: Submit work report ke Standalone

### Phase 3: Review (Standalone)
1. **Code Review**: Review quality dan best practices
2. **Testing**: Test semua functionality
3. **Validation**: Verify acceptance criteria

### Phase 4: Fix (Jika perlu)
1. **Feedback**: Standalone kirim fix request jika ada issue
2. **Fixing**: IDE memperbaiki issues
3. **Re-report**: IDE submit updated work report

### Phase 5: Approval
1. **Final Review**: Standalone verify semua fixes
2. **Approval**: Approve jika semua criteria met
3. **Deployment**: Siap untuk deployment

## Contoh Skenario

### Skenario: Membuat User Authentication

**Day 1 - Standalone (R&D)**
```
Standalone: "Kita perlu buat fitur authentication untuk WebApp"
  -> Research JWT vs Session-based auth
  -> Analyze security best practices
  -> Define requirements:
     - User registration
     - Login dengan JWT
     - Password reset
     - Role-based access
  -> Assign task ke IDE
```

**Day 2-4 - IDE (Implementation)**
```
IDE: Menerima task "Implement User Authentication"
  -> Setup project structure
  -> Create user model
  -> Implement registration API
  -> Implement login API dengan JWT
  -> Implement password reset
  -> Add role-based access control
  -> Write tests (85% coverage)
  -> Submit work report
```

**Day 5 - Standalone (Review)**
```
Standalone: Review hasil pekerjaan
  -> Test semua endpoints
  -> Check security
  -> Found issues:
     - Password reset token bisa di-reuse
     - Missing rate limiting
  -> Request fix ke IDE
```

**Day 6 - IDE (Fixing)**
```
IDE: Menerima fix request
  -> Fix token reuse issue
  -> Add rate limiting
  -> Add security logging
  -> Test coverage: 85% -> 88%
  -> Submit updated report
```

**Day 7 - Standalone (Approval)**
```
Standalone: Final review
  -> Test all fixes
  -> Verify security
  -> All criteria met
  -> APPROVED!
```

## MCP Tools

### Untuk Standalone

#### `send_rnd_request(project_id, topic, requirements, priority)`
Minta IDE melakukan R&D tentang topik tertentu.

```python
send_rnd_request(
    project_id="webapp-2026",
    topic="Best practices for API rate limiting",
    requirements="Research berbagai algoritma rate limiting dan rekomendasinya",
    priority="normal"
)
```

#### `assign_task(project_id, task_title, task_description, acceptance_criteria, priority)`
Assign pekerjaan ke IDE.

```python
assign_task(
    project_id="webapp-2026",
    task_title="Implement User Authentication",
    task_description="Buat sistem auth dengan JWT...",
    acceptance_criteria="- User bisa register\n- User bisa login\n- Token valid 24 jam",
    priority="high"
)
```

#### `request_fix(project_id, task_id, issue_description, expected_behavior, actual_behavior, priority)`
Minta IDE memperbaiki issue.

```python
request_fix(
    project_id="webapp-2026",
    task_id="auth-001",
    issue_description="Password reset token bisa di-reuse",
    expected_behavior="Token hanya bisa digunakan sekali",
    actual_behavior="Token bisa digunakan berkali-kali",
    priority="high"
)
```

#### `get_messages(for_app="standalone", unread_only=True)`
Cek pesan dari IDE.

```python
messages = get_messages(for_app="standalone", unread_only=True)
```

### Untuk IDE

#### `submit_work_report(project_id, task_id, summary, details, files_changed, issues_found, suggestions)`
Submit laporan pekerjaan ke Standalone.

```python
submit_work_report(
    project_id="webapp-2026",
    task_id="auth-001",
    summary="User Authentication System selesai",
    details="Implementasi lengkap dengan JWT, password reset, dll",
    files_changed="src/models/User.js, src/controllers/auth.js, ...",
    issues_found="None",
    suggestions="Tambahkan 2FA untuk security tambahan"
)
```

#### `send_answer(from_app="ide", to_app="standalone", project_id, answer)`
Jawab pertanyaan dari Standalone.

```python
send_answer(
    from_app="ide",
    to_app="standalone",
    project_id="webapp-2026",
    answer="JWT lebih cocok untuk API karena stateless..."
)
```

#### `get_messages(for_app="ide", unread_only=True)`
Cek pesan dari Standalone.

```python
messages = get_messages(for_app="ide", unread_only=True)
```

### Untuk Keduanya

#### `create_project(project_id, name, description)`
Buat project baru.

```python
create_project(
    project_id="webapp-2026",
    name="WebApp Project",
    description="Aplikasi web dengan authentication dan dashboard"
)
```

#### `list_projects()`
List semua project.

```python
projects = list_projects()
```

#### `get_workflow_status(project_id)`
Cek status workflow project.

```python
status = get_workflow_status("webapp-2026")
# Returns:
# {
#   "project_id": "webapp-2026",
#   "task_assignments": 1,
#   "work_reports": 2,
#   "fix_requests": 1,
#   "total_messages": 4
# }
```

## Shared Workspace

Semua data kolaborasi disimpan di:

```
C:/MitraAI/workspace/
├── messages/           # Pesan antara apps
│   ├── msg_1791979881_16516.json
│   ├── msg_1791979883_16516.json
│   └── ...
├── projects/           # Data project
│   ├── webapp-2026.json
│   └── ...
└── reports/            # Work reports
    └── ...
```

### Message Format

```json
{
  "id": "msg_1791979881_16516",
  "timestamp": "2026-10-14T18:30:00",
  "type": "task_assignment",
  "from": "standalone",
  "to": "ide",
  "subject": "Task: Implement User Authentication",
  "content": "# Task Assignment\n\n...",
  "project_id": "webapp-2026",
  "task_id": "auth-001",
  "priority": "high",
  "read": false
}
```

## Message Types

| Type | From | To | Deskripsi |
|------|------|----|-----------|
| `rnd_request` | Standalone | IDE | Minta R&D tentang topik |
| `task_assignment` | Standalone | IDE | Assign pekerjaan |
| `work_report` | IDE | Standalone | Laporan pekerjaan selesai |
| `fix_request` | Standalone | IDE | Minta perbaikan issue |
| `analysis_result` | Standalone | IDE | Hasil analisis |
| `question` | Both | Both | Pertanyaan |
| `answer` | Both | Both | Jawaban |
| `status_update` | Both | Both | Update status |

## Best Practices

### Untuk Standalone

1. **Spesifik dalam Assignment**
   - Jelaskan requirements dengan jelas
   - Sertakan acceptance criteria
   - Berikan konteks yang cukup

2. **Review dengan Teliti**
   - Test semua functionality
   - Check security best practices
   - Verify code quality

3. **Feedback yang Konstruktif**
   - Jelaskan issue dengan jelas
   - Berikan expected vs actual behavior
   - Sertakan steps to reproduce

### Untuk IDE

1. **Follow Specifications**
   - Implement sesuai requirements
   - Jangan deviate tanpa diskusi
   - Ask questions jika unclear

2. **Quality First**
   - Write clean code
   - Add comprehensive tests
   - Document your code

3. **Detailed Reports**
   - Jelaskan apa yang dikerjakan
   - List semua files changed
   - Sertakan suggestions untuk improvement

### Komunikasi

1. **Clear Subject Lines**
   - Gunakan format yang konsisten
   - Include project/task ID
   - Make it searchable

2. **Structured Content**
   - Use markdown formatting
   - Break down complex topics
   - Include code snippets when relevant

3. **Timely Responses**
   - Check messages regularly
   - Respond within reasonable time
   - Update status jika ada delay

## Demo

Jalankan demo untuk melihat workflow lengkap:

```bash
cd C:\Users\Administrator\Documents\Qoder\2026-10-14\a5189cf2\MitraAI-docs
python demo_antigravity_collaboration.py
```

Demo menunjukkan:
- Project creation
- R&D phase
- Task assignment
- Implementation
- Work report
- Review & fix request
- Fixing issues
- Final approval

## Configuration

MCP server sudah dikonfigurasi di:
```
C:\Users\Administrator\.gemini\antigravity\mcp_config.json
```

```json
{
  "mcpServers": {
    "antigravity-collaboration": {
      "command": "python",
      "args": [
        "C:/Users/Administrator/.gemini/antigravity/mcp/collaboration/mcp_server.py"
      ]
    }
  }
}
```

## Troubleshooting

### Messages tidak muncul
- Check workspace directory: `C:/MitraAI/workspace/messages/`
- Verify permissions
- Check message format

### Project tidak ditemukan
- Verify project_id
- Check `C:/MitraAI/workspace/projects/`
- Create project dulu jika belum ada

### MCP tools tidak available
- Restart MCP server
- Check mcp_config.json
- Verify Python path

## Benefits

### Untuk Standalone
- ✓ Fokus pada R&D dan strategy
- ✓ Quality control yang lebih baik
- ✓ Clear communication channel
- ✓ Structured workflow

### Untuk IDE
- ✓ Clear requirements dan expectations
- ✓ Structured feedback
- ✓ Focus pada implementation
- ✓ Easy to track tasks

### Untuk Project
- ✓ Better quality output
- ✓ Clear audit trail
- ✓ Efficient collaboration
- ✓ Reduced miscommunication

## Future Enhancements

- [ ] Real-time notifications
- [ ] File attachments support
- [ ] Code review integration
- [ ] Automated testing integration
- [ ] Performance metrics
- [ ] Dashboard UI
- [ ] Mobile notifications

---

**Antigravity Standalone + IDE = Tim yang Solid!**

Mereka bekerja bersama seperti rekan kerja yang berkomunikasi setiap hari, menghasilkan code berkualitas tinggi melalui kolaborasi yang terstruktur.
