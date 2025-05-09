from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

"""Modelo para crear ejercicios"""
class Ejercicio(BaseModel):
    nombre: str
    grupo_muscular: List[str]
    dificultad: str
    instrucciones: str
    equipamiento: Optional[List[str]] = Field(default=['hola bola'])
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    imagen_url: Optional[str] = None
    estado_registro: Optional[bool] = True # True si el documento está activo, False si está inactivo
    # errores_comunes: Optional[List[str]] = []

    model_config = {
        'json_schema_extra': {
            'example': {
                'nombre': 'Flexiones de brazos',
                'grupo_muscular': ['Pecho', 'Tríceps'],
                'dificultad': 'Intermedio',
                'instrucciones': 'Coloca tus manos en el suelo a la altura de los hombros...',
                'equipamiento': ['Colchoneta']
            }
        }
    }

"""Modelo para leer ejercicios"""
class EjercicioOut(Ejercicio):
    id: str  # ID del documento en Firestore


class EjercicioEnRutina(BaseModel):
    ejercicio_id: str
    series: int
    repeticiones: int
    descanso_segundos: int

class Rutina(BaseModel):
    nombre: str
    nivel: str
    descripcion: Optional[str] = None
    ejercicios: Optional[List[EjercicioEnRutina]] = []
    duracion_minutos: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    estado_registro: Optional[bool] = True # True si el documento está activo, False si está inactivo

    model_config = {
        'json_schema_extra': {
            'example': {
                'nombre': 'Rutina de Fuerza',
                'nivel': 'Intermedio',
                'descripcion': 'Rutina enfocada en aumentar la fuerza muscular.',
                'ejercicios': [
                    {
                        'ejercicio_id': 'ejercicio_1',
                        'series': 3,
                        'repeticiones': 10,
                        'descanso_segundos': 60
                    },
                    {
                        'ejercicio_id': 'ejercicio_2',
                        'series': 4,
                        'repeticiones': 8,
                        'descanso_segundos': 90
                    }
                ],
                'duracion_minutos': 45
            }   
        }
    }


class Usuario(BaseModel):
    nombre: str
    email: str
    contrasena: str
    telefono: Optional[str] = None
    fecha_registro: datetime
    fecha_nacimiento: datetime
    peso: float
    altura: float
    sexo: str  # 'masculino' o 'femenino'
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    estado_registro: Optional[bool] = True # True si el documento está activo, False si está inactivo

    rutinas: Optional[List[str]] = []  # IDs de rutinas asociadas al usuario
    ejercicios_favoritos: Optional[List[str]] = []  # IDs de ejercicios favoritos
    rutinas_favoritas: Optional[List[str]] = []  # IDs de rutinas favoritas


# MODELOS CON VALIDACIONES PARA CREAR UN NUEVO ELEMENTO
# class EjercicioCrear(BaseModel):
#     nombre: str = Field(..., min_length=1, max_length=100)
#     grupo_muscular: List[str] = Field(..., min_items=1)
#     dificultad: str = Field(..., min_length=1, max_length=50)
#     instrucciones: str = Field(..., min_length=1, max_length=500)
#     equipamiento: Optional[List[str]] = Field(default_factory=list)
#     fecha_creacion: Optional[datetime] = None
#     fecha_actualizacion: Optional[datetime] = None
#     estado_registro: Optional[bool] = True # True si el documento está activo, False si está inactivo
