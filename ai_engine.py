import json
import math
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "model.json"


def sigmoid(x):
    x = max(-60, min(60, x))
    return 1.0 / (1.0 + math.exp(-x))


def extract_features(message):
    text = message.lower()

    # [connection_frequency, unique_ports,
    #  failed_logins, encoded_command, unusual_outbound]

    frequency = 1
    ports = 0
    failed_logins = 0
    encoded_command = 0
    unusual_outbound = 0

    if "port scan" in text or "scan" in text:
        frequency = 20
        ports = 12

    if "many ports" in text:
        frequency = 25
        ports = 15

    if "failed login" in text:
        failed_logins = 2
        frequency = max(frequency, 8)

    if "powershell encoded" in text:
        encoded_command = 1
        frequency = max(frequency, 25)
        ports = max(ports, 15)

    if "encoded command" in text:
        encoded_command = 1
        frequency = max(frequency, 25)

    if "unusual outbound" in text:
        unusual_outbound = 1
        frequency = max(frequency, 15)

    if "data exfiltration" in text:
        unusual_outbound = 1
        frequency = max(frequency, 30)
        ports = max(ports, 20)

    return [
        frequency,
        ports,
        failed_logins,
        encoded_command,
        unusual_outbound
    ]


def load_model():
    with open(MODEL_PATH, "r") as f:
        return json.load(f)


MODEL = load_model()


def predict(message):
    features = extract_features(message)

    scores = {}

    for class_id, model in MODEL.items():

        score = model["bias"]

        for weight, feature in zip(
            model["weights"],
            features
        ):
            score += weight * feature

        scores[class_id] = sigmoid(score)

    # Normalize scores
    total = sum(scores.values())

    probabilities = {
        key: value / total
        for key, value in scores.items()
    }

    prediction = max(
        probabilities,
        key=probabilities.get
    )

    confidence = probabilities[prediction]

    labels = {
        "0": ("low", "benign_or_unknown"),
        "1": ("medium", "suspicious_activity"),
        "2": ("high", "potential_intrusion")
    }

    risk, category = labels[prediction]

    explanations = {
        "0": "The ML model found mostly benign security characteristics.",
        "1": "The ML model detected suspicious network or authentication characteristics.",
        "2": "The ML model detected multiple high-risk security characteristics."
    }

    actions = {
        "0": "Continue monitoring.",
        "1": "Collect additional local telemetry and investigate.",
        "2": "Isolate or investigate the affected process/session."
    }

    return {
        "risk": risk,
        "score": round(confidence, 4),
        "category": category,
        "prediction_class": int(prediction),
        "features": features,
        "explanation": explanations[prediction],
        "action": actions[prediction],
        "model": "SnapShield Lightweight Logistic Classifier"
    }