from redis_client import r
import json

def agregar_proceso(nombre, tamano, prioridad):
    proceso = {
        "nombre": nombre,
        "tamano": tamano,
        "prioridad": prioridad
    }

    # Cola principal
    r.rpush("cola_procesos", json.dumps(proceso))

    # Historial de entrada
    r.rpush("historial", json.dumps(proceso))


# =========================
# FIFO
# =========================
def ejecutar_fifo():
    resultados = []
    tiempo_actual = 0

    procesos = r.lrange("cola_procesos", 0, -1)

    for p in procesos:
        proceso = json.loads(p)

        inicio = tiempo_actual
        fin = inicio + proceso["tamano"]

        resultado = {
            "archivo": proceso["nombre"],
            "inicio": inicio,
            "fin": fin
        }

        # Mostrar en la web
        resultados.append(resultado)

        # 🔥 Guardar ejecución en Redis
        r.rpush("resultados", json.dumps(resultado))

        tiempo_actual = fin

    return resultados


# =========================
# ROUND ROBIN
# =========================
def ejecutar_round_robin(quantum):
    procesos_raw = r.lrange("cola_procesos", 0, -1)
    cola = [json.loads(p) for p in procesos_raw]

    resultados = []
    tiempo_actual = 0

    restantes = {p["nombre"]: p["tamano"] for p in cola}

    while any(t > 0 for t in restantes.values()):
        for proceso in cola:
            nombre = proceso["nombre"]

            if restantes[nombre] > 0:
                inicio = tiempo_actual
                ejecucion = min(quantum, restantes[nombre])
                fin = inicio + ejecucion

                resultado = {
                    "archivo": nombre,
                    "inicio": inicio,
                    "fin": fin
                }

                resultados.append(resultado)

                # 🔥 Guardar ejecución en Redis
                r.rpush("resultados", json.dumps(resultado))

                tiempo_actual = fin
                restantes[nombre] -= ejecucion

    return resultados


# =========================
# PRIORIDADES
# =========================
def ejecutar_prioridades():
    procesos_raw = r.lrange("cola_procesos", 0, -1)
    cola = [json.loads(p) for p in procesos_raw]

    resultados = []
    tiempo_actual = 0

    cola_ordenada = sorted(cola, key=lambda x: x["prioridad"])

    for proceso in cola_ordenada:
        inicio = tiempo_actual
        fin = inicio + proceso["tamano"]

        resultado = {
            "archivo": proceso["nombre"],
            "inicio": inicio,
            "fin": fin,
            "prioridad": proceso["prioridad"]
        }

        resultados.append(resultado)

        # 🔥 Guardar ejecución en Redis
        r.rpush("resultados", json.dumps(resultado))

        tiempo_actual = fin

    return resultados