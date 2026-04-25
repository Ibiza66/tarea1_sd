from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import hashlib
import json
import time
from collections import OrderedDict

app = FastAPI()

CACHE = OrderedDict()
MAX_SIZE = 50
TTL = 30

metrics = {
    "hits": 0,
    "misses": 0,
    "evictions": 0,
    "latencies": []
}

RESPONSE_GENERATOR_URL = "http://response-generator:8001/query"


class QueryRequest(BaseModel):
    query_type: str
    zone_id: str | None = None
    zone_id_a: str | None = None
    zone_id_b: str | None = None
    confidence_min: float = 0.0
    bins: int = 5


def generate_cache_key(request: QueryRequest):
    request_dict = request.dict()
    request_str = json.dumps(request_dict, sort_keys=True)
    return hashlib.md5(request_str.encode()).hexdigest()


@app.post("/query")
def query(request: QueryRequest):
    start_time = time.time()

    key = generate_cache_key(request)

    if key in CACHE:
        data, timestamp = CACHE[key]

        if time.time() - timestamp < TTL:
            CACHE.move_to_end(key)
            metrics["hits"] += 1
            latency = time.time() - start_time
            metrics["latencies"].append(latency)
            return {"source": "cache", "data": data}

        else:
            del CACHE[key]

    metrics["misses"] += 1

    try:
        response = requests.post(RESPONSE_GENERATOR_URL, json=request.dict())

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()

        if len(CACHE) >= MAX_SIZE:
            CACHE.popitem(last=False)
            metrics["evictions"] += 1

        CACHE[key] = (data, time.time())

        latency = time.time() - start_time
        metrics["latencies"].append(latency)

        return {"source": "computed", "data": data}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
def get_metrics():
    total = metrics["hits"] + metrics["misses"]
    hit_rate = metrics["hits"] / total if total > 0 else 0

    latencies = metrics["latencies"]
    latencies.sort()

    def percentile(p):
        if not latencies:
            return 0
        k = int(len(latencies) * p)
        return latencies[min(k, len(latencies)-1)]

    return {
        "hits": metrics["hits"],
        "misses": metrics["misses"],
        "hit_rate": hit_rate,
        "evictions": metrics["evictions"],
        "p50_latency": percentile(0.5),
        "p95_latency": percentile(0.95),
        "cache_size": len(CACHE)
    }


@app.delete("/cache")
def clear_cache():
    CACHE.clear()
    metrics["hits"] = 0
    metrics["misses"] = 0
    metrics["evictions"] = 0
    metrics["latencies"] = []
    return {"message": "cache limpiado"}