from .zones import ZONES


def q1_count(data, zone_id, confidence_min=0.0):
    if zone_id not in data:
        raise ValueError(f"Zona inválida: {zone_id}")

    filtered = [
        b for b in data[zone_id]
        if b["confidence"] >= confidence_min
    ]

    return {
        "zone_id": zone_id,
        "confidence_min": confidence_min,
        "count": len(filtered),
        "cache_key": f"count:{zone_id}:conf={confidence_min}"
    }


def q2_area_stats(data, zone_id, confidence_min=0.0):
    if zone_id not in data:
        raise ValueError(f"Zona inválida: {zone_id}")

    filtered = [
        b for b in data[zone_id]
        if b["confidence"] >= confidence_min
    ]

    count = len(filtered)
    total_area = sum(b["area_in_meters"] for b in filtered)
    avg_area = total_area / count if count > 0 else 0.0

    return {
        "zone_id": zone_id,
        "confidence_min": confidence_min,
        "count": count,
        "total_area": round(total_area, 2),
        "avg_area": round(avg_area, 2),
        "cache_key": f"area:{zone_id}:conf={confidence_min}"
    }


def q3_density(data, zone_id, confidence_min=0.0):
    if zone_id not in data:
        raise ValueError(f"Zona inválida: {zone_id}")

    filtered = [
        b for b in data[zone_id]
        if b["confidence"] >= confidence_min
    ]

    count = len(filtered)
    area_km2 = ZONES[zone_id]["area_km2"]
    density = count / area_km2 if area_km2 > 0 else 0.0

    return {
        "zone_id": zone_id,
        "confidence_min": confidence_min,
        "count": count,
        "area_km2": area_km2,
        "density_per_km2": round(density, 4),
        "cache_key": f"density:{zone_id}:conf={confidence_min}"
    }


def q4_compare_density(data, zone_id_a, zone_id_b, confidence_min=0.0):
    if zone_id_a not in data:
        raise ValueError(f"Zona inválida: {zone_id_a}")
    if zone_id_b not in data:
        raise ValueError(f"Zona inválida: {zone_id_b}")

    da = q3_density(data, zone_id_a, confidence_min)
    db = q3_density(data, zone_id_b, confidence_min)

    density_a = da["density_per_km2"]
    density_b = db["density_per_km2"]

    if density_a > density_b:
        winner = zone_id_a
    elif density_b > density_a:
        winner = zone_id_b
    else:
        winner = "tie"

    return {
        "zone_id_a": zone_id_a,
        "zone_id_b": zone_id_b,
        "confidence_min": confidence_min,
        "density_a": density_a,
        "density_b": density_b,
        "winner": winner,
        "cache_key": f"compare:density:{zone_id_a}:{zone_id_b}:conf={confidence_min}"
    }


def q5_confidence_dist(data, zone_id, bins=5):
    if zone_id not in data:
        raise ValueError(f"Zona inválida: {zone_id}")
    if bins <= 0:
        raise ValueError("bins debe ser mayor que 0")

    scores = [b["confidence"] for b in data[zone_id]]

    step = 1.0 / bins
    distribution = []

    for i in range(bins):
        min_edge = round(i * step, 4)
        max_edge = round((i + 1) * step, 4)

        if i < bins - 1:
            count = sum(1 for s in scores if min_edge <= s < max_edge)
        else:
            count = sum(1 for s in scores if min_edge <= s <= 1.0)

        distribution.append({
            "bucket": i,
            "min": min_edge,
            "max": max_edge,
            "count": count
        })

    return {
        "zone_id": zone_id,
        "bins": bins,
        "total_records": len(scores),
        "distribution": distribution,
        "cache_key": f"confidence_dist:{zone_id}:bins={bins}"
    }