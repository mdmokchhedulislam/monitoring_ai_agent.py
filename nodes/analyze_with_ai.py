
from core.state import DevOpsState
from services.llm import llm

def analyze_with_ai(state: DevOpsState):

    print("\n[Node 2] AI analyzing system health...")

    metrics = state["metrics"]

    prompt = f"""
You are a professional DevOps engineer.

Analyze these real system metrics:

{metrics}

Explain:
1. CPU health
2. RAM health
3. Disk health
4. Potential risks
5. Recommended investigation steps

Rules:
- Use only the provided metrics.
- Never invent system information.
- Never execute any action.
- Explain in simple language.
"""

    response = llm.invoke(prompt)
    analysis = response.content

    print("\nAI ANALYSIS:")
    print(analysis)

    return {
        "ai_analysis": analysis,
        "logs": ["AI system analysis completed."]
    }

