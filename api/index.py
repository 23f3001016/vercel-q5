from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import os
import json

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

# Load telemetry bundle at startup
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "telemetry.csv")
df = pd.read_csv(DATA_PATH)

@app.post("/")
async def check_latency(request: Request):
    body = await request.json()
    regions = body.get("regions", [])
    threshold = body.get("threshold_ms", 999999)

    result = {}

    for region in regions:
        subset = df[df["region"] == region]
        if subset.empty:
            continue

        avg_latency = float(subset["latency_ms"].mean())
        p95_latency = float(np.percentile(subset["latency_ms"], 95))
        avg_uptime = float(subset["uptime"].mean())
        breaches = int((subset["latency_ms"] > threshold).sum())

        result[region] = {
            "avg_latency": round(avg_latency, 3),
            "p95_latency": round(p95_latency, 3),
            "avg_uptime": round(avg_uptime, 5),
            "breaches": breaches
        }

    return result
