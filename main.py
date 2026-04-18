from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

#  IMPORTACIONES CORRECTAS (sin Redis)
from scheduler import (
    agregar_proceso,
    ejecutar_fifo,
    ejecutar_round_robin,
    ejecutar_prioridades,
    obtener_historial,
    obtener_resultados,
    limpiar_historial
)

from gantt import generar_gantt

app = FastAPI()

#  carpeta static
app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



# INICIO

@app.get("/")
def inicio():
    return {"mensaje": "Servidor funcionando"}



# SUBIR ARCHIVO

@app.post("/upload")
async def subir_archivo(file: UploadFile = File(...), prioridad: int = 1, user: str = ""):
    ruta = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(ruta, "wb") as f:
        contenido = await file.read()
        f.write(contenido)

    tamano = len(contenido)

    agregar_proceso(user, file.filename, tamano, prioridad)

    return {"mensaje": "Archivo subido"}



# FIFO

@app.get("/procesar")
def procesar(user: str):
    return ejecutar_fifo(user)



# ROUND ROBIN

@app.get("/procesar_rr")
def procesar_rr(quantum: int = 2):
    return ejecutar_round_robin(quantum)



# PRIORIDADES

@app.get("/procesar_prioridad")
def procesar_prioridad():
    return ejecutar_prioridades()



# GANTT

@app.get("/gantt_fifo")
def gantt_fifo():
    resultado = ejecutar_fifo()
    generar_gantt(resultado)
    return resultado



# WEB

@app.get("/web")
def web():
    return FileResponse("static/index.html")



# HISTORIAL (SIN REDIS)

@app.get("/historial")
def historial():
    return obtener_historial()


@app.delete("/historial")
def borrar_historial():
    limpiar_historial()
    return {"mensaje": "Historial eliminado"}



# RESULTADOS (SIN REDIS)

@app.get("/resultados")
def resultados():
    return obtener_resultados()


# REGISTRO

@app.post("/register")
def register(user: str, password: str):
    from database import cursor, conn

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (user, password)
    )
    conn.commit()

    return {"msg": "Usuario creado"}



# LOGIN

@app.post("/login")
def login(user: str, password: str):
    if password == "12345678":
        return {"status": "ok", "user": user}
    return {"status": "error"}