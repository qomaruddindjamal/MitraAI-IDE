#!/usr/bin/env python3
"""
Antigravity Standalone <-> Antigravity IDE Communication Bridge
Sistem kolaborasi seperti rekan kerja yang berkomunikasi setiap hari.

Workflow:
1. Standalone melakukan R&D
2. Standalone kirim task ke IDE
3. IDE mengerjakan
4. IDE kirim report balik ke Standalone
5. Standalone analisis & R&D ulang jika perlu
6. Repeat sampai selesai

Usage:
  python collaboration_bridge.py
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any
from enum import Enum

# Shared workspace
WORKSPACE_DIR = Path(os.getenv("MITRAAI_WORKSPACE", "C:/MitraAI/workspace"))
MESSAGES_DIR = WORKSPACE_DIR / "messages"
PROJECTS_DIR = WORKSPACE_DIR / "projects"
REPORTS_DIR = WORKSPACE_DIR / "reports"

# Ensure directories exist
for dir in [WORKSPACE_DIR, MESSAGES_DIR, PROJECTS_DIR, REPORTS_DIR]:
    dir.mkdir(parents=True, exist_ok=True)


class MessageType(Enum):
    RND_REQUEST = "rnd_request"          # Standalone -> IDE: Minta R&D
    TASK_ASSIGNMENT = "task_assignment"  # Standalone -> IDE: Assign pekerjaan
    WORK_REPORT = "work_report"          # IDE -> Standalone: Laporan pekerjaan
    ANALYSIS_RESULT = "analysis_result"  # Standalone -> IDE: Hasil analisis
    FIX_REQUEST = "fix_request"          # Standalone -> IDE: Minta perbaikan
    STATUS_UPDATE = "status_update"      # Both: Update status
    QUESTION = "question"                # Both: Tanya ke yang lain
    ANSWER = "answer"                    # Both: Jawab pertanyaan


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    NEEDS_FIX = "needs_fix"
    CANCELLED = "cancelled"


class Message:
    def __init__(
        self,
        msg_type: MessageType,
        from_app: str,  # "standalone" or "ide"
        to_app: str,    # "standalone" or "ide"
        subject: str,
        content: str,
        project_id: Optional[str] = None,
        task_id: Optional[str] = None,
        attachments: Optional[List[str]] = None,
        priority: str = "normal"  # low, normal, high, urgent
    ):
        self.id = f"msg_{int(time.time())}_{os.getpid()}"
        self.timestamp = datetime.now().isoformat()
        self.type = msg_type.value
        self.from_app = from_app
        self.to_app = to_app
        self.subject = subject
        self.content = content
        self.project_id = project_id
        self.task_id = task_id
        self.attachments = attachments or []
        self.priority = priority
        self.read = False

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "type": self.type,
            "from": self.from_app,
            "to": self.to_app,
            "subject": self.subject,
            "content": self.content,
            "project_id": self.project_id,
            "task_id": self.task_id,
            "attachments": self.attachments,
            "priority": self.priority,
            "read": self.read
        }

    def save(self):
        """Save message to shared workspace"""
        filename = f"{self.timestamp.replace(':', '-')}_{self.id}.json"
        filepath = MESSAGES_DIR / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        return filepath


class Project:
    def __init__(self, project_id: str, name: str, description: str):
        self.id = project_id
        self.name = name
        self.description = description
        self.created_at = datetime.now().isoformat()
        self.status = "active"
        self.tasks = []
        self.rnd_notes = []
        self.reports = []

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "status": self.status,
            "tasks": self.tasks,
            "rnd_notes": self.rnd_notes,
            "reports": self.reports
        }

    def save(self):
        """Save project to shared workspace"""
        filepath = PROJECTS_DIR / f"{self.id}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        return filepath


def send_message(
    msg_type: str,
    from_app: str,
    to_app: str,
    subject: str,
    content: str,
    project_id: Optional[str] = None,
    task_id: Optional[str] = None,
    priority: str = "normal"
) -> str:
    """
    Kirim pesan dari satu app ke app lainnya.
    
    Args:
        msg_type: Tipe pesan (rnd_request, task_assignment, work_report, dll)
        from_app: Pengirim ("standalone" atau "ide")
        to_app: Penerima ("standalone" atau "ide")
        subject: Judul pesan
        content: Isi pesan
        project_id: ID project (optional)
        task_id: ID task (optional)
        priority: Prioritas (low, normal, high, urgent)
    
    Returns:
        Message ID
    """
    msg = Message(
        msg_type=MessageType(msg_type),
        from_app=from_app,
        to_app=to_app,
        subject=subject,
        content=content,
        project_id=project_id,
        task_id=task_id,
        priority=priority
    )
    filepath = msg.save()
    return msg.id


def get_messages(
    for_app: str,
    msg_type: Optional[str] = None,
    unread_only: bool = False
) -> List[Dict]:
    """
    Ambil pesan untuk app tertentu.
    
    Args:
        for_app: App yang menerima ("standalone" atau "ide")
        msg_type: Filter by tipe pesan (optional)
        unread_only: Hanya ambil yang belum dibaca
    
    Returns:
        List of messages
    """
    messages = []
    
    for filepath in MESSAGES_DIR.glob("*.json"):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                msg = json.load(f)
                
                if msg.get('to') != for_app:
                    continue
                
                if msg_type and msg.get('type') != msg_type:
                    continue
                
                if unread_only and msg.get('read', False):
                    continue
                
                messages.append(msg)
        except Exception as e:
            continue
    
    # Sort by timestamp
    messages.sort(key=lambda x: x.get('timestamp', ''))
    return messages


def mark_as_read(message_id: str):
    """Tandai pesan sudah dibaca"""
    for filepath in MESSAGES_DIR.glob("*.json"):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                msg = json.load(f)
            
            if msg.get('id') == message_id:
                msg['read'] = True
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(msg, f, indent=2, ensure_ascii=False)
                return True
        except:
            continue
    return False


def create_project(project_id: str, name: str, description: str) -> str:
    """
    Buat project baru di shared workspace.
    
    Args:
        project_id: ID project
        name: Nama project
        description: Deskripsi project
    
    Returns:
        Project ID
    """
    project = Project(project_id, name, description)
    project.save()
    return project.id


def get_project(project_id: str) -> Optional[Dict]:
    """Ambil detail project"""
    filepath = PROJECTS_DIR / f"{project_id}.json"
    if not filepath.exists():
        return None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def update_project(project_id: str, updates: Dict) -> bool:
    """Update project data"""
    filepath = PROJECTS_DIR / f"{project_id}.json"
    if not filepath.exists():
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        project = json.load(f)
    
    project.update(updates)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(project, f, indent=2, ensure_ascii=False)
    
    return True


def list_projects() -> List[Dict]:
    """List semua project"""
    projects = []
    for filepath in PROJECTS_DIR.glob("*.json"):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                projects.append(json.load(f))
        except:
            continue
    return projects


def get_workflow_status(project_id: str) -> Dict:
    """
    Ambil status workflow untuk project.
    
    Returns:
        Dict dengan status R&D, tasks, reports, dll
    """
    project = get_project(project_id)
    if not project:
        return {"error": "Project not found"}
    
    # Count messages by type
    all_messages = get_messages("standalone") + get_messages("ide")
    project_messages = [m for m in all_messages if m.get('project_id') == project_id]
    
    rnd_requests = len([m for m in project_messages if m.get('type') == 'rnd_request'])
    task_assignments = len([m for m in project_messages if m.get('type') == 'task_assignment'])
    work_reports = len([m for m in project_messages if m.get('type') == 'work_report'])
    fix_requests = len([m for m in project_messages if m.get('type') == 'fix_request'])
    
    return {
        "project_id": project_id,
        "project_name": project.get('name'),
        "status": project.get('status'),
        "rnd_requests": rnd_requests,
        "task_assignments": task_assignments,
        "work_reports": work_reports,
        "fix_requests": fix_requests,
        "total_messages": len(project_messages),
        "last_activity": project_messages[-1]['timestamp'] if project_messages else None
    }


if __name__ == "__main__":
    print("=" * 60)
    print("ANTIGRAVITY COLLABORATION BRIDGE")
    print("Standalone <-> IDE Communication System")
    print("=" * 60)
    print()
    print(f"Workspace: {WORKSPACE_DIR}")
    print(f"Messages: {MESSAGES_DIR}")
    print(f"Projects: {PROJECTS_DIR}")
    print()
    print("Bridge is ready for communication!")
    print()
    print("Available functions:")
    print("  - send_message()")
    print("  - get_messages()")
    print("  - mark_as_read()")
    print("  - create_project()")
    print("  - get_project()")
    print("  - update_project()")
    print("  - list_projects()")
    print("  - get_workflow_status()")
