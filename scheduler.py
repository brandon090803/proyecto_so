#  MEMORIA LOCAL (reemplazo de Redis)
cola_memoria = []
historial_memoria = []
resultados_memoria = []


# AGREGAR PROCESO

def agregar_proceso(nombre, tamano, prioridad):
    proceso = {
        "nombre": nombre,
        "tamano": tamano,
        "prioridad": prioridad
    }

    # Cola en memoria
    cola_memoria.append(proceso)

    # Historial
    historial_memoria.append(proceso)



# FIFO

def ejecutar_fifo():
    resultados = []
    tiempo_actual = 0

    for proceso in cola_memoria:
        inicio = tiempo_actual
        fin = inicio + proceso["tamano"]

        resultado = {
            "archivo": proceso["nombre"],
            "inicio": inicio,
            "fin": fin
        }

        resultados.append(resultado)

        # 🔥 Guardar resultados en memoria
        resultados_memoria.append(resultado)

        tiempo_actual = fin

    return resultados



# ROUND ROBIN

def ejecutar_round_robin(quantum):
    cola = cola_memoria.copy()

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
                resultados_memoria.append(resultado)

                tiempo_actual = fin
                restantes[nombre] -= ejecucion

    return resultados



# PRIORIDADES

def ejecutar_prioridades():
    cola = sorted(cola_memoria, key=lambda x: x["prioridad"])

    resultados = []
    tiempo_actual = 0

    for proceso in cola:
        inicio = tiempo_actual
        fin = inicio + proceso["tamano"]

        resultado = {
            "archivo": proceso["nombre"],
            "inicio": inicio,
            "fin": fin,
            "prioridad": proceso["prioridad"]
        }

        resultados.append(resultado)
        resultados_memoria.append(resultado)

        tiempo_actual = fin

    return resultados



# HISTORIAL

def obtener_historial():
    return historial_memoria



# RESULTADOS

def obtener_resultados():
    return resultados_memoria



# LIMPIAR HISTORIAL

def limpiar_historial():
    historial_memoria.clear()