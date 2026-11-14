
from core.state import DevOpsState
from langgraph.types import interrupt
def request_approval(state: DevOpsState):

    print("\n[Node 5] Waiting for human approval...")

    decision = interrupt({
        "message": "Critical system risk detected!",
        "risk_level": state["risk_level"],
        "action": "Run approved diagnostic check",
        "warning": "This workflow uses dry-run only."
    })

    decision = str(decision).strip().lower()

    if decision not in ["approve", "reject"]:
        raise ValueError("Invalid approval decision.")

    print(f"Human decision received: {decision}")

    return {
        "approval_status": decision,
        "logs": [f"Human decision: {decision}"]
    }

