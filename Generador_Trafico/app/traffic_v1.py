import requests
import random
import time
import matplotlib.pyplot as plt

URL = "http://cache-service:8000/query"
METRICS_URL = "http://cache-service:8000/metrics"

ZONES = ["Z1", "Z2", "Z3", "Z4", "Z5"]
QUERIES = ["Q1", "Q2", "Q3", "Q4", "Q5"]


def random_query():
    q = random.choice(QUERIES)

    if q == "Q4":
        return {
            "query_type": q,
            "zone_id_a": random.choice(ZONES),
            "zone_id_b": random.choice(ZONES),
            "confidence_min": random.random()
        }

    elif q == "Q5":
        return {
            "query_type": q,
            "zone_id": random.choice(ZONES),
            "bins": random.randint(3, 10)
        }

    else:
        return {
            "query_type": q,
            "zone_id": random.choice(ZONES),
            "confidence_min": random.random()
        }


def run(n_requests=100):
    for i in range(n_requests):
        payload = random_query()

        try:
            r = requests.post(URL, json=payload)
            print(f"{i+1}/{n_requests}", r.status_code)
        except Exception as e:
            print("Error:", e)

        time.sleep(0.1)

    print("\n Obteniendo métricas...\n")
    show_metrics()


def show_metrics():
    try:
        r = requests.get(METRICS_URL)
        data = r.json()

        hits = data.get("hits", 0)
        misses = data.get("misses", 0)

        print("Metrics:", data)

        plt.figure()

        labels = ["Hits", "Misses"]
        values = [hits, misses]

        plt.bar(labels, values)
        plt.title("Cache Performance")
        plt.xlabel("Type")
        plt.ylabel("Count")

        plt.savefig("/app/metrics.png")
        print("Gráfico guardado como metrics.png")

    except Exception as e:
        print("Error obteniendo métricas:", e)


if __name__ == "__main__":
    run(200)