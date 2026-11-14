
import os
import secrets
import threading
import html

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature, SignatureExpired

from langgraph.types import Command

# Load environment variables
load_dotenv()

# Import the SAME compiled graph used by this server
from core.graph import graph_app


# =====================================
# STEP 1: CONFIGURATION
# =====================================

APPROVAL_SECRET = os.getenv("APPROVAL_SECRET")
APPROVAL_BASE_URL = os.getenv(
    "APPROVAL_BASE_URL",
    "http://127.0.0.1:8000"
).rstrip("/")

TOKEN_MAX_AGE = 900  # 15 minutes

if not APPROVAL_SECRET:
    raise RuntimeError(
        "APPROVAL_SECRET is missing from .env"
    )

serializer = URLSafeTimedSerializer(
    APPROVAL_SECRET,
    salt="devops-ai-approval"
)

app = FastAPI(
    title="DevOps AI Approval Server",
    version="1.0.0"
)


# =====================================
# STEP 2: IN-MEMORY REQUEST STORAGE
# =====================================

pending_requests = {}

request_lock = threading.Lock()


# =====================================
# STEP 3: HTML PAGE HELPER
# =====================================

def make_page(title, message):

    safe_title = html.escape(str(title))
    safe_message = html.escape(str(message))

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{safe_title}</title>
    </head>

    <body style="
        font-family: Arial;
        max-width: 600px;
        margin: 80px auto;
        padding: 25px;
        text-align: center;
        background: #f8fafc;
    ">

        <div style="
            background: white;
            padding: 30px;
            border-radius: 10px;
        ">

            <h2>{safe_title}</h2>

            <p>{safe_message}</p>

        </div>

    </body>
    </html>
    """


# =====================================
# STEP 4: VERIFY SIGNED TOKEN
# =====================================

def verify_token(token):

    try:

        payload = serializer.loads(
            token,
            max_age=TOKEN_MAX_AGE
        )

        required_keys = {
            "thread_id",
            "request_id",
            "decision"
        }

        if not required_keys.issubset(payload):
            raise HTTPException(
                status_code=400,
                detail="Invalid approval token."
            )

        if payload["decision"] not in ["approve", "reject"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid decision."
            )

        return payload

    except SignatureExpired:

        raise HTTPException(
            status_code=410,
            detail="Approval link has expired."
        )

    except BadSignature:

        raise HTTPException(
            status_code=400,
            detail="Invalid or modified approval link."
        )


# =====================================
# STEP 5: HOME PAGE
# =====================================

@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <!DOCTYPE html>
    <html>
    <body style="
        font-family: Arial;
        text-align: center;
        margin-top: 100px;
    ">

        <h1>DevOps AI Agent</h1>

        <p>Human Approval System</p>

        <form action="/run" method="post">

            <button type="submit" style="
                background: #2563eb;
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
            ">
                Start System Monitoring
            </button>

        </form>

    </body>
    </html>
    """


# =====================================
# STEP 6: START DEVOPS WORKFLOW
# =====================================

@app.post("/run", response_class=HTMLResponse)
def run_workflow():

    thread_id = secrets.token_urlsafe(18)
    request_id = secrets.token_urlsafe(18)

    approve_token = serializer.dumps({
        "thread_id": thread_id,
        "request_id": request_id,
        "decision": "approve"
    })

    reject_token = serializer.dumps({
        "thread_id": thread_id,
        "request_id": request_id,
        "decision": "reject"
    })

    approve_url = (
        f"{APPROVAL_BASE_URL}/approval/{approve_token}"
    )

    reject_url = (
        f"{APPROVAL_BASE_URL}/approval/{reject_token}"
    )

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    initial_state = {
        "user_request": "Check my system health",
        "metrics": {},
        "ai_analysis": "",
        "risk_level": "",
        "approval_status": "",
        "execution_result": "",
        "approval_url": approve_url,
        "reject_url": reject_url,
        "logs": []
    }

    with request_lock:

        pending_requests[thread_id] = {
            "request_id": request_id,
            "status": "starting"
        }

    try:

        result = graph_app.invoke(
            initial_state,
            config=config
        )

        if result.get("__interrupt__"):

            with request_lock:

                pending_requests[thread_id]["status"] = "pending"

            return HTMLResponse(
                make_page(
                    "Approval Email Sent",
                    "Critical risk detected. "
                    "Check your Gmail inbox and select "
                    "Approve or Reject."
                )
            )

        with request_lock:

            pending_requests[thread_id]["status"] = "completed"

        return HTMLResponse(
            make_page(
                "Monitoring Completed",
                result.get(
                    "execution_result",
                    "No critical risk detected."
                )
            )
        )

    except Exception as exc:

        with request_lock:

            pending_requests[thread_id]["status"] = "failed"

        print("Workflow error:", exc)

        raise HTTPException(
            status_code=500,
            detail="Workflow execution failed. Check server logs."
        )


