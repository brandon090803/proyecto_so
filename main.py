from fastapi import FastAPI, UploadFile, File
import os
from scheduler import agregar_proceso, ejecutar_fifo
from scheduler import ejecutar_round_robin
from gantt import generar_gantt
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.get("/")
def inicio():
    return {"mensaje": "Servidor funcionando"}

@app.post("/upload")
async def subir_archivo(file: UploadFile = File(...), prioridad: int = 1):
    ruta = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(ruta, "wb") as f:
        contenido = await file.read()
        f.write(contenido)

    tamano = len(contenido)  

    agregar_proceso(file.filename, tamano, prioridad)

    return {"mensaje": "Archivo subido", "tamano": tamano}  

@app.get("/procesar")
def procesar():
    resultado = ejecutar_fifo()
    return resultado

@app.get("/procesar_rr")
def procesar_rr(quantum: int = 2):
    resultado = ejecutar_round_robin(quantum)
    return resultado

@app.get("/procesar_prioridad")
def procesar_prioridad():
    from scheduler import ejecutar_prioridades
    return ejecutar_prioridades()

@app.get("/gantt_fifo")
def gantt_fifo():
    resultado = ejecutar_fifo()
    generar_gantt(resultado)
    return resultado

from fastapi.responses import FileResponse

@app.get("/web")
def web():
    return FileResponse("static/index.html")

@app.get("/historial")
def historial():
    import json
    from redis_client import r

    datos = r.lrange("historial", 0, -1)
    return [json.loads(d) for d in datos]

@app.delete("/historial")
def limpiar_historial():
    from redis_client import r
    r.delete("historial")
    return {"mensaje": "Historial eliminado"}

@app.get("/resultados")
def resultados():
    import json
    from redis_client import r
    datos = r.lrange("resultados", 0, -1)
    return [json.loads(d) for d in datos]


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
    from database import cursor

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (user, password)
    )

    if cursor.fetchone():
        return {"status": "ok"}

    return {"status": "error"}

