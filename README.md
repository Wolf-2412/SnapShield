# \# 🛡️ SnapShield

# 

# \## On-Device AI Cybersecurity Assistant

# 

# \*\*Privacy-first security monitoring with lightweight local AI and a Snapdragon deployment target.\*\*

# 

# SnapShield is a cybersecurity prototype that performs AI-assisted security analysis directly on a Windows endpoint.

# 

# It monitors local network activity, extracts behavioral features, analyzes security events using lightweight machine-learning models, and presents the results through an interactive dashboard.

# 

# The architecture is designed with a future deployment path toward \*\*Snapdragon-powered HP PCs\*\* and Qualcomm's supported AI deployment ecosystem.

# 

# \---

# 

# \## 🎯 Problem

# 

# Modern computers continuously generate security-relevant activity such as:

# 

# \- Network connections

# \- Listening ports

# \- Remote endpoints

# \- Suspicious processes

# \- Authentication events

# \- System activity

# 

# Security analysis can rely heavily on centralized or cloud-based processing. This can introduce privacy concerns, network dependency, and additional latency.

# 

# SnapShield explores a local-first approach:

# 

# > \*\*Bring lightweight security intelligence closer to the endpoint.\*\*

# 

# \---

# 

# \## 💡 Solution

# 

# SnapShield combines:

# 

# \- Local network telemetry

# \- Lightweight machine learning

# \- Security-event classification

# \- Network behavior assessment

# \- Explainable results

# \- Recommended security actions

# \- Interactive visualization

# 

# The system processes the prototype's security telemetry locally instead of intentionally sending it to a cloud security-analysis service.

# 

# \---

# 

# \## ✨ Key Features

# 

# \### 🌐 Live Network Monitoring

# 

# SnapShield observes local network activity using `psutil`.

# 

# It tracks:

# 

# \- Total connections

# \- Established connections

# \- Listening ports

# \- Unique remote IP addresses

# \- Unique remote ports

# \- HTTPS connection ratio

# 

# The network monitor is read-only and does not automatically terminate connections.

# 

# \### 🧠 AI Network Assessment

# 

# A lightweight network classifier analyzes current network behavior.

# 

# The result contains:

# 

# \- Risk level

# \- Confidence

# \- Network features

# \- Explanation

# \- Recommended action

# \- Model information

# 

# \### 🔍 Security Event Analysis

# 

# SnapShield can analyze manually entered security events.

# 

# Example:

# 

# ```text

# powershell encoded command observed

