#!/usr/bin/env python3
"""
MCP Server: Antigravity Collaboration Tools
Tools untuk komunikasi antara Antigravity Standalone dan IDE.

Tools:
- send_rnd_request: Standalone minta IDE melakukan R&D
- assign_task: Standalone assign pekerjaan ke IDE
- submit_work_report: IDE submit laporan pekerjaan
- request_fix: Standalone minta IDE memperbaiki sesuatu
- send_question: Tanya ke app lain
- send_answer: Jawab pertanyaan
- get_messages: Ambil pesan masuk
- get_workflow_status: Cek status workflow project
- create_project: Buat project baru
- list_projects: List semua project
"""

from mcp.server.fastmcp import FastMCP
import json
import sys
import os

# Add parent directory to path to import collaboration_bridge
sys.path.insert(0, os.path.dirname(__file__))
from collaboration_bridge import (
    send_message,
    get_messages,
    mark_as_read,
    create_project,
    get_project,
    update_project,
    list_projects,
    get_workflow_status
)

# Initialize MCP server
mcp = FastMCP("antigravity-collaboration")


@mcp.tool()
def send_rnd_request(
    project_id: str,
    topic: str,
    requirements: str,
    priority: str = "normal"
) -> str:
    """
    [Standalone -> IDE] Minta IDE melakukan R&D tentang topik tertentu.
    
    Args:
        project_id: ID project
        topic: Topik yang ingin diteliti
        requirements: Kebutuhan/spesifikasi R&D
        priority: Prioritas (low, normal, high, urgent)
    
    Returns:
        Message ID
    """
    content = f"""
# R&D Request

**Topik**: {topic}

**Kebutuhan**:
{requirements}

**Prioritas**: {priority}

---
Tolong lakukan R&D dan berikan hasil penelitian yang komprehensif.
""".strip()
    
    msg_id = send_message(
        msg_type="rnd_request",
        from_app="standalone",
        to_app="ide",
        subject=f"R&D Request: {topic}",
        content=content,
        project_id=project_id,
        priority=priority
    )
    
    return json.dumps({
        "status": "sent",
        "message_id": msg_id,
        "message": f"R&D request tentang '{topic}' sudah dikirim ke IDE"
    }, indent=2)


@mcp.tool()
def assign_task(
    project_id: str,
    task_title: str,
    task_description: str,
    acceptance_criteria: str,
    priority: str = "normal"
) -> str:
    """
    [Standalone -> IDE] Assign pekerjaan ke IDE.
    
    Args:
        project_id: ID project
        task_title: Judul task
        task_description: Deskripsi pekerjaan
        acceptance_criteria: Kriteria penerimaan (definition of done)
        priority: Prioritas (low, normal, high, urgent)
    
    Returns:
        Message ID
    """
    content = f"""
# Task Assignment

**Judul**: {task_title}

**Deskripsi**:
{task_description}

**Acceptance Criteria**:
{acceptance_criteria}

**Prioritas**: {priority}

---
Tolong kerjakan task ini sesuai spesifikasi.
""".strip()
    
    msg_id = send_message(
        msg_type="task_assignment",
        from_app="standalone",
        to_app="ide",
        subject=f"Task: {task_title}",
        content=content,
        project_id=project_id,
        priority=priority
    )
    
    return json.dumps({
        "status": "sent",
        "message_id": msg_id,
        "message": f"Task '{task_title}' sudah di-assign ke IDE"
    }, indent=2)


@mcp.tool()
def submit_work_report(
    project_id: str,
    task_id: str,
    summary: str,
    details: str,
    files_changed: str = "",
    issues_found: str = "",
    suggestions: str = ""
) -> str:
    """
    [IDE -> Standalone] Submit laporan pekerjaan yang sudah diselesaikan.
    
    Args:
        project_id: ID project
        task_id: ID task yang dikerjakan
        summary: Ringkasan pekerjaan
        details: Detail implementasi
        files_changed: List file yang diubah
        issues_found: Masalah yang ditemukan (jika ada)
        suggestions: Saran untuk improvement (jika ada)
    
    Returns:
        Message ID
    """
    content = f"""
# Work Report

**Task ID**: {task_id}

## Ringkasan
{summary}

## Detail Implementasi
{details}

## Files Changed
{files_changed if files_changed else "N/A"}

## Issues Found
{issues_found if issues_found else "None"}

## Suggestions
{suggestions if suggestions else "None"}

---
Pekerjaan selesai, mohon review.
""".strip()
    
    msg_id = send_message(
        msg_type="work_report",
        from_app="ide",
        to_app="standalone",
        subject=f"Work Report: Task {task_id}",
        content=content,
        project_id=project_id,
        task_id=task_id
    )
    
    return json.dumps({
        "status": "sent",
        "message_id": msg_id,
        "message": f"Work report untuk task {task_id} sudah dikirim ke Standalone"
    }, indent=2)


