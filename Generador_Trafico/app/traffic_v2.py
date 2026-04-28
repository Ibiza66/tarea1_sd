import requests
import random
import time
import matplotlib.pyplot as plt

CACHE_URL = "http://cache-service:8000/query"

zones = ["Z1", "Z2", "Z3", "Z4", "Z5"]
query_types = ["Q1", "Q2", "Q3", "Q4", "Q5"]

hits = 0
misses = 0

x_points = []
y_points = []


def build_query_uniform():
    qt = random.choice(query_types)

    if qt == "Q4":
        a, b = random.sample(zones, 2)
        return {
            "query_type": "Q4",
            "zone_id_a": a,
            "zone_id_b": b,
            "confidence_min": random.choice([0.0, 0.5, 0.8])
        }

    elif qt == "Q5":
        return {
            "query_type": "Q5",
            "zone_id": random.choice(zones),
            "bins": 5
        }

    else:
        return {
            "query_type": qt,
            "zone_id": random.choice(zones),
            "confidence_min": random.choice([0.0, 0.5, 0.8])
        }


def build_query_zipf():
    weights = [0.5, 0.2, 0.15, 0.1, 0.05]
    qt = random.choice(query_types)

    if qt == "Q4":
        a = random.choices(zones, weights=weights)[0]
        restantes = [z for z in zones if z != a]
        b = random.choice(restantes)
        return {
            "query_type": "Q4",
            "zone_id_a": a,
            "zone_id_b": b,
            "confidence_min": 0.0
        }

    elif qt == "Q5":
        return {
            "query_type": "Q5",
            "zone_id": random.choices(zones, weights=weights)[0],
            "bins": 5
        }

    else:
        return {
            "query_type": qt,
            "zone_id": random.choices(zones, weights=weights)[0],
            "confidence_min": 0.0
        }


def run(mode="uniform"):
    global hits, misses

    for i in range(100):
        query = build_query_zipf() if mode == "zipf" else build_query_uniform()

        try:
            r = requests.post(CACHE_URL, json=query)
            data = r.json()

            if r.status_code == 200:
                if data.get("source") == "cache":
                    hits += 1
                    y_points.append(1)
                else:
                    misses += 1
                    y_points.append(0)

                x_points.append(i)

            print(f"{i+1}/100 {r.status_code}")

        except Exception as e:
            print("error:", e)

        time.sleep(0.1)

    draw()


def draw():
    plt.figure()
    plt.scatter(x_points, y_points, alpha=0.6)
    plt.title("Cache performance (Live)")
    plt.xlabel("Request order")
    plt.ylabel("Hit / Miss")
    plt.yticks([0, 1], ["Miss", "Hit"])
    plt.savefig("/app/metrics.png")
    print("gráfico guardado en /app/metrics.png")


if __name__ == "__main__":
    run("uniform")