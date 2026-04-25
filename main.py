from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

#  IMPORTACIONES MULTIUSUARIO
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



#  INICIO - LOGIN

@app.get("/")
def inicio():
    return FileResponse("static/login.html")



#  SUBIR ARCHIVO

@app.post("/upload")
async def subir_archivo(
    file: UploadFile = File(...),
    prioridad: int = 1,
    user: str = ""
):
    #  VALIDAR USUARIO
    if not user or user.strip() == "":
        return {"error": "Usuario no enviado"}

    user = user.strip()

    #  DEBUG 
    print("USUARIO RECIBIDO:", user)

    ruta = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(ruta, "wb") as f:
        contenido = await file.read()
        f.write(contenido)

    tamano = len(contenido)

    #  ASEGURAR QUE SE GUARDE CON EL USUARIO CORRECTO
    agregar_proceso(user, file.filename, tamano, prioridad)

    return {
        "mensaje": "Archivo subido",
        "usuario": user,   #  para verificar
        "tamano": tamano
    }



#  FIFO

@app.get("/procesar")
def procesar(user: str):
    return ejecutar_fifo(user)



#  ROUND ROBIN

@app.get("/procesar_rr")
def procesar_rr(user: str, quantum: int = 2):
    return ejecutar_round_robin(user, quantum)



#  PRIORIDADES

@app.get("/procesar_prioridad")
def procesar_prioridad(user: str):
    return ejecutar_prioridades(user)



#  GANTT

@app.get("/gantt_fifo")
def gantt_fifo(user: str):
    resultado = ejecutar_fifo(user)
    generar_gantt(resultado)
    return resultado



#  WEB PRINCIPAL

@app.get("/web")
def web():
    return FileResponse("static/index.html")



#  HISTORIAL

@app.get("/historial")
def historial(user: str):
    return obtener_historial(user)


@app.delete("/historial")
def borrar_historial(user: str):
    limpiar_historial(user)
    return {"mensaje": "Historial eliminado"}



#  RESULTADOS

@app.get("/resultados")
def resultados(user: str):
    return obtener_resultados(user)



#  REGISTRO (opcional)

@app.post("/register")
def register(user: str, password: str):
    from database import cursor, conn

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (user, password)
    )
    conn.commit()

    return {"msg": "Usuario creado"}



#  LOGIN

@app.post("/login")
def login(user: str, password: str):
    if password == "12345678":
        return {"status": "ok", "user": user}
    return {"status": "error"}