import math

# Network features:
# [established, listening, unique_remote_ips,
#  unique_remote_ports, https_ratio]


TRAINING_DATA = [
    # NORMAL
    ([5, 10, 3, 4, 0.80], "low"),
    ([12, 20, 6, 8, 0.75], "low"),
    ([20, 30, 10, 12, 0.85], "low"),
    ([30, 35, 15, 20, 0.80], "low"),
    ([40, 40, 18, 25, 0.82], "low"),
    ([25, 35, 12, 18, 0.90], "low"),

    # SUSPICIOUS
    ([45, 30, 25, 35, 0.45], "medium"),
    ([55, 35, 30, 45, 0.35], "medium"),
    ([35, 25, 25, 40, 0.40], "medium"),

    # HIGH RISK
    ([80, 20, 60, 100, 0.15], "high"),
    ([100, 15, 80, 150, 0.10], "high"),
    ([70, 10, 55, 90, 0.20], "high"),
]


def distance(a, b):
    return math.sqrt(
        sum((x - y) ** 2 for x, y in zip(a, b))
    )


def normalize(features):
    # Approximate feature scales.
    scales = [100, 50, 100, 150, 1]

    return [
        value / scale
        for value, scale in zip(features, scales)
    ]


def predict(features, k=3):

    normalized = normalize(features)

    neighbors = []

    for training_features, label in TRAINING_DATA:

        normalized_training = normalize(
            training_features
        )

        d = distance(
            normalized,
            normalized_training
        )

        neighbors.append((d, label))

    neighbors.sort(key=lambda x: x[0])

    nearest = neighbors[:k]

    votes = {
        "low": 0,
        "medium": 0,
        "high": 0
    }

    for _, label in nearest:
        votes[label] += 1

    prediction = max(
        votes,
        key=votes.get
    )

    confidence = votes[prediction] / k

    return prediction, confidence


def analyze_network(snapshot):

    summary = snapshot.get("summary", {})

    established = summary.get(
        "established", 0
    )

    listening = summary.get(
        "listening", 0
    )

    remote_ips = summary.get(
        "unique_remote_ips", 0
    )

    remote_ports = summary.get(
        "unique_remote_ports", 0
    )

    connections = snapshot.get(
        "connections", []
    )

    https_connections = sum(
        1
        for c in connections
        if c.get("status") == "ESTABLISHED"
        and c.get("remote_port") == 443
    )

    if established > 0:
        https_ratio = (
            https_connections / established
        )
    else:
        https_ratio = 0

    features = [
        established,
        listening,
        remote_ips,
        remote_ports,
        round(https_ratio, 3)
    ]

    risk, confidence = predict(features)

    explanations = {

        "low":
            "The observed network pattern is "
            "similar to the normal baseline.",

        "medium":
            "The network pattern contains "
            "unusual connection diversity or volume "
            "that deserves investigation.",

        "high":
            "The network pattern is substantially "
            "different from the normal baseline and "
            "may indicate suspicious activity."
    }

    actions = {

        "low":
            "Continue monitoring.",

        "medium":
            "Review unusual connections and "
            "associated processes.",

        "high":
            "Investigate affected processes and "
            "connections immediately."
    }

    return {
        "risk": risk,
        "confidence": round(confidence, 3),
        "features": {
            "established_connections": established,
            "listening_ports": listening,
            "unique_remote_ips": remote_ips,
            "unique_remote_ports": remote_ports,
            "https_ratio": round(
                https_ratio, 3
            )
        },
        "explanation": explanations[risk],
        "recommended_action": actions[risk],
        "model": "SnapShield Network KNN Classifier"
    }