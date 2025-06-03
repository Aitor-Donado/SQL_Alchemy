from fastapi import FastAPI, HTTPException
import pickle
from uuid import uuid4 as uuid 
from datetime import datetime
app = FastAPI()

############### PERSISTENCIA DE DATOS ###############
# Es mejor usar una base de datos, por supuesto.
# Función para guardar datos en un archivo pickle
def guarda_datos(publicaciones):
    with open("publicaciones.pckl", 'wb') as archivo:
        pickle.dump(publicaciones, archivo)

# Función para cargar datos desde un archivo pickle
def carga_datos():
    try:
        with open("publicaciones.pckl", 'rb') as archivo:
            publicaciones = pickle.load(archivo)
        return publicaciones
    except FileNotFoundError:
        return []

publicaciones = carga_datos()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la biblioteca"}

@app.post("/publicacion")
def guardar_publicacion(titulo: str, 
				contenido: str, 
				autor: str = "Anónimo"):
    nueva_publicacion = {
        "id": str(uuid()),
        "titulo": titulo,
        "autor": autor,
        "contenido": contenido,
        "fecha_creacion": datetime.now().isoformat(),
        "fecha_publicacion": None
    }
    publicaciones.append(nueva_publicacion)
    guarda_datos(publicaciones)
    return nueva_publicacion

@app.get("/listado")
def lee_listado():
    return {"listado": publicaciones}

@app.get("/listado/{identificador}")
def lee_publicacion_id(identificador: str):
    for publicacion in publicaciones:
        if publicacion["id"] == identificador:
            return publicacion
    raise HTTPException(status_code=404, 
					    detail="Publicación no encontrada")

@app.put("/actualizacion/{identificador}")
def actualiza_publicacion(identificador: str, 
						  titulo: str, 
						  contenido: str, 
						  autor: str = "Anónimo"):
    for publicacion in publicaciones:
        if publicacion["id"] == identificador:
            publicacion["titulo"] = titulo
            publicacion["contenido"] = contenido
            publicacion["autor"] = autor
            publicacion["fecha_publicacion"] = datetime.now().isoformat()
            guarda_datos(publicaciones)
            return publicacion
    raise HTTPException(status_code=404, 
					    detail="Publicación no encontrada")

@app.delete("/borrado/{identificador}")
def borra_publicacion(identificador: str):
    for publicacion in publicaciones:
        if publicacion["id"] == identificador:
            publicaciones.remove(publicacion)
            guarda_datos(publicaciones)
            return {"mensaje": "Publicación eliminada"}
    raise HTTPException(status_code=404, 
					    detail="Publicación no encontrada")