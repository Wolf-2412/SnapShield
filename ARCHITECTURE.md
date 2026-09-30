# SnapShield architecture

## 1. Data plane
Collect only the minimum local telemetry needed for detection:
- process metadata
- connection metadata
- authentication/security events
- selected system events

## 2. Pre-processing
Normalize fields, remove unnecessary identifiers, and transform events into model-ready
features or text representations.

## 3. AI inference
Run a compact threat-classification model locally. The competition implementation should
select a Qualcomm AI Hub-supported model/runtime path appropriate to the target Snapdragon HP PC.

## 4. Decision layer
Combine model confidence with deterministic security rules. This makes the prototype more
transparent and provides a fallback when model confidence is low.

## 5. Explanation
Generate a short local explanation containing:
- why the event was flagged
- confidence/risk level
- evidence
- recommended next action

## 6. UI
A lightweight dashboard should show live events, risk levels, explanations, and device-local
privacy status.

## Benchmark plan
Measure on the same test set:
- cold-start time
- average inference latency
- throughput
- CPU utilization
- NPU utilization when available
- RAM usage
- energy/battery impact
- detection precision/recall/F1

Do not publish numbers until they are measured on the target hardware.
