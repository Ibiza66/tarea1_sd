import requests
import random
import time
import matplotlib.pyplot as plt

URL = "http://cache-service:8000/query"

ZONES = ["Z1", "Z2", "Z3", "Z4", "Z5"]
QUERIES = ["Q1", "Q2", "Q3", "Q4", "Q5"]

# 👇 listas para guardar comportamiento real
x_points = []
y_points = []


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


def run(mode="uniform", n_requests=200):
    print("🚦 Traffic generator iniciado")

    for i in range(n_requests):
        payload = random_query()

        try:
            r = requests.post(URL, json=payload)
            data = r.json()

            # 👇 registrar comportamiento real
            if data.get("source") == "cache":
                y_points.append(1)  # HIT
            else:
                y_points.append(0)  # MISS

            x_points.append(i)

            print(f"{i+1}/{n_requests} -> {data.get('source')}")

        except Exception as e:
            print("Error:", e)

        time.sleep(0.1)

    print("\n📊 Generando gráfico...\n")
    draw()


def draw():
    plt.figure()

    # 👇 gráfico de puntos (ordenado)
    plt.scatter(x_points, y_points, alpha=0.6)

    plt.title("Cache behavior per query (v1)")
    plt.xlabel("Query index")
    plt.ylabel("Result")

    plt.yticks([0, 1], ["Miss", "Hit"])

    plt.savefig("/app/metrics.png")
    print("Gráfico guardado en /app/metrics.png")


if __name__ == "__main__":
    run("uniform")