
from core.state import DevOpsState
from tools.system_monitor import get_system_info
def collect_metrics(state: DevOpsState):

    print("\n[Node 1] Collecting system metrics...")

    metrics = get_system_info()

    print("\nRAW SYSTEM METRICS:")
    print(metrics)

    return {
        "metrics": metrics,
        "logs": ["System metrics collected."]
    }
