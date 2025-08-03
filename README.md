# 🔥 Dragon Forge API REST

API REST para gestión de ejercicios, rutinas y usuarios de una aplicación de fitness desarrollada con FastAPI y Firebase Firestore.

## ✨ Características

- ✅ **CRUD completo** para Ejercicios, Rutinas y Usuarios
- 🔍 **Filtrado avanzado** con múltiples parámetros
- 🔐 **Autenticación** con Firebase Auth
- 📊 **Soft delete** para mantenimiento de datos
- 📝 **Documentación automática** con Swagger/OpenAPI
- 🚀 **Actualización parcial** con endpoints PATCH
- 🎯 **Validación de datos** con Pydantic

## 🛠 Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **Firebase Firestore** - Base de datos NoSQL
- **Firebase Auth** - Sistema de autenticación
- **Pydantic** - Validación de datos
- **Python 3.8+**

## 📝 Aplicativo en producción

El aplicativo se encuentra operativo en la plataforma Render, donde se puede acceder por medio de los siguientes enlaces:

- [Aplicativo en render](https://api-rest-dragon-forge.onrender.com)
- [Documentación Interactiva](https://api-rest-dragon-forge.onrender.com/docs)

***Nota:** puede que tarde en inicializar unos 30 segundos, debido a que debe inicializarse el servidor de render.*

## 🚀 Instalación

En caso de que se requiera utilizar el código para uso personal, se recomienda seguir los siguientes pasos.

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/api-rest-dragon-forge.git
cd api-rest-dragon-forge
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Firebase

- Crear proyecto en [Firebase Console](https://console.firebase.google.com/)
- Descargar archivo de configuración `serviceAccountKey.json`
- Colocar en la raíz del proyecto

## ⚙️ Configuración

### 1. Variables de entorno

```bash
# .env
FIREBASE_PROJECT_ID=tu-proyecto-id
FIREBASE_PRIVATE_KEY_ID=tu-private-key-id
FIREBASE_PRIVATE_KEY=tu-private-key
FIREBASE_CLIENT_EMAIL=tu-client-email
```

### 2. Inicializar Firebase

```python
# app/init_firebase.py ya configurado
```

## 🎯 Uso

### Desarrollo

```bash
python run_dev.py
```

### Producción

```bash
uvicorn app.app:app --host 0.0.0.0 --port 8000
```

**Base URL:** `http://localhost:8000/api/v1`  
**Documentación:** `http://localhost:8000/docs`

## 📚 Endpoints

### 🏋️ Ejercicios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/ejercicios/` | Obtener todos los ejercicios (con filtros) |
| `GET` | `/ejercicios/{id}` | Obtener ejercicio por ID |
| `GET` | `/ejercicios/destacados/` | Obtener ejercicios destacados |
| `POST` | `/ejercicios/` | Crear nuevo ejercicio |
| `PUT` | `/ejercicios/{id}` | Actualizar ejercicio completo |
| `PATCH` | `/ejercicios/{id}` | Actualizar ejercicio parcial |
| `PUT` | `/ejercicios/{id}/eliminar` | Marcar como inactivo |
| `PUT` | `/ejercicios/{id}/recuperar` | Marcar como activo |
| `DELETE` | `/ejercicios/{id}` | Eliminar permanentemente |

#### Filtros disponibles

- `dificultad`: Filtrar por nivel de dificultad
- `equipamiento`: Filtrar por equipamiento necesario
- `grupo_muscular`: Filtrar por grupos musculares

### 📋 Rutinas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/rutinas/` | Obtener todas las rutinas |
| `GET` | `/rutinas/{id}` | Obtener rutina por ID |
| `POST` | `/rutinas/` | Crear nueva rutina |
| `PUT` | `/rutinas/{id}` | Actualizar rutina completa |
| `PATCH` | `/rutinas/{id}` | Actualizar rutina parcial |
| `PUT` | `/rutinas/{id}/eliminar` | Marcar como inactiva |
| `PUT` | `/rutinas/{id}/recuperar` | Marcar como activa |
| `DELETE` | `/rutinas/{id}` | Eliminar permanentemente |

### 👤 Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/usuarios/` | Obtener todos los usuarios |
| `GET` | `/usuarios/{id}` | Obtener usuario por ID |
| `POST` | `/usuarios/` | Registrar nuevo usuario |
| `POST` | `/usuarios/login` | Iniciar sesión |
| `PUT` | `/usuarios/{id}` | Actualizar usuario completo |
| `PATCH` | `/usuarios/{id}` | Actualizar usuario parcial |
| `PATCH` | `/usuarios/{id}/fenotipo` | Actualizar datos físicos |
| `PATCH` | `/usuarios/{id}/info` | Actualizar información personal |

## 📊 Modelos de Datos

### Ejercicio

```json
{
  "id": "string",
  "nombre": "string",
  "grupo_muscular": ["string"],
  "dificultad": "string",
  "instrucciones": "string",
  "equipamiento": ["string"],
  "destacado": "boolean",
  "imagen_url": "string",
  "estado_registro": "boolean",
  "fecha_creacion": "datetime",
  "fecha_actualizacion": "datetime"
}
```

### Rutina

```json
{
  "id": "string",
  "nombre": "string",
  "descripcion": "string",
  "ejercicios": [
    {
      "ejercicio_id": "string",
      "series": "integer",
      "repeticiones": "integer",
      "descanso_segundos": "integer"
    }
  ],
  "estado_registro": "boolean",
  "fecha_creacion": "datetime",
  "fecha_actualizacion": "datetime"
}
```

### Usuario

```json
{
  "id": "string",
  "nombre": "string",
  "email": "string",
  "telefono": "string",
  "altura": "float",
  "peso": "float",
  "sexo": "string",
  "fecha_nacimiento": "datetime",
  "foto_perfil_url": "string",
  "info_fenotipica_completa": "boolean",
  "estado_registro": "boolean",
  "fecha_creacion": "datetime",
  "fecha_actualizacion": "datetime"
}
```

## 🔢 Códigos de Estado

| Código | Descripción |
|--------|-------------|
| `200` | ✅ Operación exitosa |
| `201` | ✅ Recurso creado |
| `204` | ✅ Operación exitosa sin contenido |
| `400` | ❌ Error en petición |
| `401` | ❌ No autorizado |
| `404` | ❌ Recurso no encontrado |
| `500` | ❌ Error interno del servidor |

## 📝 Ejemplos de Uso

### Crear un ejercicio

```bash
curl -X POST "http://localhost:8000/api/v1/ejercicios/" \
     -H "Content-Type: application/json" \
     -d '{
       "nombre": "Flexiones de brazos",
       "grupo_muscular": ["Pecho", "Tríceps"],
       "dificultad": "Intermedio",
       "instrucciones": "Coloca las manos en el suelo...",
       "equipamiento": ["Colchoneta"]
     }'
```

### Filtrar ejercicios

```bash
# Por dificultad
curl "http://localhost:8000/api/v1/ejercicios/?dificultad=Intermedio"

# Por múltiples filtros
curl "http://localhost:8000/api/v1/ejercicios/?dificultad=Avanzado&grupo_muscular=Pecho"
```

### Actualización parcial

```bash
curl -X PATCH "http://localhost:8000/api/v1/ejercicios/123" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Nuevo nombre"}'
```

### Registrar usuario

```bash
curl -X POST "http://localhost:8000/api/v1/usuarios/" \
     -H "Content-Type: application/json" \
     -d '{
       "nombre": "Juan Pérez",
       "email": "juan@example.com",
       "password": "password123",
       "telefono": "+123456789"
     }'
```

### Actualizar datos fenotípicos

```bash
curl -X PATCH "http://localhost:8000/api/v1/usuarios/123/fenotipo" \
     -H "Content-Type: application/json" \
     -d '{
       "altura": 175.5,
       "peso": 70.0,
       "sexo": "M",
       "fecha_nacimiento": "1990-01-01T00:00:00"
     }'
```

## 🚦 Estados de Respuesta

### Éxito

```json
{
  "mensaje": "Operación exitosa",
  "id": "documento_id"
}
```

### Error

```json
{
  "detail": "Descripción del error"
}
```

## 🔧 Configuración de Firebase

1. **Crear proyecto** en Firebase Console
2. **Habilitar Firestore** Database
3. **Configurar reglas** de seguridad:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true; // Ajustar según necesidades
    }
  }
}
```

## 📁 Estructura del Proyecto

```bash
api-rest-dragon-forge/
├── app/
│   ├── __init__.py
│   ├── app.py                 # Aplicación principal
│   ├── models.py              # Modelos Pydantic
│   ├── firestore_db.py        # Operaciones de base de datos
│   ├── init_firebase.py       # Configuración Firebase
│   ├── models/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── ejercicios.py      # Rutas de ejercicios
│   │   ├── rutinas.py         # Rutas de rutinas
│   │   └── usuarios.py        # Rutas de usuarios
│   └── services/
│       ├── ejercicio_service.py
├── run_dev.py                 # Script de desarrollo
├── requirements.txt           # Dependencias
└── README.md                  # Documentación
```
