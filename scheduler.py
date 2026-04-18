# 🔥 ESTRUCTURAS POR USUARIO
colas_por_usuario = {}
historial_por_usuario = {}
resultados_por_usuario = {}


# =========================
#  ASEGURAR USUARIO
# =========================
def asegurar_usuario(usuario):
    if usuario not in colas_por_usuario:
        colas_por_usuario[usuario] = []
        historial_por_usuario[usuario] = []
        resultados_por_usuario[usuario] = []


# =========================
#  AGREGAR PROCESO
# =========================
def agregar_proceso(usuario, nombre, tamano, prioridad):
    asegurar_usuario(usuario)

    proceso = {
        "nombre": nombre,
        "tamano": tamano,
        "prioridad": prioridad
    }

    colas_por_usuario[usuario].append(proceso)
    historial_por_usuario[usuario].append(proceso)


# =========================
#  FIFO
# =========================
def ejecutar_fifo(usuario):
    asegurar_usuario(usuario)

    cola = colas_por_usuario[usuario]
    resultados_por_usuario[usuario] = []  # 🔥 limpiar resultados anteriores

    resultados = []
    tiempo_actual = 0

    for proceso in cola:
        inicio = tiempo_actual
        fin = inicio + proceso["tamano"]

        resultado = {
            "archivo": proceso["nombre"],
            "inicio": inicio,
            "fin": fin
        }

        resultados.append(resultado)
        resultados_por_usuario[usuario].append(resultado)

        tiempo_actual = fin

    return resultados


# =========================
# ROUND ROBIN
# =========================
def ejecutar_round_robin(usuario, quantum):
    asegurar_usuario(usuario)

    cola = colas_por_usuario[usuario].copy()
    resultados_por_usuario[usuario] = []

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
                resultados_por_usuario[usuario].append(resultado)

                tiempo_actual = fin
                restantes[nombre] -= ejecucion

    return resultados


# =========================
#  PRIORIDADES
# =========================
def ejecutar_prioridades(usuario):
    asegurar_usuario(usuario)

    cola = sorted(colas_por_usuario[usuario], key=lambda x: x["prioridad"])
    resultados_por_usuario[usuario] = []

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
        resultados_por_usuario[usuario].append(resultado)

        tiempo_actual = fin

    return resultados


# =========================
#  HISTORIAL
# =========================
def obtener_historial(usuario):
    asegurar_usuario(usuario)
    return historial_por_usuario[usuario]


# =========================
#  RESULTADOS
# =========================
def obtener_resultados(usuario):
    asegurar_usuario(usuario)
    return resultados_por_usuario[usuario]


# =========================
#  LIMPIAR HISTORIAL
# =========================
def limpiar_historial(usuario):
    asegurar_usuario(usuario)
    historial_por_usuario[usuario] = []