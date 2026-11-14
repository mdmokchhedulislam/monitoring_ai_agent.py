

from core.state import DevOpsState

def evaluate_risk(state: DevOpsState):

    print("\n[Node 3] Evaluating system risk...")

    metrics = state["metrics"]

    cpu = metrics["cpu_usage"]
    ram = metrics["memory"]["usage_percent"]
    disk = metrics["disk"]["usage_percent"]

    if disk > 90 or ram > 90 or cpu > 90:
        risk = "critical"

    elif disk > 80 or ram > 80 or cpu > 80:
        risk = "warning"

    else:
        risk = "normal"

    print(f"Risk Level: {risk}")

    return {
        "risk_level": risk,
        "logs": [f"Risk evaluated: {risk}"]
    }

