import requests
import random
import time
import matplotlib.pyplot as plt

CACHE_URL = "http://cache-service:8000/query"

zones = ["Z1", "Z2", "Z3", "Z4", "Z5"]
query_types = ["Q1", "Q2", "Q3", "Q4", "Q5"]

#  contadores
hits = 0
misses = 0


def generate_uniform():
    return {
        "query_type": random.choice(query_types),
        "zone_id": random.choice(zones),
        "confidence_min": random.choice([0.0, 0.5, 0.8]),
        "bins": 5
    }


def generate_zipf():
    weights = [0.5, 0.2, 0.15, 0.1, 0.05]
    zone = random.choices(zones, weights=weights)[0]

    return {
        "query_type": random.choice(query_types),
        "zone_id": zone,
        "confidence_min": 0.0,
        "bins": 5
    }


def run(mode="uniform"):
    global hits, misses

    for _ in range(100):

        if mode == "zipf":
            query = generate_zipf()
        else:
            query = generate_uniform()

        try:
            r = requests.post(CACHE_URL, json=query)
            data = r.json()

            print(data)

            #  contar hits/miss
            if data["source"] == "cache":
                hits += 1
            else:
                misses += 1

        except:
            print("error")

        time.sleep(0.1)

    print("\nConsultas terminadas")
    print("Hits:", hits)
    print("Misses:", misses)

    draw_graph()


def draw_graph():
    labels = ["Hits", "Misses"]
    values = [hits, misses]

    plt.figure()
    plt.bar(labels, values)
    plt.xlabel("Tipo")
    plt.ylabel("Cantidad")
    plt.title("Rendimiento de la Cache")

    plt.savefig("/app/metrics.png")
    print("Gráfico guardado como metrics.png")


if __name__ == "__main__":
    run("uniform")  # cambia a "zipf"