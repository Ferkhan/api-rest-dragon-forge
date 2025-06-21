from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

"""Modelo para crear ejercicios"""
class EjercicioIn(BaseModel):
    nombre: str
    grupo_muscular: List[str]
    dificultad: str
    instrucciones: str
    equipamiento: Optional[List[str]] = Field(default_factory=list)
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    imagen_url: Optional[str] = "https://firebasestorage.googleapis.com/v0/b/dragon-forge-6b879.firebasestorage.app/o/default%2Fejercicios%2Fdefault.webp?alt=media&token=aa7be216-e02e-49fb-b24f-3e00f968202b"
    estado_registro: Optional[bool] = True # True si el documento está activo, False si está inactivo
    # errores_comunes: Optional[List[str]] = []

    model_config = {
        'json_schema_extra': {
            'example': {
                'nombre': 'Flexiones de brazos',
                'grupo_muscular': ['Pecho', 'Tríceps'],
                'dificultad': 'Intermedio',
                'instrucciones': 'Coloca tus manos en el suelo a la altura de los hombros',
                'equipamiento': ['Colchoneta']
            }
        }
    }

"""Modelo para leer ejercicios"""
class EjercicioOut(EjercicioIn):
    id: str  # ID del documento en Firestore


class EjercicioEnRutina(BaseModel):
    ejercicio_id: str
    series: int
    repeticiones: int
    descanso_segundos: int

"""Modelo para crear rutinas"""
class RutinaIn(BaseModel):
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

"""Modelo para leer rutinas"""
class RutinaOut(RutinaIn):
    id: str  # ID del documento en Firestore

"""Modelo para crear usuarios"""
class UsuarioIn(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    peso: Optional[float] = None # Peso en kilogramos
    altura: Optional[float] = None # Altura en centímetros
    sexo: Optional[str] = None  # 'masculino' o 'femenino'
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    cuenta_verificada: Optional[bool] = False  # True si el usuario ha verificado su cuenta, False si no
    foto_perfil_url: Optional[str] = None  # URL de la foto de perfil del usuario
    info_fenotipica_completa: Optional[bool] = False  # True si el usuario ha completado su información fenotípica, False si no
    estado_registro: Optional[bool] = True # True si el documento está activo, False si está inactivo

    rutinas: Optional[List[str]] = []  # IDs de rutinas asociadas o creadas por el usuario
    ejercicios_favoritos: Optional[List[str]] = []  # IDs de ejercicios favoritos
    rutinas_favoritas: Optional[List[str]] = []  # IDs de rutinas favoritas

    model_config = {
        'json_schema_extra': {
            'example': {
                'nombre': 'Juan Perez',
                'email': 'juan.perez@example.com',
                'telefono': '0987654321',
                'fecha_nacimiento': '2000-01-01',
                'peso': 70.5,
                'altura': 175.0,
                'sexo': 'masculino',
                'info_fenotipica_completa': False,
                'estado_registro': True,
                'rutinas': ['rutina_1', 'rutina_2'],
                'ejercicios_favoritos': ['ejercicio_1', 'ejercicio_2'],
                'rutinas_favoritas': ['rutina_fav_1']
            }
        }
    }

"""Modelo para leer usuarios"""
class UsuarioOut(UsuarioIn):
    id: str  # ID del documento en Firestore

"""Modelo para el inicio de sesión de usuarios"""
class UsuarioLogin(BaseModel):
    email: str
    contrasenia: str

    model_config = {
        'json_schema_extra': {
            'example': {
                'email': 'juan.perez@example.com',
                'contrasenia': 'Password123'
            }
        }
    }

"""Modelo para el registro de usuarios"""
class UsuarioRegistro(UsuarioIn):
    contrasenia: str  # Contraseña del usuario

    model_config = {
        'json_schema_extra': {
            'example': {
                'nombre': 'Juan Perez',
                'email': 'juan.perez@example.com',
                'contrasenia': 'Password123',
                'telefono': '0987654321',
                'info_fenotipica_completa': False,
                'estado_registro': True,
            }
        }
    }

class UsuarioPatchDatosFenotipicos(BaseModel):
    altura: float = Field(..., gt=0)
    sexo: str = Field(..., min_length=1)
    fecha_nacimiento: datetime
    peso: float = Field(..., gt=0)

    model_config = {
        'json_schema_extra': {
            'example': {
                'altura': 175.5,
                'sexo': 'masculino',
                'fecha_nacimiento': '2005-06-16T16:17:40.768551+00:00',
                'peso': 70.5
            }
        }
    }

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