# =====================================
# STEP 7: OPEN APPROVAL CONFIRMATION
# =====================================

@app.get(
    "/approval/{token}",
    response_class=HTMLResponse
)
def approval_confirmation(token: str):

    payload = verify_token(token)

    thread_id = payload["thread_id"]
    request_id = payload["request_id"]
    decision = payload["decision"]

    with request_lock:

        record = pending_requests.get(thread_id)

        if not record or record["request_id"] != request_id:

            raise HTTPException(
                status_code=404,
                detail="Approval request not found."
            )

        if record["status"] != "pending":

            raise HTTPException(
                status_code=409,
                detail="This approval request is no longer pending."
            )

    if decision == "approve":

        title = "Confirm Approval"
        message = (
            "You are about to APPROVE the diagnostic action. "
            "Click Confirm below to continue."
        )

        button_color = "#16a34a"
        button_text = "Confirm Approve"

    else:

        title = "Confirm Rejection"
        message = (
            "You are about to REJECT the diagnostic action. "
            "Click Confirm below to cancel it."
        )

        button_color = "#dc2626"
        button_text = "Confirm Reject"

    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <body style="
        font-family: Arial;
        max-width: 600px;
        margin: 80px auto;
        padding: 25px;
        text-align: center;
    ">

        <h2>{title}</h2>

        <p>{message}</p>

        <form
            action="/approval/{html.escape(token, quote=True)}/confirm"
            method="post"
        >

            <button type="submit" style="
                background: {button_color};
                color: white;
                padding: 14px 28px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
            ">
                {button_text}
            </button>

        </form>

        <p style="color: #888; font-size: 12px;">
            This confirmation link expires after 15 minutes.
        </p>

    </body>
    </html>
    """)


# =====================================
# STEP 8: PROCESS HUMAN DECISION
# =====================================

@app.post(
    "/approval/{token}/confirm",
    response_class=HTMLResponse
)
def confirm_approval(token: str):

    payload = verify_token(token)

    thread_id = payload["thread_id"]
    request_id = payload["request_id"]
    decision = payload["decision"]

    # Validate and consume the pending request once.
    with request_lock:

        record = pending_requests.get(thread_id)

        if not record or record["request_id"] != request_id:

            raise HTTPException(
                status_code=404,
                detail="Approval request not found."
            )

        if record["status"] != "pending":

            raise HTTPException(
                status_code=409,
                detail="Request already processed or unavailable."
            )

        record["status"] = "processing"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    try:

        print(f"\nHuman decision received: {decision}")

        # Resume the SAME paused LangGraph workflow.
        result = graph_app.invoke(
            Command(resume=decision),
            config=config
        )

        if result.get("__interrupt__"):

            raise RuntimeError(
                "Workflow is still waiting for approval."
            )

        with request_lock:

            pending_requests[thread_id]["status"] = "completed"

        final_result = result.get(
            "execution_result",
            "Workflow completed."
        )

        return HTMLResponse(
            make_page(
                f"Decision: {decision.upper()}",
                final_result
            )
        )

    except Exception as exc:

        with request_lock:

            pending_requests[thread_id]["status"] = "failed"

        print("Approval processing error:", exc)

        raise HTTPException(
            status_code=500,
            detail="Could not process approval. Check server logs."
        )
