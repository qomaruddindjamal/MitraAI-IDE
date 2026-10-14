#!/usr/bin/env python3
"""
Demo: MitraAI <-> Qoder Collaboration
Menunjukkan bagaimana Qoder dan MitraAI bekerja bersama
"""

import requests
import json
import time

MITRAAI_PROXY = "http://127.0.0.1:50999"

def check_status():
    """Cek status MitraAI proxy"""
    print("=" * 60)
    print("MITRAAI <-> QODER COLLABORATION DEMO")
    print("=" * 60)
    print()
    
    try:
        response = requests.get(f"{MITRAAI_PROXY}/health", timeout=2)
        if response.status_code == 200:
            print("[OK] MitraAI proxy: RUNNING")
        else:
            print("[ERROR] MitraAI proxy: ERROR")
            return False
    except:
        print("[ERROR] MitraAI proxy: NOT RUNNING")
        print("\nJalankan dulu:")
        print("  cd C:\\Users\\Administrator\\MitraAI-patch")
        print("  npm run proxy:start")
        return False
    
    # Load models
    try:
        with open(r"C:\Users\Administrator\.gemini\antigravity\custom_models.json", 'r', encoding='utf-8') as f:
            content = f.read()
            if content.startswith('\ufeff'):
                content = content[1:]
            data = json.loads(content)
            models = [m for m in data.get('models', []) if m.get('enabled', True)]
            
        print(f"[OK] Models available: {len(models)}")
        
        if models:
            print("\nAvailable models:")
            for i, model in enumerate(models[:5], 1):
                print(f"  {i}. {model.get('displayName')} ({model.get('provider')})")
            if len(models) > 5:
                print(f"  ... dan {len(models) - 5} model lainnya")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error loading models: {e}")
        return False


def demo_ask_model():
    """Demo: Qoder bertanya ke model MitraAI"""
    print("\n" + "=" * 60)
    print("DEMO 1: Qoder bertanya ke Model AI")
    print("=" * 60)
    print()
    
    # Load models
    with open(r"C:\Users\Administrator\.gemini\antigravity\custom_models.json", 'r', encoding='utf-8') as f:
        content = f.read()
        if content.startswith('\ufeff'):
            content = content[1:]
        data = json.loads(content)
        models = [m for m in data.get('models', []) if m.get('enabled', True)]
    
    if not models:
        print("Tidak ada model yang tersedia.")
        return
    
    # Pick first model
    model = models[0]
    model_name = model.get('name')
    display_name = model.get('displayName')
    
    print(f"Model: {display_name}")
    print(f"Question: 'Apa itu machine learning? Jelaskan dalam 2 kalimat.'")
    print()
    print("Qoder -> MitraAI ->", display_name)
    print("Waiting for response...")
    
    # Simulate asking the model
    # In real scenario, Qoder would use MCP tool: ask_model()
    print()
    print("[OK] Response received!")
    print(f"  '{display_name}' menjelaskan machine learning dengan jelas.")
    print()
    print("Qoder: 'Terima kasih! Saya akan gunakan penjelasan ini untuk")
    print("        membantu user memahami konsep ML.'")


def demo_delegate_task():
    """Demo: Qoder delegate tugas ke model terbaik"""
    print("\n" + "=" * 60)
    print("DEMO 2: Qoder Delegate Tugas")
    print("=" * 60)
    print()
    
    print("Task: 'Review kode Python ini dan berikan saran optimization'")
    print()
    print("Qoder analysis:")
    print("  - Ini tugas coding kompleks")
    print("  - Butuh model dengan reasoning kuat")
    print("  - Pilih: OpenAI GPT-4 atau Anthropic Claude")
    print()
    print("Qoder -> delegate_task(task, provider='openai')")
    print()
    print("[OK] Task delegated to GPT-4")
    print("[OK] Response received dengan 5 optimization suggestions")
    print()
    print("Qoder: 'Saya dapat 5 saran dari GPT-4. Sekarang saya akan")
    print("        verify dengan model lokal untuk quick check...'")
    print()
    print("Qoder -> ask_model('ollama-qwen', 'Verify: apakah suggestion #1 valid?')")
    print()
    print("[OK] Local model confirmed suggestion #1 is valid")
    print()
    print("Qoder: 'Great! Saya akan present semua suggestions ke user")
    print("        dengan confidence levels.'")


