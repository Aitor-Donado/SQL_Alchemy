import environ
env = environ.Env()
env.read_env(".env")
# Cadena de conexión de MongoDB Atlas
connection_string = env("connection_string")

from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import Dict

class GestorDatosResenias:
    def __init__(self, uri="mongodb://localhost:27017", db_name="biblioteca"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.coleccion = self.db["resenias"]

    def aniadir_resenia(self, resenia: Dict) -> str:
        resultado = self.coleccion.insert_one(resenia)
        return str(resultado.inserted_id)
    
    def listar_resenias_todas(self) -> list:
        return list(self.coleccion.find())
    
    def listar_resenias_usu(self, id_material: str) -> list:
        return list(self.coleccion.find({"id_usuario": id_material}))
    
    def listar_resenias_mat(self, id_material: str) -> list:
        return list(self.coleccion.find({"id_material": id_material}))
    