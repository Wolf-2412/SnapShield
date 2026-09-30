import math
import json
from pathlib import Path

# Features:
# [connection_frequency, unique_ports, failed_logins, encoded_command, unusual_outbound]

TRAINING_DATA = [
    ([1, 0, 0, 0, 0], 0),  # benign
    ([2, 0, 0, 0, 0], 0),
    ([3, 1, 0, 0, 0], 0),
    ([2, 0, 1, 0, 0], 0),

    ([15, 8, 0, 0, 1], 1), # suspicious
    ([20, 12, 2, 0, 1], 1),
    ([18, 10, 0, 0, 1], 1),

    ([25, 15, 0, 1, 1], 2), # high risk
    ([30, 20, 3, 1, 1], 2),
    ([35, 25, 1, 1, 1], 2),
]

# Convert 3 classes to three one-vs-rest classifiers.
def sigmoid(x):
    x = max(-60, min(60, x))
    return 1.0 / (1.0 + math.exp(-x))


def train_binary(data, target, epochs=3000, learning_rate=0.08):
    n = len(data[0][0])
    weights = [0.0] * n
    bias = 0.0

    for _ in range(epochs):
        grad_w = [0.0] * n
        grad_b = 0.0

        for features, label in data:
            y = 1.0 if label == target else 0.0
            score = bias + sum(w * x for w, x in zip(weights, features))
            prediction = sigmoid(score)

            error = prediction - y

            for i in range(n):
                grad_w[i] += error * features[i]

            grad_b += error

        count = len(data)

        for i in range(n):
            weights[i] -= learning_rate * grad_w[i] / count

        bias -= learning_rate * grad_b / count

    return weights, bias


models = {}

for target in [0, 1, 2]:
    weights, bias = train_binary(TRAINING_DATA, target)
    models[str(target)] = {
        "weights": weights,
        "bias": bias
    }

output = Path("model.json")

with output.open("w") as f:
    json.dump(models, f, indent=2)

print("SnapShield ML model trained successfully.")
print("Model saved to:", output.resolve())