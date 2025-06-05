# main_api.py
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Request, Form, Depends
from typing import Optional, List
from GestorBiblioteca import GestorBiblioteca
from fastapi.middleware.cors import CORSMiddleware
from gestor_resenias import GestorDatosResenias

app = FastAPI(title="API Biblioteca")
# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los headers
)

# modelos de Pydantic
from pydantic import BaseModel, Field


#---------------- Modelo para prestamos ----------------
class PrestamoCreate(BaseModel):
    id_usuario: str = Field(..., example="55E58A")
    id_material: str = Field(..., example="ABC123")


#---------------- Modelo para materiales ----------------
class MaterialForm(BaseModel):
    tipo: str
    titulo: str
    autor: Optional[str] = None
    isbn: Optional[str] = None
    numero_paginas: Optional[int] = None
    fecha_publicacion: Optional[str] = None
    numero_edicion: Optional[str] = None
    duracion: Optional[int] = None
    director: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        tipo: str = Form(...),
        titulo: str = Form(...),
        autor: Optional[str] = Form(None),
        isbn: Optional[str] = Form(None),
        numero_paginas: Optional[int] = Form(None),
        fecha_publicacion: Optional[str] = Form(None),
        numero_edicion: Optional[str] = Form(None),
        duracion: Optional[int] = Form(None),
        director: Optional[str] = Form(None),
    ) -> "MaterialForm":
        return cls(
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

# ---------------- Modelo para resenias ----------------
class Resenia(BaseModel):
    id_material: str
    id_usuario: str
    comentario: str
    calificacion: int = Field(..., ge=1, le=5)
    mencionar_usuarios: List[str] = []
    fecha: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def as_form(
        cls,
        id_material: str = Form(...),
        id_usuario: str = Form(...),
        comentario: str = Form(...),
        calificacion: int = Form(...),
        mencionar_usuarios: Optional[str] = Form(default=""),  # CSV string input
    ):
        mencionar_lista = [u.strip() for u in mencionar_usuarios.split(",") if u.strip()]
        return cls(
            id_material=id_material,
            id_usuario=id_usuario,
            comentario=comentario,
            calificacion=calificacion,
            mencionar_usuarios=mencionar_lista,
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
def crear_material(material: MaterialForm = Depends(MaterialForm.as_form)):
    try:
        codigo = biblioteca.agregar_material(
            tipo=material.tipo,
            titulo=material.titulo,
            autor=material.autor,
            isbn=material.isbn,
            numero_paginas=material.numero_paginas,
            fecha_publicacion=material.fecha_publicacion,
            numero_edicion=material.numero_edicion,
            duracion=material.duracion,
            director=material.director,
        )
        return biblioteca.buscar_material(codigo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

"""
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
"""
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

gdr = GestorDatosResenias()

@app.post("/resenias/")
def crear_resenia(resenia: Resenia = Depends(Resenia.as_form)):
    try:
        id_insertado = gdr.aniadir_resenia(resenia.model_dump())
        return {"mensaje": "Reseña guardada", "id": id_insertado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
