import sys
sys.path.insert(0, 'e:/Keffi Ai/Platform/Backend')
from clinical_router import rule_based_route

def run_qa_diagnostics():
    """Executes automated clinical decision tree diagnostics across key scenarios."""
    tests = [
        ('Somatic Panic', "My hands are trembling and my chest feels so tight I can't take a full breath."),
        ('DBT Distress', "My friend betrayed my trust today. I am furious and want to smash my screen."),
        ('ACT Acceptance', "I got diagnosed with a chronic illness. I'll be in pain for the rest of my life."),
        ('Rogerian Support', "I'm just so exhausted with everything today. I just need someone to hear me out."),
    ]
    results = []
    for name, msg in tests:
        res = rule_based_route(msg, 'sadness')
        results.append({
            "scenario": name,
            "message": msg,
            "clinical_state": res['state_name'],
            "category": res['category'],
            "is_sos": res['is_sos'],
            "insight": res['clinical_insight']
        })
    return {"status": "QA Diagnostics Complete", "test_count": len(results), "results": results}

if __name__ == "__main__":
    print(run_qa_diagnostics())
