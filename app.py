from fastapi import FastAPI
from pydantic import BaseModel

from ai_engine import predict
from network_monitor import collect_network_snapshot
from network_ai import analyze_network


app = FastAPI(
    title="SnapShield",
    version="0.4.0",
    description="On-device AI cybersecurity assistant"
)


class SecurityEvent(BaseModel):

    event_type: str

    source: str = "local"

    message: str

    features: dict = {}


@app.get("/")
def root():

    return {
        "project": "SnapShield",
        "version": "0.4.0",
        "mode": "AI threat detection",
        "inference": "local"
    }


@app.post("/analyze")
def analyze(event: SecurityEvent):

    result = predict(event.message)

    result["event_type"] = event.event_type

    result["source"] = event.source

    return result


@app.get("/network")
def network():

    return collect_network_snapshot()


@app.get("/network/analyze")
def analyze_live_network():

    snapshot = collect_network_snapshot()

    result = analyze_network(snapshot)

    return result