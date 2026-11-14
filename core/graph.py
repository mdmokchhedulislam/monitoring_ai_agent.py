
from nodes.metrics_collection import collect_metrics    
from nodes.analyze_with_ai import analyze_with_ai    
from nodes.evaluate_risk import evaluate_risk    
from nodes.send_approval_email import send_approval_email    
from nodes.request_approval import request_approval    
from nodes.reject_action import reject_action    
from nodes.execute_action import execute_action    

from core.state import DevOpsState

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from agent.router import check_risk, check_approval
builder = StateGraph(DevOpsState)

builder.add_node("collect_metrics", collect_metrics)
builder.add_node("analyze_with_ai", analyze_with_ai)
builder.add_node("evaluate_risk", evaluate_risk)
builder.add_node("send_approval_email", send_approval_email)
builder.add_node("request_approval", request_approval)
builder.add_node("execute_action", execute_action)
builder.add_node("reject_action", reject_action)

builder.add_edge(START, "collect_metrics")
builder.add_edge("collect_metrics", "analyze_with_ai")
builder.add_edge("analyze_with_ai", "evaluate_risk")

builder.add_conditional_edges(
    "evaluate_risk",
    check_risk,
    {
        "approval": "send_approval_email",
        "finish": END
    }
)

builder.add_edge("send_approval_email", "request_approval")

builder.add_conditional_edges(
    "request_approval",
    check_approval,
    {
        "approved": "execute_action",
        "rejected": "reject_action"
    }
)

builder.add_edge("execute_action", END)
builder.add_edge("reject_action", END)


# =====================================
# STEP 13: CHECKPOINTER
# =====================================

memory = InMemorySaver()

graph_app = builder.compile(checkpointer=memory)

