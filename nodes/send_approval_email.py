

from core.state import DevOpsState
from services.email_service import send_email
from services.email_template import create_approval_email


def send_approval_email(state: DevOpsState):

    print("\n[Node 4] Sending approval email...")

    metrics = state["metrics"]
    analysis = state["ai_analysis"]

    action = "Run approved diagnostic check"

    html_body = create_approval_email(
        metrics=metrics,
        analysis=analysis,
        action=action,
        approve_url=state["approval_url"],
        reject_url=state["reject_url"]
    )

    send_email(
        subject="CRITICAL - DevOps AI Agent Approval Required",
        body=(
            "Critical system risk detected.\n"
            "Please open this email in an HTML-capable email client "
            "to review the approval request."
        ),
        html_body=html_body
    )

    print("[Node 4] Approval email sent.")

    return {
        "logs": ["Approval email sent successfully."]
    }
