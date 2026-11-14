import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from core.graph import app

def run_devops_agent():
    print("========================================")
    print("  Starting DevOps AI Agent Workflow...  ")
    print("========================================")

  
    initial_state = {
        "user_request": "Run routine system health check",
        "metrics": {},
        "ai_analysis": "",
        "risk_level": "normal",
        "approval_status": "",
        "execution_result": "",
        "approval_url": "http://localhost:8000/approve",
        "reject_url": "http://localhost:8000/reject",
        "logs": []
    }

    # ২. থ্রেড আইডি কনফিগারেশন (মেমোরি ও চেকপয়েন্টারের জন্য)
    config = {
        "configurable": {
            "thread_id": "devops-monitor-001"
        }
    }

    try:
        # ৩. গ্রাফ বা ওয়ার্কফ্লো রান করা
        result = app.invoke(initial_state, config)

        print("\n========================================")
        print("         WORKFLOW COMPLETED             ")
        print("========================================")
        print(f"Final Risk Level: {result.get('risk_level')}")
        print(f"Execution Result: {result.get('execution_result', 'N/A')}")

    except Exception as e:
        print(f"\n[Error] An error occurred during workflow execution: {e}")

if __name__ == "__main__":
    run_devops_agent()