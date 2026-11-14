
from core.state import DevOpsState
from typing import Annotated, Literal


def check_risk(
    state: DevOpsState
) -> Literal["approval", "finish"]:

    if state["risk_level"] == "critical":
        return "approval"

    return "finish"


def check_approval(
    state: DevOpsState
) -> Literal["approved", "rejected"]:

    if state["approval_status"] == "approve":
        return "approved"

    return "rejected"

