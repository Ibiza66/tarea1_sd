from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .loader import load_data
from .queries import q1_count, q2_area_stats, q3_density, q4_compare_density, q5_confidence_dist

app = FastAPI()

DATA = load_data()


class Q1Request(BaseModel):
    zone_id: str
    confidence_min: float = 0.0


class Q2Request(BaseModel):
    zone_id: str
    confidence_min: float = 0.0


class Q3Request(BaseModel):
    zone_id: str
    confidence_min: float = 0.0


class Q4Request(BaseModel):
    zone_id_a: str
    zone_id_b: str
    confidence_min: float = 0.0


class Q5Request(BaseModel):
    zone_id: str
    bins: int = 5


@app.get("/")
def root():
    return {"message": "Response Generator activo"}


@app.get("/health")
def health():
    return {"status": "ok", "zones_loaded": list(DATA.keys())}


@app.post("/q1")
def run_q1(request: Q1Request):
    try:
        return q1_count(DATA, request.zone_id, request.confidence_min)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/q2")
def run_q2(request: Q2Request):
    try:
        return q2_area_stats(DATA, request.zone_id, request.confidence_min)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/q3")
def run_q3(request: Q3Request):
    try:
        return q3_density(DATA, request.zone_id, request.confidence_min)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/q4")
def run_q4(request: Q4Request):
    try:
        return q4_compare_density(
            DATA,
            request.zone_id_a,
            request.zone_id_b,
            request.confidence_min
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/q5")
def run_q5(request: Q5Request):
    try:
        return q5_confidence_dist(DATA, request.zone_id, request.bins)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))