def demo_multi_perspective():
    """Demo: Multi-perspective problem solving"""
    print("\n" + "=" * 60)
    print("DEMO 3: Multi-Perspective Problem Solving")
    print("=" * 60)
    print()
    
    print("User question: 'Bagaimana cara improve performance aplikasi?'")
    print()
    print("Qoder: 'Pertanyaan luas, saya butuh multiple perspectives...'")
    print()
    
    perspectives = [
        ("Ollama (Local)", "Quick analysis: caching, indexing, lazy loading"),
        ("GPT-4 (Cloud)", "Deep analysis: architecture patterns, scaling strategies"),
        ("Claude (Cloud)", "Alternative view: user experience, maintainability")
    ]
    
    for i, (model, insight) in enumerate(perspectives, 1):
        print(f"{i}. Ask {model}...")
        print(f"   [OK] {insight}")
        print()
    
    print("Qoder synthesis:")
    print("  - Gabungkan semua insights")
    print("  - Identify common themes")
    print("  - Prioritize by impact & effort")
    print("  - Present comprehensive recommendation")
    print()
    print("[OK] User mendapat jawaban komprehensif dari 3 perspektif!")


def demo_collaboration_workflow():
    """Demo: Full collaboration workflow"""
    print("\n" + "=" * 60)
    print("DEMO 4: Full Collaboration Workflow")
    print("=" * 60)
    print()
    
    print("Scenario: User minta bantuan menulis dokumentasi API")
    print()
    
    steps = [
        ("User", "Request", "Buatkan dokumentasi untuk REST API ini"),
        ("Qoder", "Analysis", "Ini tugas writing + technical"),
        ("Qoder", "Action", "Create outline & structure"),
        ("Qoder", "Delegate", "Ask Claude: improve writing quality"),
        ("Claude", "Response", "Suggestions for clarity & flow"),
        ("Qoder", "Action", "Apply suggestions"),
        ("Qoder", "Verify", "Ask local model: check technical accuracy"),
        ("Ollama", "Response", "Confirmed: technical details correct"),
        ("Qoder", "Finalize", "Combine all improvements"),
        ("Qoder", "Deliver", "Present final documentation to user"),
    ]
    
    for actor, action, detail in steps:
        icon = "->" if actor == "Qoder" else "<-"
        print(f"  {icon} {actor:10} | {action:12} | {detail}")
    
    print()
    print("[OK] Dokumentasi berkualitas tinggi delivered!")
    print("[OK] User puas dengan hasil kolaborasi AI")


def main():
    """Run all demos"""
    if not check_status():
        return
    
    time.sleep(1)
    demo_ask_model()
    
    time.sleep(1)
    demo_delegate_task()
    
    time.sleep(1)
    demo_multi_perspective()
    
    time.sleep(1)
    demo_collaboration_workflow()
    
    print("\n" + "=" * 60)
    print("DEMO SELESAI!")
    print("=" * 60)
    print()
    print("Kesimpulan:")
    print("  [OK] Qoder bisa akses 37 provider AI melalui MitraAI")
    print("  [OK] Delegasi tugas ke model terbaik")
    print("  [OK] Multi-perspective problem solving")
    print("  [OK] Kolaborasi seperti tim AI yang solid")
    print()
    print("MitraAI + Qoder = Super Team!")
    print()
    print("Documentation: COLLABORATION.md")
    print("GitHub: https://github.com/qomaruddindjamal/MitraAI")
    print()


if __name__ == "__main__":
    main()
