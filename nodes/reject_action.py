
from core.state import DevOpsState
def reject_action(state: DevOpsState):

    print("\n[Node 7] Action rejected.")

    return {
        "execution_result": "Action rejected. Nothing was executed.",
        "logs": ["Action rejected by human."]
    }
