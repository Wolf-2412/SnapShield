import re

# Safe starter classifier. Replace/augment this with a Snapdragon-optimized
# ML model exported/compiled through the selected Qualcomm AI Hub workflow.

HIGH_RISK = [
    "credential dump", "ransomware", "reverse shell",
    "powershell encoded", "suspicious persistence", "data exfiltration"
]
MEDIUM_RISK = [
    "port scan", "failed login", "privilege escalation",
    "unusual outbound", "unknown process"
]

def classify_event(event: dict) -> dict:
    text = (event.get("message") or "").lower()

    for phrase in HIGH_RISK:
        if phrase in text:
            return {
                "risk": "high",
                "score": 0.92,
                "category": "potential_intrusion",
                "explanation": f"Matched high-risk security indicator: {phrase}",
                "action": "Isolate or investigate the affected process/session."
            }

    for phrase in MEDIUM_RISK:
        if phrase in text:
            return {
                "risk": "medium",
                "score": 0.68,
                "category": "suspicious_activity",
                "explanation": f"Matched suspicious activity indicator: {phrase}",
                "action": "Collect additional local telemetry and investigate."
            }

    # Baseline result; the trained model should replace this branch.
    return {
        "risk": "low",
        "score": 0.12,
        "category": "benign_or_unknown",
        "explanation": "No high-confidence indicator was found by the starter rules.",
        "action": "Continue monitoring."
    }
