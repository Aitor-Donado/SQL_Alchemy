from pymongo import MongoClient

import environ
env = environ.Env()
env.read_env(".env")
# Cadena de conexión de MongoDB Atlas
connection_string = env("connection_string")


# Conectar a la base de datos
client = MongoClient(connection_string)

# Verificar la conexión
try:
    # Listar las bases de datos disponibles
    databases = client.list_database_names()
    print("Conexión exitosa a MongoDB")
    print("Bases de datos disponibles:", databases)
except Exception as e:
    print("Error al conectar a MongoDB:", e)


db = client['biblioteca']
collection = db['resenias']

nueva_resenia = {
    "autor": "55E58A",
    "material": "ABC123",
    "resenia": "Muy buen libro. Me ha gustado",
    "mencionar_usuarios": ["B6EDE9"],
    "calificacion": 5,
    "fecha": ""
}   

collection.insert_one(nueva_resenia)

def listar_resenias():
    return list(collection.find({"autor": "55E58A", "material": "ABC123"}))

lista_resenias = listar_resenias()
print(lista_resenias)

# Todos los documentos
for usuario in db.resenias.find():
    print(usuario)


def borrar_resenia(autor, material):
    collection.delete_one({"autor": autor, "material": material})
    return "Resenia borrada correctamente"
borrar = borrar_resenia("55E58A", "ABC123")
print(borrar)  # Debería imprimir "Resenia borrada correctamente" si se borró correctamente,