@mcp.tool()
def request_fix(
    project_id: str,
    task_id: str,
    issue_description: str,
    expected_behavior: str,
    actual_behavior: str,
    steps_to_reproduce: str = "",
    priority: str = "high"
) -> str:
    """
    [Standalone -> IDE] Minta IDE memperbaiki masalah yang ditemukan.
    
    Args:
        project_id: ID project
        task_id: ID task yang perlu diperbaiki
        issue_description: Deskripsi masalah
        expected_behavior: Behavior yang diharapkan
        actual_behavior: Behavior yang terjadi
        steps_to_reproduce: Langkah untuk reproduce (optional)
        priority: Prioritas (low, normal, high, urgent)
    
    Returns:
        Message ID
    """
    content = f"""
# Fix Request

**Task ID**: {task_id}

## Issue Description
{issue_description}

## Expected Behavior
{expected_behavior}

## Actual Behavior
{actual_behavior}

## Steps to Reproduce
{steps_to_reproduce if steps_to_reproduce else "N/A"}

**Prioritas**: {priority}

---
Tolong perbaiki masalah ini.
""".strip()
    
    msg_id = send_message(
        msg_type="fix_request",
        from_app="standalone",
        to_app="ide",
        subject=f"Fix Request: Task {task_id}",
        content=content,
        project_id=project_id,
        task_id=task_id,
        priority=priority
    )
    
    return json.dumps({
        "status": "sent",
        "message_id": msg_id,
        "message": f"Fix request untuk task {task_id} sudah dikirim ke IDE"
    }, indent=2)


@mcp.tool()
def send_question(
    from_app: str,
    to_app: str,
    project_id: str,
    question: str,
    context: str = ""
) -> str:
    """
    Kirim pertanyaan ke app lain.
    
    Args:
        from_app: Pengirim ("standalone" atau "ide")
        to_app: Penerima ("standalone" atau "ide")
        project_id: ID project
        question: Pertanyaan
        context: Konteks tambahan (optional)
    
    Returns:
        Message ID
    """
    content = f"""
# Question

{question}

## Context
{context if context else "N/A"}

---
Mohon jawaban dan penjelasannya.
""".strip()
    
    msg_id = send_message(
        msg_type="question",
        from_app=from_app,
        to_app=to_app,
        subject=f"Question about project",
        content=content,
        project_id=project_id
    )
    
    return json.dumps({
        "status": "sent",
        "message_id": msg_id,
        "message": f"Pertanyaan sudah dikirim dari {from_app} ke {to_app}"
    }, indent=2)


@mcp.tool()
def send_answer(
    from_app: str,
    to_app: str,
    project_id: str,
    answer: str,
    additional_notes: str = ""
) -> str:
    """
    Jawab pertanyaan dari app lain.
    
    Args:
        from_app: Pengirim ("standalone" atau "ide")
        to_app: Penerima ("standalone" atau "ide")
        project_id: ID project
        answer: Jawaban
        additional_notes: Catatan tambahan (optional)
    
    Returns:
        Message ID
    """
    content = f"""
# Answer

{answer}

## Additional Notes
{additional_notes if additional_notes else "None"}
""".strip()
    
    msg_id = send_message(
        msg_type="answer",
        from_app=from_app,
        to_app=to_app,
        subject=f"Answer to your question",
        content=content,
        project_id=project_id
    )
    
    return json.dumps({
        "status": "sent",
        "message_id": msg_id,
        "message": f"Jawaban sudah dikirim dari {from_app} ke {to_app}"
    }, indent=2)


@mcp.tool()
def get_messages(
    for_app: str,
    msg_type: str = None,
    unread_only: bool = False
) -> str:
    """
    Ambil pesan masuk untuk app tertentu.
    
    Args:
        for_app: App yang menerima ("standalone" atau "ide")
        msg_type: Filter by tipe pesan (optional)
        unread_only: Hanya ambil yang belum dibaca
    
    Returns:
        JSON string berisi list pesan
    """
    messages = get_messages(for_app, msg_type, unread_only)
    
    return json.dumps({
        "status": "ok",
        "for_app": for_app,
        "total": len(messages),
        "messages": messages
    }, indent=2)


@mcp.tool()
def mark_message_read(message_id: str) -> str:
    """
    Tandai pesan sudah dibaca.
    
    Args:
        message_id: ID pesan
    
    Returns:
        Status
    """
    success = mark_as_read(message_id)
    
    return json.dumps({
        "status": "ok" if success else "error",
        "message_id": message_id,
        "message": "Marked as read" if success else "Message not found"
    }, indent=2)


