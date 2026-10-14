#!/usr/bin/env python3
"""
Demo: Antigravity Standalone <-> IDE Collaboration
Menunjukkan workflow kolaborasi seperti rekan kerja.

Scenario:
1. Standalone melakukan R&D untuk fitur baru
2. Standalone assign task ke IDE
3. IDE mengerjakan dan submit report
4. Standalone review dan minta fix
5. IDE fix dan submit ulang
6. Standalone approve
"""

import sys
import os
import time
import json

# Add MCP directory to path
sys.path.insert(0, r"C:\Users\Administrator\.gemini\antigravity\mcp\collaboration")
from collaboration_bridge import (
    send_message,
    get_messages,
    create_project,
    get_workflow_status,
    WORKSPACE_DIR
)


def print_header(text):
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70 + "\n")


def print_section(text):
    print(f"\n{'-' * 70}")
    print(f"  {text}")
    print(f"{'-' * 70}\n")


def demo_workflow():
    """Demo full workflow kolaborasi"""
    
    print_header("ANTIGRAVITY COLLABORATION DEMO")
    print("Scenario: Membuat fitur User Authentication untuk Project 'WebApp'")
    print()
    print("Workspace:", WORKSPACE_DIR)
    
    # Step 1: Create Project
    print_section("STEP 1: Standalone membuat project baru")
    
    project_id = create_project(
        project_id="webapp-2026",
        name="WebApp Project",
        description="Aplikasi web dengan user authentication dan dashboard"
    )
    print(f"[OK] Project created: {project_id}")
    print(f"     Name: WebApp Project")
    print(f"     Description: Aplikasi web dengan user authentication dan dashboard")
    
    time.sleep(1)
    
    # Step 2: Standalone melakukan R&D
    print_section("STEP 2: Standalone melakukan R&D")
    
    print("Standalone (Research & Analysis):")
    print("  -> Menganalisis kebutuhan authentication")
    print("  -> Research best practices (JWT, OAuth, dll)")
    print("  -> Membuat spesifikasi teknis")
    print("  -> Menentukan tech stack")
    print()
    print("[OK] R&D selesai, siap assign task ke IDE")
    
    time.sleep(1)
    
    # Step 3: Standalone assign task ke IDE
    print_section("STEP 3: Standalone assign task ke IDE")
    
    msg_id = send_message(
        msg_type="task_assignment",
        from_app="standalone",
        to_app="ide",
        subject="Task: Implement User Authentication",
        content="""
# Task Assignment

**Judul**: Implement User Authentication System

**Deskripsi**:
Buat sistem authentication untuk WebApp dengan fitur:
- User registration dengan email verification
- Login dengan JWT token
- Password reset via email
- Session management
- Role-based access control (admin, user)

**Tech Stack**:
- Backend: Node.js + Express
- Database: PostgreSQL
- Auth: JWT + bcrypt
- Email: SendGrid

**Acceptance Criteria**:
- User bisa register dan verify email
- User bisa login dan dapat JWT token
- Token valid untuk 24 jam
- Password reset berfungsi
- Admin dan user punya akses berbeda
- Semua API ada test coverage 80%+

**Prioritas**: High

---
Tolong kerjakan task ini sesuai spesifikasi.
Estimasi: 3-4 hari kerja.
        """.strip(),
        project_id=project_id,
        priority="high"
    )
    
    print(f"[OK] Task assigned ke IDE")
    print(f"     Message ID: {msg_id}")
    print(f"     Subject: Implement User Authentication")
    print(f"     Priority: High")
    
    time.sleep(1)
    
    # Step 4: IDE mengerjakan
    print_section("STEP 4: IDE mengerjakan task")
    
    print("IDE (Implementation):")
    print("  -> Setup project structure")
    print("  -> Implement user model & database schema")
    print("  -> Create registration API")
    print("  -> Create login API dengan JWT")
    print("  -> Implement password reset")
    print("  -> Add role-based access control")
    print("  -> Write unit tests")
    print("  -> Write integration tests")
    print()
    print("[OK] Implementation selesai (3 hari)")
    print("[OK] Test coverage: 85%")
    
    time.sleep(1)
    
    # Step 5: IDE submit work report
    print_section("STEP 5: IDE submit work report ke Standalone")
    
    msg_id = send_message(
        msg_type="work_report",
        from_app="ide",
        to_app="standalone",
        subject="Work Report: User Authentication",
        content="""
# Work Report

**Task ID**: auth-001

## Ringkasan
User Authentication System sudah selesai diimplementasikan dengan semua fitur yang diminta.

## Detail Implementasi

### 1. User Model
- Schema: id, email, password_hash, role, verified, created_at
- Password di-hash dengan bcrypt (10 rounds)
- Email verification token generated

### 2. APIs Implemented
- POST /api/auth/register - Register user baru
- POST /api/auth/login - Login, return JWT token
- POST /api/auth/verify-email - Verify email dengan token
- POST /api/auth/forgot-password - Request password reset
- POST /api/auth/reset-password - Reset password dengan token
- GET /api/auth/me - Get current user info
- PUT /api/auth/change-password - Change password

### 3. Security Features
- JWT token dengan expiry 24 jam
- Password hashing dengan bcrypt
- Email verification required
- Rate limiting pada login (5 attempts/15min)
- CORS configured
- Input validation dengan Joi

### 4. Role-Based Access
- Middleware: requireAuth, requireRole
- Roles: admin, user
- Admin bisa akses semua endpoints
- User hanya bisa akses own data

## Files Changed
- src/models/User.js
- src/controllers/authController.js
- src/routes/auth.js
- src/middleware/auth.js
- src/utils/jwt.js
- src/utils/email.js
- tests/auth.test.js

## Issues Found
None - semua berjalan smooth

## Suggestions
- Tambahkan 2FA untuk security tambahan
- Implement refresh token untuk better UX
- Add audit log untuk security events

---
Pekerjaan selesai, test coverage 85%.
Mohon review dan testing.
        """.strip(),
        project_id=project_id,
        task_id="auth-001"
    )
    
    print(f"[OK] Work report submitted ke Standalone")
    print(f"     Message ID: {msg_id}")
    print(f"     Test coverage: 85%")
    print(f"     Files changed: 7 files")
    
    time.sleep(1)
    
    # Step 6: Standalone review
    print_section("STEP 6: Standalone review hasil pekerjaan")
    
    print("Standalone (Review & Analysis):")
    print("  -> Review code quality")
    print("  -> Test semua endpoints")
    print("  -> Check security best practices")
    print("  -> Verify acceptance criteria")
    print()
    print("Issues ditemukan:")
    print("  [!] Bug: Password reset token tidak expire setelah digunakan")
    print("  [!] Missing: Rate limiting pada forgot-password endpoint")
    print("  [!] Suggestion: Tambahkan logging untuk security events")
    print()
    print("[OK] Review selesai, perlu fix 2 issues")
    
    time.sleep(1)
    
    # Step 7: Standalone request fix
    print_section("STEP 7: Standalone request fix ke IDE")
    
    msg_id = send_message(
        msg_type="fix_request",
        from_app="standalone",
        to_app="ide",
        subject="Fix Request: Security Issues",
        content="""
# Fix Request

**Task ID**: auth-001

## Issue Description
Ditemukan 2 security issues dan 1 suggestion pada implementasi authentication.

## Issue #1: Password Reset Token Reuse
**Expected**: Token hanya bisa digunakan sekali, setelah itu invalid
**Actual**: Token bisa digunakan berkali-kali

**Steps to Reproduce**:
1. Request password reset
2. Use token to reset password
3. Use same token again -> still works (should be invalid)

## Issue #2: Missing Rate Limiting
**Expected**: forgot-password endpoint punya rate limiting
**Actual**: Tidak ada rate limiting, bisa spam email user

## Suggestion: Add Security Logging
**Expected**: Log semua authentication events (login, failed login, password change)
**Actual**: Tidak ada logging

---
Tolong perbaiki 2 issues dan implement suggestion.
Prioritas: High (security issues)
        """.strip(),
        project_id=project_id,
        task_id="auth-001",
        priority="high"
    )
    
    print(f"[OK] Fix request dikirim ke IDE")
    print(f"     Message ID: {msg_id}")
    print(f"     Issues: 2 security issues + 1 suggestion")
    print(f"     Priority: High")
    
    time.sleep(1)
    
    # Step 8: IDE fix issues
    print_section("STEP 8: IDE fix issues")
    
    print("IDE (Fixing Issues):")
    print("  -> Fix #1: Invalidate token setelah digunakan")
    print("     - Add 'used' field ke token schema")
    print("     - Check token validity sebelum reset")
    print("     - Mark token as used setelah reset")
    print()
    print("  -> Fix #2: Add rate limiting")
    print("     - Install express-rate-limit")
    print("     - Apply to forgot-password: 3 requests/hour")
    print("     - Apply to login: 5 attempts/15min")
    print()
    print("  -> Suggestion: Add security logging")
    print("     - Create logger utility")
    print("     - Log: login success/fail, password change, token use")
    print("     - Include: timestamp, IP, user ID, action")
    print()
    print("[OK] All issues fixed")
    print("[OK] Test coverage: 88% (increased)")
    
    time.sleep(1)
    
    # Step 9: IDE submit updated report
    print_section("STEP 9: IDE submit updated work report")
    
    msg_id = send_message(
        msg_type="work_report",
        from_app="ide",
        to_app="standalone",
        subject="Work Report: Security Fixes Applied",
        content="""
# Work Report (Updated)

**Task ID**: auth-001

## Ringkasan
Semua security issues sudah diperbaiki dan suggestion sudah diimplementasi.

## Fixes Applied

### Fix #1: Password Reset Token Reuse
- Added 'used' boolean field ke token schema
- Token di-mark as used setelah reset
- Check token validity: if used, return error
- Added test case untuk token reuse

### Fix #2: Rate Limiting
- Installed express-rate-limit
- forgot-password: 3 requests per hour per IP
- login: 5 attempts per 15 minutes per IP
- Added appropriate error messages
- Added test cases untuk rate limiting

### Suggestion: Security Logging
- Created src/utils/logger.js
- Log events:
  * LOGIN_SUCCESS
  * LOGIN_FAILED
  * PASSWORD_CHANGED
  * PASSWORD_RESET_REQUESTED
  * TOKEN_USED
- Log format: {timestamp, level, event, userId, ip, details}
- Logs saved ke logs/security.log

## Files Changed (Additional)
- src/models/ResetToken.js (added 'used' field)
- src/controllers/authController.js (added logging)
- src/middleware/rateLimit.js (new file)
- src/utils/logger.js (new file)
- tests/security.test.js (new test cases)

## Test Coverage
- Before: 85%
- After: 88%
- New tests: 12 test cases

## Security Improvements
- Token reuse prevented
- Rate limiting active
- Security events logged
- Audit trail available

---
All issues fixed, security improved.
Test coverage increased to 88%.
Ready for final review.
        """.strip(),
        project_id=project_id,
        task_id="auth-001"
    )
    
    print(f"[OK] Updated work report submitted")
    print(f"     Message ID: {msg_id}")
    print(f"     Test coverage: 85% -> 88%")
    print(f"     Security: Improved")
    
    time.sleep(1)
    
    # Step 10: Standalone final review
    print_section("STEP 10: Standalone final review & approval")
    
    print("Standalone (Final Review):")
    print("  -> Test password reset token reuse -> FIXED")
    print("  -> Test rate limiting -> WORKING")
    print("  -> Check security logs -> LOGGING ACTIVE")
    print("  -> Verify all acceptance criteria -> PASSED")
    print("  -> Run full test suite -> 88% coverage")
    print()
    print("[OK] All issues resolved")
    print("[OK] Security standards met")
    print("[OK] Test coverage acceptable")
    print()
    print("=== APPROVED ===")
    print("User Authentication System siap untuk deployment!")
    
    time.sleep(1)
    
    # Final summary
    print_section("WORKFLOW SUMMARY")
    
    status = get_workflow_status(project_id)
    
    print(f"Project: {status.get('project_name')}")
    print(f"Status: {status.get('status')}")
    print()
    print("Communication:")
    print(f"  - Task assignments: {status.get('task_assignments')}")
    print(f"  - Work reports: {status.get('work_reports')}")
    print(f"  - Fix requests: {status.get('fix_requests')}")
    print(f"  - Total messages: {status.get('total_messages')}")
    print()
    print("Timeline:")
    print("  Day 1: R&D + Task Assignment")
    print("  Day 2-4: Implementation")
    print("  Day 5: Review & Fix Request")
    print("  Day 6: Fixes Applied")
    print("  Day 7: Final Review & Approval")
    print()
    print("[OK] Project completed successfully!")
    print("[OK] Standalone dan IDE bekerja sama seperti tim yang solid!")
    
    print_header("DEMO SELESAI")
    print("Antigravity Standalone dan IDE sudah berkolaborasi seperti rekan kerja!")
    print()
    print("Key Takeaways:")
    print("  1. Standalone fokus pada R&D dan analysis")
    print("  2. IDE fokus pada implementation")
    print("  3. Komunikasi terstruktur via messages")
    print("  4. Review dan feedback loop bekerja dengan baik")
    print("  5. Hasil akhir: High quality code dengan security best practices")
    print()


if __name__ == "__main__":
    demo_workflow()
