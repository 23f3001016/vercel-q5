# Vercel Q5: Telemetry API

This repository contains a simple FastAPI application designed to provide telemetry metrics for different regions.

## Purpose

The primary purpose of this application is to expose an API endpoint that calculates and returns latency and uptime metrics based on a provided telemetry data bundle.

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the application:**
    ```bash
    uvicorn api.index:app --reload
    ```
    The application will be available at `http://127.0.0.1:8000`.

## API Usage

### `POST /api/latency`

This endpoint calculates latency and uptime metrics for a specified list of regions.

**Request Body:**

```json
{
  "regions": ["iad1", "sfo1"],
  "threshold_ms": 100.5
}
```

-   `regions` (List[str]): A list of region identifiers to query.
-   `threshold_ms` (float): The latency threshold in milliseconds. Latencies above this value will be counted as "breaches".

**Response Body:**

```json
{
  "regions": {
    "iad1": {
      "avg_latency": 95.345,
      "p95_latency": 150.123,
      "avg_uptime": 99.987,
      "breaches": 5
    },
    "sfo1": {
      "avg_latency": 120.678,
      "p95_latency": 180.456,
      "avg_uptime": 99.954,
      "breaches": 12
    }
  }
}
```

The response is a JSON object where the `regions` key contains a dictionary of metrics for each requested region. Each region's metrics include:

-   `avg_latency`: Average latency in milliseconds.
-   `p95_latency`: 95th percentile latency in milliseconds.
-   `avg_uptime`: Average uptime percentage.
-   `breaches`: The number of times the latency exceeded the `threshold_ms`.

### `GET /`

A simple health check endpoint.

**Response Body:**

```json
{
  "message": "Hello World"
}
```