@mcp.tool()
def get_workflow_status(project_id: str) -> str:
    """
    Cek status workflow untuk project.
    
    Args:
        project_id: ID project
    
    Returns:
        JSON string berisi status workflow
    """
    status = get_workflow_status(project_id)
    return json.dumps(status, indent=2)


@mcp.tool()
def create_project(
    project_id: str,
    name: str,
    description: str
) -> str:
    """
    Buat project baru di shared workspace.
    
    Args:
        project_id: ID project
        name: Nama project
        description: Deskripsi project
    
    Returns:
        Project ID
    """
    pid = create_project(project_id, name, description)
    
    return json.dumps({
        "status": "ok",
        "project_id": pid,
        "message": f"Project '{name}' sudah dibuat"
    }, indent=2)


@mcp.tool()
def list_projects() -> str:
    """
    List semua project di shared workspace.
    
    Returns:
        JSON string berisi list projects
    """
    projects = list_projects()
    
    return json.dumps({
        "status": "ok",
        "total": len(projects),
        "projects": projects
    }, indent=2)


@mcp.tool()
def get_project(project_id: str) -> str:
    """
    Ambil detail project.
    
    Args:
        project_id: ID project
    
    Returns:
        JSON string berisi detail project
    """
    project = get_project(project_id)
    
    if not project:
        return json.dumps({
            "status": "error",
            "message": "Project not found"
        }, indent=2)
    
    return json.dumps({
        "status": "ok",
        "project": project
    }, indent=2)


@mcp.tool()
def introduce_collaboration() -> str:
    """
    Perkenalan sistem kolaborasi Antigravity.
    
    Returns:
        Informasi tentang sistem kolaborasi
    """
    return """
# Antigravity Collaboration System

Halo! Saya adalah bridge yang menghubungkan Antigravity Standalone dan Antigravity IDE.

## Cara Kerja Kami

Kami bekerja seperti rekan kerja yang berkomunikasi setiap hari:

### 1. R&D Phase (Standalone)
- Standalone melakukan research & analysis
- Mengidentifikasi kebutuhan dan masalah
- Membuat spesifikasi dan requirements

### 2. Task Assignment (Standalone -> IDE)
- Standalone assign pekerjaan ke IDE
- Menyertakan acceptance criteria
- Menetapkan prioritas

### 3. Implementation (IDE)
- IDE mengerjakan task sesuai spesifikasi
- Menulis kode, test, dokumentasi
- Submit work report ketika selesai

### 4. Review & Analysis (Standalone)
- Standalone review hasil pekerjaan
- Melakukan testing dan validasi
- Analisis apakah sesuai requirements

### 5. Fix Request (Jika perlu)
- Standalone minta perbaikan jika ada issue
- IDE melakukan fix
- Repeat sampai满意

## Tools yang Tersedia

### Untuk Standalone:
- `send_rnd_request()` - Minta IDE melakukan R&D
- `assign_task()` - Assign pekerjaan ke IDE
- `request_fix()` - Minta perbaikan
- `send_question()` - Tanya ke IDE
- `get_messages()` - Cek pesan dari IDE

### Untuk IDE:
- `submit_work_report()` - Submit laporan pekerjaan
- `send_answer()` - Jawab pertanyaan
- `send_question()` - Tanya ke Standalone
- `get_messages()` - Cek pesan dari Standalone

### Untuk Keduanya:
- `create_project()` - Buat project baru
- `list_projects()` - List semua project
- `get_project()` - Detail project
- `get_workflow_status()` - Cek status workflow

## Workflow Example

```
Day 1:
  Standalone: "Kita perlu buat fitur X untuk project Y"
  Standalone -> assign_task("Implement feature X", ...)
  
Day 2:
  IDE: Mengerjakan task
  IDE -> submit_work_report("Feature X selesai", ...)
  
Day 3:
  Standalone: Review hasil
  Standalone: "Ada bug di line 42, tolong fix"
  Standalone -> request_fix("Bug in feature X", ...)
  
Day 4:
  IDE: Fix bug
  IDE -> submit_work_report("Bug fixed", ...)
  
Day 5:
  Standalone: Test ulang
  Standalone: "Perfect! Feature X approved"
```

## Shared Workspace

Semua data disimpan di:
```
C:/MitraAI/workspace/
├── messages/     # Pesan antara apps
├── projects/     # Data project
└── reports/      # Work reports
```

Mari bekerja sama seperti tim yang solid!
"""


if __name__ == "__main__":
    print("Starting Antigravity Collaboration MCP Server...")
    print()
    mcp.run()
