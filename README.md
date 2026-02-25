# FastAPI + React Application

Una aplicación web moderna que combina un backend robusto con FastAPI y un frontend dinámico con React.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Ejecución](#ejecución)
- [Desarrollo](#desarrollo)
- [Producción](#producción)
- [Configuración](#configuración)

## ✨ Características

- **Backend**: FastAPI con Python
- **Frontend**: React con componentes modernos
- **Servicio Estático**: Los archivos de React compilados se sirven desde FastAPI
- **Desarrollo Rápido**: Hot reload en modo desarrollo
- **Producción Optimizada**: Archivos compilados y minimizados

## 📦 Requisitos Previos

Asegúrate de tener instalado:

- **Python 3.8+** - [Descargar](https://www.python.org/downloads/)
- **Node.js 14+** - [Descargar](https://nodejs.org/)
- **npm 6+** (incluido con Node.js)
- **pip** - Gestor de paquetes de Python

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <tu-repositorio>
cd react-fastapi
```

### 2. Configurar el Backend (FastAPI)

```bash
# Crear un entorno virtual (recomendado)
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar el Frontend (React)

```bash
# Navegar al directorio del frontend (si existe)
cd frontend
npm install

# Volver al directorio raíz
cd ..
```

## 📁 Estructura del Proyecto

```
react-fastapi/
├── main.py                 # Punto de entrada de la aplicación FastAPI
├── requirements.txt        # Dependencias de Python
├── README.md              # Este archivo
├── __pycache__/           # Cache de Python (ignorar)
├── app/                   # Directorio principal de la aplicación
│   ├── Controllers/       # Lógica de controladores
│   ├── Helpers/          # Funciones auxiliares
│   ├── Models/           # Modelos de datos (Pydantic)
│   └── Routes/           # Definición de rutas de la API
├── react-dist/           # Archivos compilados del frontend (React build)
│   └── ...               # Contenido generado por npm run build
└── frontend/             # Código fuente de React (opcional)
    ├── src/
    ├── public/
    ├── package.json
    └── ...
```

## ▶️ Ejecución

### Modo Desarrollo

#### Opción 1: Ejecutar solo FastAPI

```bash
# Desde el directorio raíz
uvicorn main:app --reload
```

La aplicación estará disponible en: `http://localhost:8000`

- **API**: `http://localhost:8000/api/...`
- **Documentación interactiva**: `http://localhost:8000/docs`
- **Alternativa (ReDoc)**: `http://localhost:8000/redoc`

#### Opción 2: Ejecutar FastAPI + Frontend (recomendado para desarrollo completo)

```bash
# Terminal 1 - Backend
uvicorn main:app --reload

# Terminal 2 - Frontend (si existe servidor de desarrollo de React)
cd frontend
npm start
```

### Modo Producción

#### 1. Compilar React

```bash
cd frontend
npm run build
```

Esto genera la carpeta `dist/` con todos los archivos compilados.

#### 2. Copiar archivos compilados

```bash
# Copiar el contenido de dist/ a react-dist/
cp -r frontend/dist/* react-dist/
```

**IMPORTANTE**: Todo el contenido generado por `npm run build` debe colocarse en la carpeta `react-dist/` para que FastAPI lo sirva correctamente.

#### 3. Ejecutar en producción

```bash
# Desactivar recarga automática para producción
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🛠️ Desarrollo

### Agregar Dependencias de Python

```bash
pip install nombre-del-paquete
pip freeze > requirements.txt
```

### Agregar Dependencias de React (si aplica)

```bash
cd frontend
npm install nombre-del-paquete
```

### Estructura de Controladores (ejemplo)

Los controladores se encuentran en `app/Controllers/` y contienen la lógica de negocio.

### Estructura de Modelos

Los modelos Pydantic en `app/Models/` definen la estructura de datos.

### Rutas de la API

Las rutas se definen en `app/Routes/` y se registran en `main.py`.

## 🔧 Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto (si es necesario):

```env
# Ejemplo
DEBUG=True
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=tu-clave-secreta-aqui
```

### CORS (Si es necesario)

Si necesitas habilitar CORS, asegúrate de configurarlo en `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📝 Notas Importantes

1. **Frontend**: El contenido de `react-dist/` debe ser generado desde React compilado
2. **Hot Reload**: Solo funciona en modo desarrollo con `--reload`
3. **Producción**: Usa un servidor como Gunicorn para mayor estabilidad

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📧 Soporte

Para reportar problemas o sugerencias, abre un issue en el repositorio.