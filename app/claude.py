# main.py
from fastapi import FastAPI, HTTPException, Query, Depends, status
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uvicorn
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

# Configuración de Firebase
# Asegúrate de tener tu archivo de credenciales descargado desde la consola de Firebase
cred = credentials.Certificate("./firebase-credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Inicialización de FastAPI
app = FastAPI(
    title="Fitness Gym API",
    description="API RESTful para gestionar ejercicios y rutinas de gimnasio",
    version="1.0.0",
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Esto permite todas las origenes. En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

# Modelos de Pydantic para validación
class EjercicioBase(BaseModel):
    nombre: str
    tipo_musculo: str
    dificultad: str
    instrucciones: str
    equipamiento: Optional[List[str]] = []

class EjercicioCreate(EjercicioBase):
    pass

class Ejercicio(EjercicioBase):
    id: str
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        orm_mode = True

class EjercicioEnRutina(BaseModel):
    ejercicio_id: str
    series: int
    repeticiones: int
    descanso_segundos: int

class RutinaBase(BaseModel):
    nombre: str
    nivel: str
    descripcion: str
    ejercicios: Optional[List[EjercicioEnRutina]] = []

class RutinaCreate(RutinaBase):
    pass

class Rutina(RutinaBase):
    id: str
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        orm_mode = True

class RutinaCompleta(Rutina):
    ejercicios_detallados: Optional[List[Dict[str, Any]]] = []

# Funciones auxiliares
def firestore_doc_to_dict(doc):
    """Convierte un documento de Firestore a un diccionario con su ID."""
    if doc.exists:
        data = doc.to_dict()
        data['id'] = doc.id
        return data
    return None

# Endpoints para Ejercicios
@app.post("/ejercicios/", response_model=Ejercicio, status_code=status.HTTP_201_CREATED)
async def crear_ejercicio(ejercicio: EjercicioCreate):
    """Crea un nuevo ejercicio en la base de datos."""
    try:
        ejercicios_ref = db.collection('ejercicios')
        
        datos_ejercicio = ejercicio.dict()
        datos_ejercicio['fecha_creacion'] = firestore.SERVER_TIMESTAMP
        
        # Añadir el documento a Firestore
        doc_ref = ejercicios_ref.document()  # Crear un ID automático
        doc_ref.set(datos_ejercicio)
        
        # Obtener el documento recién creado
        nuevo_doc = doc_ref.get()
        resultado = firestore_doc_to_dict(nuevo_doc)
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear ejercicio: {str(e)}")

@app.get("/ejercicios/", response_model=List[Ejercicio])
async def obtener_ejercicios(
    tipo_musculo: Optional[str] = Query(None, description="Filtrar por tipo de músculo"),
    dificultad: Optional[str] = Query(None, description="Filtrar por nivel de dificultad")
):
    """Obtiene todos los ejercicios con filtros opcionales."""
    try:
        query = db.collection('ejercicios')
        
        # Aplicar filtros si se proporcionan
        if tipo_musculo:
            query = query.where('tipo_musculo', '==', tipo_musculo)
        if dificultad:
            query = query.where('dificultad', '==', dificultad)
        
        ejercicios = query.stream()
        
        resultados = []
        for doc in ejercicios:
            data = firestore_doc_to_dict(doc)
            resultados.append(data)
        
        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener ejercicios: {str(e)}")

@app.get("/ejercicios/{ejercicio_id}", response_model=Ejercicio)
async def obtener_ejercicio(ejercicio_id: str):
    """Obtiene un ejercicio específico por su ID."""
    try:
        doc_ref = db.collection('ejercicios').document(ejercicio_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail=f"Ejercicio con ID {ejercicio_id} no encontrado")
        
        return firestore_doc_to_dict(doc)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el ejercicio: {str(e)}")

@app.put("/ejercicios/{ejercicio_id}", response_model=Ejercicio)
async def actualizar_ejercicio(ejercicio_id: str, ejercicio: EjercicioBase):
    """Actualiza un ejercicio existente."""
    try:
        doc_ref = db.collection('ejercicios').document(ejercicio_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail=f"Ejercicio con ID {ejercicio_id} no encontrado")
        
        datos_actualizados = ejercicio.dict()
        datos_actualizados['fecha_actualizacion'] = firestore.SERVER_TIMESTAMP
        
        # Actualizar el documento
        doc_ref.update(datos_actualizados)
        
        # Obtener el documento actualizado
        doc_actualizado = doc_ref.get()
        return firestore_doc_to_dict(doc_actualizado)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el ejercicio: {str(e)}")

@app.delete("/ejercicios/{ejercicio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_ejercicio(ejercicio_id: str):
    """Elimina un ejercicio específico."""
    try:
        doc_ref = db.collection('ejercicios').document(ejercicio_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail=f"Ejercicio con ID {ejercicio_id} no encontrado")
        
        # Eliminar el ejercicio de todas las rutinas que lo contienen
        rutinas = db.collection('rutinas').stream()
        for rutina_doc in rutinas:
            rutina_data = rutina_doc.to_dict()
            ejercicios = rutina_data.get('ejercicios', [])
            
            # Verificar si el ejercicio está en la rutina
            for ejercicio in ejercicios:
                if ejercicio.get('ejercicio_id') == ejercicio_id:
                    # Filtrar el ejercicio a eliminar
                    nuevos_ejercicios = [e for e in ejercicios if e.get('ejercicio_id') != ejercicio_id]
                    # Actualizar la rutina
                    db.collection('rutinas').document(rutina_doc.id).update({
                        'ejercicios': nuevos_ejercicios,
                        'fecha_actualizacion': firestore.SERVER_TIMESTAMP
                    })
                    break
        
        # Eliminar el ejercicio
        doc_ref.delete()
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el ejercicio: {str(e)}")

# Endpoints para Rutinas
@app.post("/rutinas/", response_model=Rutina, status_code=status.HTTP_201_CREATED)
async def crear_rutina(rutina: RutinaCreate):
    """Crea una nueva rutina de ejercicios."""
    try:
        rutinas_ref = db.collection('rutinas')
        
        datos_rutina = rutina.dict()
        datos_rutina['fecha_creacion'] = firestore.SERVER_TIMESTAMP
        
        # Añadir el documento a Firestore
        doc_ref = rutinas_ref.document()  # Crear un ID automático
        doc_ref.set(datos_rutina)
        
        # Obtener el documento recién creado
        nuevo_doc = doc_ref.get()
        resultado = firestore_doc_to_dict(nuevo_doc)
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear rutina: {str(e)}")

@app.get("/rutinas/", response_model=List[Rutina])
async def obtener_rutinas(
    nivel: Optional[str] = Query(None, description="Filtrar por nivel de dificultad")
):
    """Obtiene todas las rutinas con filtros opcionales."""
    try:
        query = db.collection('rutinas')
        
        # Aplicar filtros si se proporcionan
        if nivel:
            query = query.where('nivel', '==', nivel)
        
        rutinas = query.stream()
        
        resultados = []
        for doc in rutinas:
            data = firestore_doc_to_dict(doc)
            resultados.append(data)
        
        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener rutinas: {str(e)}")

@app.get("/rutinas/{rutina_id}", response_model=RutinaCompleta)
async def obtener_rutina(rutina_id: str, detallado: bool = Query(False, description="Incluir detalles completos de ejercicios")):
    """Obtiene una rutina específica por su ID, opcionalmente con detalles completos de ejercicios."""
    try:
        doc_ref = db.collection('rutinas').document(rutina_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail=f"Rutina con ID {rutina_id} no encontrada")
        
        datos_rutina = firestore_doc_to_dict(doc)
        
        # Si se solicita detalle completo, obtener información de cada ejercicio
        if detallado:
            ejercicios_completos = []
            for item in datos_rutina.get('ejercicios', []):
                ejercicio_id = item.get('ejercicio_id')
                ejercicio_doc = db.collection('ejercicios').document(ejercicio_id).get()
                
                if ejercicio_doc.exists:
                    ejercicio_datos = firestore_doc_to_dict(ejercicio_doc)
                    # Combinar datos del ejercicio con detalles de la rutina
                    ejercicio_en_rutina = {
                        **ejercicio_datos,
                        'series': item.get('series'),
                        'repeticiones': item.get('repeticiones'),
                        'descanso_segundos': item.get('descanso_segundos')
                    }
                    ejercicios_completos.append(ejercicio_en_rutina)
                else:
                    # Si el ejercicio no existe, incluir solo los datos de la rutina
                    ejercicios_completos.append(item)
            
            datos_rutina['ejercicios_detallados'] = ejercicios_completos
        
        return datos_rutina
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la rutina: {str(e)}")

@app.put("/rutinas/{rutina_id}", response_model=Rutina)
async def actualizar_rutina(rutina_id: str, rutina: RutinaBase):
    """Actualiza una rutina existente."""
    try:
        doc_ref = db.collection('rutinas').document(rutina_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail=f"Rutina con ID {rutina_id} no encontrada")
        
        datos_actualizados = rutina.dict()
        datos_actualizados['fecha_actualizacion'] = firestore.SERVER_TIMESTAMP
        
        # Actualizar el documento
        doc_ref.update(datos_actualizados)
        
        # Obtener el documento actualizado
        doc_actualizado = doc_ref.get()
        return firestore_doc_to_dict(doc_actualizado)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la rutina: {str(e)}")

@app.post("/rutinas/{rutina_id}/ejercicios", response_model=Rutina, status_code=status.HTTP_200_OK)
async def añadir_ejercicio_a_rutina(rutina_id: str, ejercicio_rutina: EjercicioEnRutina):
    """Añade un ejercicio a una rutina existente."""
    try:
        # Verificar que la rutina existe
        rutina_ref = db.collection('rutinas').document(rutina_id)
        rutina_doc = rutina_ref.get()
        
        if not rutina_doc.exists:
            raise HTTPException(status_code=404, detail=f"Rutina con ID {rutina_id} no encontrada")
        
        # Verificar que el ejercicio existe
        ejercicio_id = ejercicio_rutina.ejercicio_id
        ejercicio_doc = db.collection('ejercicios').document(ejercicio_id).get()
        
        if not ejercicio_doc.exists:
            raise HTTPException(status_code=404, detail=f"Ejercicio con ID {ejercicio_id} no encontrado")
        
        # Detalle del ejercicio en la rutina
        detalle_ejercicio = ejercicio_rutina.dict()
        
        # Actualizar el array de ejercicios usando arrayUnion
        rutina_ref.update({
            'ejercicios': firestore.ArrayUnion([detalle_ejercicio]),
            'fecha_actualizacion': firestore.SERVER_TIMESTAMP
        })
        
        # Obtener la rutina actualizada
        rutina_actualizada = rutina_ref.get()
        return firestore_doc_to_dict(rutina_actualizada)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al añadir ejercicio a la rutina: {str(e)}")

@app.delete("/rutinas/{rutina_id}/ejercicios/{ejercicio_id}", status_code=status.HTTP_200_OK, response_model=Rutina)
async def eliminar_ejercicio_de_rutina(rutina_id: str, ejercicio_id: str):
    """Elimina un ejercicio específico de una rutina."""
    try:
        # Verificar que la rutina existe
        rutina_ref = db.collection('rutinas').document(rutina_id)
        rutina_doc = rutina_ref.get()
        
        if not rutina_doc.exists:
            raise HTTPException(status_code=404, detail=f"Rutina con ID {rutina_id} no encontrada")
        
        # Obtener los datos actuales de la rutina
        datos_rutina = rutina_doc.to_dict()
        ejercicios = datos_rutina.get('ejercicios', [])
        
        # Filtrar el ejercicio que queremos eliminar
        nuevos_ejercicios = [e for e in ejercicios if e.get('ejercicio_id') != ejercicio_id]
        
        # Verificar si el ejercicio estaba en la rutina
        if len(nuevos_ejercicios) == len(ejercicios):
            raise HTTPException(status_code=404, detail=f"Ejercicio con ID {ejercicio_id} no encontrado en la rutina")
        
        # Actualizar la rutina
        rutina_ref.update({
            'ejercicios': nuevos_ejercicios,
            'fecha_actualizacion': firestore.SERVER_TIMESTAMP
        })
        
        # Obtener la rutina actualizada
        rutina_actualizada = rutina_ref.get()
        return firestore_doc_to_dict(rutina_actualizada)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar ejercicio de la rutina: {str(e)}")

@app.delete("/rutinas/{rutina_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_rutina(rutina_id: str):
    """Elimina una rutina específica."""
    try:
        doc_ref = db.collection('rutinas').document(rutina_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail=f"Rutina con ID {rutina_id} no encontrada")
        
        # Eliminar la rutina
        doc_ref.delete()
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la rutina: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)