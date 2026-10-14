#!/usr/bin/env python3
"""
Interactive Chat Bridge: Antigravity Standalone <-> IDE
Interface untuk komunikasi real-time seperti orang mengobrol.

Usage:
  python chat_bridge.py

Commands:
  /standalone   - Switch ke mode Standalone
  /ide          - Switch ke mode IDE
  /messages     - Lihat pesan masuk
  /send <msg>   - Kirim pesan
  /projects     - List semua project
  /status       - Cek status workflow
  /help         - Show help
  /quit         - Exit
"""

import sys
import os
import time
from datetime import datetime

# Add MCP directory to path
sys.path.insert(0, r"C:\Users\Administrator\.gemini\antigravity\mcp\collaboration")
from collaboration_bridge import (
    send_message,
    get_messages,
    mark_as_read,
    list_projects,
    get_workflow_status,
    create_project
)


class ChatBridge:
    def __init__(self):
        self.current_app = "standalone"  # or "ide"
        self.current_project = None
        self.running = True
        
    def print_header(self):
        print("\n" + "=" * 70)
        print("ANTIGRAVITY CHAT BRIDGE".center(70))
        print("Real-time Communication between Standalone and IDE".center(70))
        print("=" * 70)
        
    def print_prompt(self):
        app_name = "STANDALONE" if self.current_app == "standalone" else "IDE"
        project_info = f" | Project: {self.current_project}" if self.current_project else ""
        print(f"\n[{app_name}{project_info}] > ", end="", flush=True)
        
    def show_help(self):
        print("\n" + "-" * 70)
        print("COMMANDS:")
        print("-" * 70)
        print("  /standalone       - Switch ke mode Standalone (R&D)")
        print("  /ide              - Switch ke mode IDE (Implementation)")
        print("  /messages         - Lihat pesan masuk")
        print("  /read <msg_id>    - Tandai pesan sudah dibaca")
        print("  /projects         - List semua project")
        print("  /use <project_id> - Set active project")
        print("  /create <id> <name> <desc> - Buat project baru")
        print("  /status           - Cek status workflow")
        print("  /assign <title> <desc> - Assign task ke IDE")
        print("  /report <summary> - Submit work report")
        print("  /fix <issue>      - Request fix")
        print("  /help             - Show this help")
        print("  /quit             - Exit chat bridge")
        print("-" * 70)
        
    def show_messages(self):
        messages = get_messages(self.current_app, unread_only=False)
        
        if not messages:
            print("\n[No messages]")
            return
        
        print("\n" + "-" * 70)
        print(f"MESSAGES for {self.current_app.upper()} ({len(messages)} total):")
        print("-" * 70)
        
        for i, msg in enumerate(messages[-10:], 1):  # Show last 10
            read_status = "[READ]" if msg.get('read') else "[NEW]"
            timestamp = msg.get('timestamp', '')[:19]
            from_app = msg.get('from', 'unknown').upper()
            msg_type = msg.get('type', 'unknown')
            subject = msg.get('subject', 'No subject')
            
            print(f"\n{i}. {read_status} {timestamp}")
            print(f"   From: {from_app} | Type: {msg_type}")
            print(f"   Subject: {subject}")
            print(f"   ID: {msg.get('id')}")
            
        print("-" * 70)
        
    def show_projects(self):
        projects = list_projects()
        
        if not projects:
            print("\n[No projects yet. Create one with: /create <id> <name> <desc>]")
            return
        
        print("\n" + "-" * 70)
        print(f"PROJECTS ({len(projects)} total):")
        print("-" * 70)
        
        for i, proj in enumerate(projects, 1):
            print(f"\n{i}. {proj.get('name')}")
            print(f"   ID: {proj.get('id')}")
            print(f"   Description: {proj.get('description')}")
            print(f"   Status: {proj.get('status')}")
            print(f"   Created: {proj.get('created_at', '')[:19]}")
            
        print("-" * 70)
        
    def show_status(self):
        if not self.current_project:
            print("\n[No active project. Use: /use <project_id>]")
            return
        
        status = get_workflow_status(self.current_project)
        
        if 'error' in status:
            print(f"\n[Error: {status.get('error')}]")
            return
        
        print("\n" + "-" * 70)
        print(f"WORKFLOW STATUS: {status.get('project_name')}")
        print("-" * 70)
        print(f"  Project ID: {status.get('project_id')}")
        print(f"  Status: {status.get('status')}")
        print(f"  Task Assignments: {status.get('task_assignments', 0)}")
        print(f"  Work Reports: {status.get('work_reports', 0)}")
        print(f"  Fix Requests: {status.get('fix_requests', 0)}")
        print(f"  Total Messages: {status.get('total_messages', 0)}")
        print(f"  Last Activity: {status.get('last_activity', 'N/A')}")
        print("-" * 70)
        
    def send_chat_message(self, content):
        if not self.current_project:
            print("\n[Error: No active project. Use: /use <project_id>]")
            return
        
        to_app = "ide" if self.current_app == "standalone" else "standalone"
        
        msg_id = send_message(
            msg_type="question",
            from_app=self.current_app,
            to_app=to_app,
            subject=f"Chat message from {self.current_app}",
            content=content,
            project_id=self.current_project
        )
        
        print(f"\n[Message sent to {to_app.upper()} | ID: {msg_id}]")
        
    def assign_task(self, title, description):
        if not self.current_project:
            print("\n[Error: No active project. Use: /use <project_id>]")
            return
        
        if self.current_app != "standalone":
            print("\n[Error: Only Standalone can assign tasks]")
            return
        
        msg_id = send_message(
            msg_type="task_assignment",
            from_app="standalone",
            to_app="ide",
            subject=f"Task: {title}",
            content=f"# Task Assignment\n\n**Judul**: {title}\n\n**Deskripsi**:\n{description}",
            project_id=self.current_project,
            priority="normal"
        )
        
        print(f"\n[Task assigned to IDE | ID: {msg_id}]")
        
    def submit_report(self, summary):
        if not self.current_project:
            print("\n[Error: No active project. Use: /use <project_id>]")
            return
        
        if self.current_app != "ide":
            print("\n[Error: Only IDE can submit work reports]")
            return
        
        msg_id = send_message(
            msg_type="work_report",
            from_app="ide",
            to_app="standalone",
            subject="Work Report",
            content=f"# Work Report\n\n## Summary\n{summary}",
            project_id=self.current_project
        )
        
        print(f"\n[Work report submitted to Standalone | ID: {msg_id}]")
        
    def request_fix(self, issue):
        if not self.current_project:
            print("\n[Error: No active project. Use: /use <project_id>]")
            return
        
        if self.current_app != "standalone":
            print("\n[Error: Only Standalone can request fixes]")
            return
        
        msg_id = send_message(
            msg_type="fix_request",
            from_app="standalone",
            to_app="ide",
            subject="Fix Request",
            content=f"# Fix Request\n\n## Issue\n{issue}",
            project_id=self.current_project,
            priority="high"
        )
        
        print(f"\n[Fix request sent to IDE | ID: {msg_id}]")
        
    def create_new_project(self, project_id, name, description):
        pid = create_project(project_id, name, description)
        self.current_project = pid
        print(f"\n[Project created: {name} | ID: {pid}]")
        
    def process_command(self, command):
        parts = command.strip().split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd == "/standalone":
            self.current_app = "standalone"
            print("\n[Switched to STANDALONE mode]")
            
        elif cmd == "/ide":
            self.current_app = "ide"
            print("\n[Switched to IDE mode]")
            
        elif cmd == "/messages":
            self.show_messages()
            
        elif cmd == "/read":
            if args:
                mark_as_read(args.strip())
                print(f"\n[Message {args.strip()} marked as read]")
            else:
                print("\n[Usage: /read <message_id>]")
            
        elif cmd == "/projects":
            self.show_projects()
            
        elif cmd == "/use":
            if args:
                self.current_project = args.strip()
                print(f"\n[Active project: {self.current_project}]")
            else:
                print("\n[Usage: /use <project_id>]")
            
        elif cmd == "/create":
            parts = args.split(maxsplit=2)
            if len(parts) >= 3:
                self.create_new_project(parts[0], parts[1], parts[2])
            else:
                print("\n[Usage: /create <id> <name> <description>]")
            
        elif cmd == "/status":
            self.show_status()
            
        elif cmd == "/assign":
            parts = args.split(maxsplit=1)
            if len(parts) >= 2:
                self.assign_task(parts[0], parts[1])
            else:
                print("\n[Usage: /assign <title> <description>]")
            
        elif cmd == "/report":
            if args:
                self.submit_report(args)
            else:
                print("\n[Usage: /report <summary>]")
            
        elif cmd == "/fix":
            if args:
                self.request_fix(args)
            else:
                print("\n[Usage: /fix <issue_description>]")
            
        elif cmd == "/help":
            self.show_help()
            
        elif cmd == "/quit":
            self.running = False
            print("\n[Goodbye!]")
            
        else:
            # Treat as chat message
            self.send_chat_message(command)
            
    def run(self):
        self.print_header()
        self.show_help()
        
        while self.running:
            self.print_prompt()
            try:
                user_input = input()
                if user_input.strip():
                    self.process_command(user_input)
            except KeyboardInterrupt:
                print("\n\n[Interrupted. Goodbye!]")
                break
            except EOFError:
                break


if __name__ == "__main__":
    bridge = ChatBridge()
    bridge.run()
