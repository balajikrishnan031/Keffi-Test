import os

def run_backend_cleanup():
    BASE = r"e:\Keffi Ai\Platform\Backend"
    to_delete = [
        "quick_validate_router.py",
        "comprehensive_stress_test_pro.py",
        "comprehensive_stress_test.py",
        "compare_metrics.py",
        "evaluate_chat_metrics.py",
        "evaluate_metrics.py",
        "test_live_chat.py",
        "check_n8n_db.py",
        "fix_db.py",
        "fix_patient_alert_webhook.py",
        "gemini_engine.py",
        "migrate_v3.py",
        "reset_db.py",
        "clinical_data.db",
        "ai_orchestrator.py",
    ]
    deleted_files = []
    for f in to_delete:
        path = os.path.join(BASE, f)
        if os.path.exists(path):
            try:
                os.remove(path)
                deleted_files.append(f)
            except:
                pass
    return {"status": "Cleanup Complete", "deleted_files": deleted_files}

if __name__ == "__main__":
    print(run_backend_cleanup())
