import time
import json
from redis_client import r

print("Worker iniciado...")

while True:
    proceso = r.lpop("cola_procesos")

    if proceso:
        p = json.loads(proceso)

        print(f"Procesando: {p['nombre']}")

        tiempo = p["tamano"] / 1000  # simula tiempo
        time.sleep(tiempo)

        print(f"Terminado: {p['nombre']}")

    else:
        time.sleep(2)