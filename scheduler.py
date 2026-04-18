#  ESTRUCTURAS POR USUARIO
colas_por_usuario = {}
historial_por_usuario = {}
resultados_por_usuario = {}


# =========================
# AGREGAR PROCESO
# =========================
def agregar_proceso(usuario, nombre, tamano, prioridad):
    proceso = {
        "nombre": nombre,
        "tamano": tamano,
        "prioridad": prioridad
    }

    # Crear estructuras si no existen
    if usuario not in colas_por_usuario:
        colas_por_usuario[usuario] = []
        historial_por_usuario[usuario] = []
        resultados_por_usuario[usuario] = []

    # Guardar en cola e historial
    colas_por_usuario[usuario].append(proceso)
    historial_por_usuario[usuario].append(proceso)


# =========================
# FIFO
# =========================
def ejecutar_fifo(usuario):
    cola = colas_por_usuario.get(usuario, [])

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
    cola = colas_por_usuario.get(usuario, []).copy()

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
# PRIORIDADES
# =========================
def ejecutar_prioridades(usuario):
    cola = sorted(colas_por_usuario.get(usuario, []), key=lambda x: x["prioridad"])

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
# HISTORIAL
# =========================
def obtener_historial(usuario):
    return historial_por_usuario.get(usuario, [])


# =========================
# RESULTADOS
# =========================
def obtener_resultados(usuario):
    return resultados_por_usuario.get(usuario, [])



# LIMPIAR HISTORIAL
# =========================
def limpiar_historial(usuario):
    if usuario in historial_por_usuario:
        historial_por_usuario[usuario].clear()