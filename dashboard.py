import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

API_URL = "http://127.0.0.1:8000"

# Refresh dashboard every 5 seconds
st_autorefresh(
    interval=5000,
    key="snapshield_refresh"
)

st.set_page_config(
    page_title="SnapShield",
    page_icon="S",
    layout="wide"
)

# =========================================================
# Styling
# =========================================================

st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
}

.subtitle {
    color: #888;
    font-size: 17px;
}

.section-note {
    color: #888;
    font-size: 13px;
}

.metric-card {
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# Header
# =========================================================

st.markdown(
    '<div class="main-title">SnapShield</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'On-Device AI Cybersecurity Assistant'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    "Privacy-first security monitoring with local AI-assisted threat assessment."
)

st.divider()


# =========================================================
# Backend Check
# =========================================================

try:
    network_response = requests.get(
        f"{API_URL}/network",
        timeout=3
    )

    backend_online = network_response.status_code == 200

except Exception:
    backend_online = False


c1, c2, c3 = st.columns(3)

with c1:
    if backend_online:
        st.success("BACKEND ONLINE")
    else:
        st.error("BACKEND OFFLINE")

with c2:
    st.success("LOCAL AI ACTIVE")

with c3:
    st.info("SNAPDRAGON TARGET")


# =========================================================
# Live AI Network Assessment
# =========================================================

st.header("Live AI Network Assessment")

st.caption(
    "AI-assisted assessment of the current local network activity."
)

if backend_online:

    try:
        ai_response = requests.get(
            f"{API_URL}/network/analyze",
            timeout=5
        )

        if ai_response.status_code == 200:

            ai = ai_response.json()

            risk = ai["risk"]
            confidence = ai["confidence"]

            if risk == "high":
                st.error(
                    f"HIGH RISK - {confidence:.1%} confidence"
                )

            elif risk == "medium":
                st.warning(
                    f"MEDIUM RISK - {confidence:.1%} confidence"
                )

            else:
                st.success(
                    f"LOW RISK - {confidence:.1%} confidence"
                )

            features = ai["features"]

            f1, f2, f3, f4, f5 = st.columns(5)

            f1.metric(
                "Established",
                features["established_connections"]
            )

            f2.metric(
                "Listening",
                features["listening_ports"]
            )

            f3.metric(
                "Remote IPs",
                features["unique_remote_ips"]
            )

            f4.metric(
                "Remote Ports",
                features["unique_remote_ports"]
            )

            f5.metric(
                "HTTPS Ratio",
                f"{features['https_ratio']:.0%}"
            )

            st.info(
                "AI Explanation: " + ai["explanation"]
            )

            st.warning(
                "Recommended Action: "
                + ai["recommended_action"]
            )

            st.caption(
                "Model: " + ai["model"]
            )

        else:
            st.error(
                "Unable to obtain AI network assessment."
            )

    except Exception as e:
        st.error(
            f"AI analysis error: {e}"
        )

else:
    st.warning(
        "Start the FastAPI backend first."
    )


st.divider()


# =========================================================
# Prototype Performance
# =========================================================

st.header("Prototype AI Performance")

st.caption(
    "Measured locally on the development PC. These are CPU prototype "
    "measurements and are NOT Snapdragon NPU benchmarks."
)

b1, b2, b3, b4 = st.columns(4)

b1.metric(
    "Event AI Avg",
    "0.0056 ms"
)

b2.metric(
    "Network AI Avg",
    "0.0338 ms"
)

b3.metric(
    "Event AI Runs",
    "100"
)

b4.metric(
    "Network AI Runs",
    "50"
)

st.caption(
    "Event AI: median 0.0048 ms | Network AI: median 0.0295 ms | "
    "Measurements obtained using Python perf_counter()."
)


st.divider()


# =========================================================
# Snapdragon Deployment Target
# =========================================================

st.header("Snapdragon Deployment Target")

st.markdown("""
**Target architecture**

`SnapShield AI Model`
→ `Qualcomm AI Hub / supported model deployment path`
→ `Qualcomm runtime`
→ `Snapdragon NPU`
→ `HP Snapdragon-powered PC`
""")

st.info(
    "The current prototype is validated on a Windows development PC. "
    "Snapdragon NPU execution and Qualcomm AI Hub deployment are the "
    "target optimization path and require validation on compatible "
    "Snapdragon-powered HP hardware."
)


st.divider()


# =========================================================
# Network Monitor
# =========================================================

st.header("Network Monitor")

if backend_online:

    data = network_response.json()

    summary = data.get("summary", {})

    total = summary.get("total_connections", 0)
    established = summary.get("established", 0)
    listening = summary.get("listening", 0)
    remote_ips = summary.get("unique_remote_ips", 0)
    remote_ports = summary.get("unique_remote_ports", 0)

    m1, m2, m3, m4, m5 = st.columns(5)

    m1.metric("Total Connections", total)
    m2.metric("Established", established)
    m3.metric("Listening", listening)
    m4.metric("Remote IPs", remote_ips)
    m5.metric("Remote Ports", remote_ports)

    st.divider()

    connections = data.get("connections", [])

    # -----------------------------------------------------
    # Established Connections
    # -----------------------------------------------------

    st.subheader("Established Connections")

    established_connections = [
        c for c in connections
        if c.get("status") == "ESTABLISHED"
    ]

    if established_connections:

        for c in established_connections[:15]:

            st.write(
                f"**{c.get('local_ip')}:{c.get('local_port')}**"
                f" -> "
                f"**{c.get('remote_ip')}:{c.get('remote_port')}**"
                f" | PID: {c.get('pid')}"
            )

    else:
        st.info("No established connections.")


    # -----------------------------------------------------
    # Listening Ports
    # -----------------------------------------------------

    st.subheader("Listening Ports")

    listening_connections = [
        c for c in connections
        if c.get("status") == "LISTEN"
    ]

    ports_seen = set()

    for c in listening_connections:

        port = c.get("local_port")

        if port in ports_seen:
            continue

        ports_seen.add(port)

        st.write(
            f"**Port {port}**"
            f" | {c.get('local_ip')}"
            f" | PID {c.get('pid')}"
        )

else:
    st.info("Network monitor unavailable.")


st.divider()


# =========================================================
# Manual AI Event Analysis
# =========================================================

st.header("Manual AI Event Analysis")

st.caption(
    "Test SnapShield's local security-event classifier."
)

event_type = st.selectbox(
    "Event Type",
    [
        "network",
        "process",
        "login",
        "system"
    ]
)

message = st.text_input(
    "Security Event",
    placeholder="Example: powershell encoded command observed"
)

if st.button(
    "Analyze Event",
    use_container_width=True
):

    if not message.strip():

        st.warning(
            "Enter a security event."
        )

    else:

        try:

            result = requests.post(
                f"{API_URL}/analyze",
                json={
                    "event_type": event_type,
                    "source": "local",
                    "message": message
                },
                timeout=5
            )

            if result.status_code == 200:

                analysis = result.json()

                risk = analysis["risk"]

                if risk == "high":

                    st.error(
                        f"HIGH - {analysis['score']:.2%}"
                    )

                elif risk == "medium":

                    st.warning(
                        f"MEDIUM - {analysis['score']:.2%}"
                    )

                else:

                    st.success(
                        f"LOW - {analysis['score']:.2%}"
                    )

                a1, a2 = st.columns(2)

                with a1:

                    st.write("**Threat Category**")

                    st.write(
                        analysis["category"]
                        .replace("_", " ")
                        .title()
                    )

                    st.write("**Model**")

                    st.write(
                        analysis["model"]
                    )

                with a2:

                    st.write("**Extracted Features**")

                    st.write(
                        analysis["features"]
                    )

                st.info(
                    "AI Explanation: "
                    + analysis["explanation"]
                )

                st.warning(
                    "Recommended Action: "
                    + analysis["action"]
                )

            else:

                st.error(
                    "AI analysis request failed."
                )

        except Exception as e:

            st.error(
                f"Backend error: {e}"
            )


# =========================================================
# Footer
# =========================================================

st.divider()

st.caption(
    "SnapShield | Local-first AI cybersecurity prototype | "
    "Snapdragon optimization target"
)