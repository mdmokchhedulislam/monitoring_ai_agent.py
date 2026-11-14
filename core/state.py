from typing_extensions import TypedDict
import operator
from typing import Annotated
class DevOpsState(TypedDict):
    user_request: str
    metrics: dict
    ai_analysis: str
    risk_level: str
    approval_status: str
    execution_result: str
    approval_url: str
    reject_url: str
    logs: Annotated[list[str], operator.add]