# main_api.py
from fastapi import FastAPI, HTTPException, Request
from typing import Optional
from GestorBiblioteca import GestorBiblioteca
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Biblioteca")

# modelos de Pydantic
from pydantic import BaseModel, Field
class PrestamoCreate(BaseModel):
    id_usuario: str = Field(..., description="ID del usuario que realiza el préstamo", example="55E58A")
    id_material: str = Field(..., description="ID del material a prestar", example="ABC123")



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
async def crear_prestamo(prestamo: PrestamoCreate):
    try:
        biblioteca.agregar_prestamo(prestamo.id_usuario, prestamo.id_material)
        return {"mensaje": "Préstamo registrado correctamente"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
"""
@app.post("/prestamos/")
async def crear_prestamo(request: Request):
    try:
        body = await request.json()
        print(body)
        id_usuario = body.get("id_usuario")
        id_material = body.get("id_material")

        if not id_usuario or not id_material:
            raise HTTPException(status_code=422, detail="Faltan datos obligatorios")

        biblioteca.agregar_prestamo(id_usuario, id_material)

        return {"mensaje": "Préstamo registrado correctamente"}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
"""
@app.get("/prestamos/")
def listar_prestamos():
    return biblioteca.listar_prestamos()