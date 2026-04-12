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