# \# SnapShield

# 

# \## On-Device AI Cybersecurity Assistant for Snapdragon-Powered HP PCs

# 

# SnapShield is a privacy-first cybersecurity prototype that performs

# AI-assisted security event classification and network anomaly assessment

# locally on the user's PC.

# 

# The system is designed around a future Snapdragon deployment model where

# AI inference can be optimized for Qualcomm hardware and the Snapdragon NPU.

# 

# \---

# 

# \## Problem

# 

# Traditional endpoint security systems may rely heavily on cloud-based

# analysis. This can introduce:

# 

# \- Privacy concerns

# \- Network dependency

# \- Additional latency

# \- Reduced control over local telemetry

# 

# SnapShield explores a local-first alternative.

# 

# \---

# 

# \## Solution

# 

# SnapShield continuously observes local network activity and provides

# AI-assisted security assessment.

# 

# \### Core pipeline

# 

# Windows network telemetry

# &#x20;       ↓

# Feature extraction

# &#x20;       ↓

# Local AI network assessment

# &#x20;       ↓

# Risk + confidence

# &#x20;       ↓

# Explanation + recommended action

# &#x20;       ↓

# Streamlit security dashboard

# 

# The project also supports manual security-event analysis.

# 

# \---

# 

# \## Key Features

# 

# \### 1. Local Network Monitoring

# 

# SnapShield collects network information from the local Windows system,

# including:

# 

# \- Established connections

# \- Listening ports

# \- Unique remote IP addresses

# \- Unique remote ports

# \- HTTPS connection ratio

# 

# The monitor is read-only and does not automatically block or terminate

# connections.

# 

# \### 2. AI Network Assessment

# 

# A lightweight prototype ML classifier analyzes network-level features and

# produces:

# 

# \- Risk level

# \- Confidence

# \- Explanation

# \- Recommended action

# 

# \### 3. Security Event Classification

# 

# Users can provide security events such as:

# 

# ```text

# powershell encoded command observed

