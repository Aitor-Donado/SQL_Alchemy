# main_api.py
from fastapi import FastAPI, HTTPException
from typing import Optional
from GestorBiblioteca import GestorBiblioteca
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Biblioteca")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

biblioteca = GestorBiblioteca()

# ---------------- USUARIOS ----------------

@app.post("/usuarios/")
def crear_usuario(nombre: str, apellido: str):
    id_usuario = biblioteca.agregar_usuario(nombre, apellido)
    return {"id_usuario": id_usuario, "nombre": nombre, "apellido": apellido}

@app.get("/usuarios/")
def listar_usuarios():
    return biblioteca.listar_usuarios()


# ---------------- MATERIALES ----------------

@app.post("/materiales/")
def crear_material(
    tipo: str,
    titulo: str,
    autor: Optional[str] = None,
    isbn: Optional[str] = None,
    numero_paginas: Optional[int] = None,
    fecha_publicacion: Optional[str] = None,
    numero_edicion: Optional[str] = None,
    duracion: Optional[int] = None,
    director: Optional[str] = None,
):
    try:
        codigo = biblioteca.agregar_material(
            tipo=tipo,
            titulo=titulo,
            autor=autor,
            isbn=isbn,
            numero_paginas=numero_paginas,
            fecha_publicacion=fecha_publicacion,
            numero_edicion=numero_edicion,
            duracion=duracion,
            director=director,
        )
        return biblioteca.buscar_material(codigo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/materiales/")
def listar_materiales():
    return biblioteca.listar_materiales()

@app.get("/materiales/{codigo}")
def obtener_material(codigo: str):
    m = biblioteca.buscar_material(codigo)
    if not m:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    return m

@app.delete("/materiales/{codigo}")
def eliminar_material(codigo: str):
    if biblioteca.borrar_material(codigo):
        return {"mensaje": "Material eliminado"}
    raise HTTPException(status_code=404, detail="Material no encontrado")


# ---------------- PRÉSTAMOS ----------------

@app.post("/prestamos/")
def agregar_prestamo(id_usuario: str, id_material: str):
    exito = biblioteca.agregar_prestamo(id_usuario, id_material)
    if not exito:
        raise HTTPException(status_code=400, detail="No se pudo registrar el préstamo")
    return {"mensaje": "Préstamo registrado"}

@app.get("/prestamos/")
def listar_prestamos():
    return biblioteca.listar_prestamos()