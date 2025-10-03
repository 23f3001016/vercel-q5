from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import os
import json
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI()

# Enable CORS for POST requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"] # important
)

class MetricsRequest(BaseModel):
    regions: List[str]
    threshold_ms: float

# Load telemetry bundle at startup
df = pd.read_json("telemetry.json")

@app.get("/")
def hello():
    return {"message": "Hello World"}

@app.post("/api/metrics")
async def api_metrics(req: MetricsRequest) -> Dict[str, Any]:
    result: Dict[str, Any] = {}

    for region in req.regions:
        subset = df[df["region"] == region]
        if subset.empty:
            result[region] = {
                "avg_latency": None,
                "p95_latency": None,
                "avg_uptime": None,
                "breaches": 0
            }
            continue

        avg_latency = float(subset["latency_ms"].mean())
        p95_latency = float(np.percentile(subset["latency_ms"], 95))
        avg_uptime = float(subset["uptime_pct"].mean())  # corrected column name
        breaches = int((subset["latency_ms"] > req.threshold_ms).sum())

        result[region] = {
            "avg_latency": round(avg_latency, 3),
            "p95_latency": round(p95_latency, 3),
            "avg_uptime": round(avg_uptime, 3),  # still a percentage
            "breaches": breaches
        }
    return result
