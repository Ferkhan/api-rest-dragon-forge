import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("dragon-forge-cred.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

pelicula_1 = {
    "nombre": "IronMan",
    "descipcion": "Un hombre se convierte en un superhéroe",
    "genero": "Accion",
    "anio": 2008
}

pelicula_2 = {
    "nombre": "Now You See Me",
    "descipcion": "Un grupo de ilusionistas comete robos durante sus espectáculos",
    "genero": "Accion",
    "anio": 2013
}

pelicula_3 = {
    "nombre": "El Origen",
    "descipcion": "Un ladrón que roba secretos a través de los sueños",
    "genero": "Accion",
    "anio": 2010
}

# Crear una colección y agregar un documento
def guardar():
    # Agregar un nuevo documento a la colección "peliculas"
    db.collection("peliculas").document("ironman").set(pelicula_1)
    db.collection("peliculas").document().set(pelicula_2)
    db.collection("peliculas").document("subpeli").document("otra peli").set(pelicula_2)

guardar()