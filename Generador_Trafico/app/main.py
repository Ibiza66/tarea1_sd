import os

version = os.getenv("VERSION", "v1")

if version == "v2":
    from traffic_v2 import run
else:
    from traffic_v1 import run

if __name__ == "__main__":
    run()