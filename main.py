from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse, HTMLResponse, Response, JSONResponse
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from starlette.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.routes.api_routes import api_router
from app.routes.pages_routes import pages_router
from app.routes.for_react_routes import for_react_router
from app.routes.file_routes import files_router
from app.models.database import create_db_and_tables

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent                     # carpeta de este archivo
DIST_DIR = (BASE_DIR / "react-dist").resolve()          # .../react-fastapi/react-dist

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  # ← Aquí se conecta y crea las tablas en PostgreSQL
    yield

app = FastAPI(title="Sistema de Restaurante", description="API para gestión de pedidos, productos y usuarios", version="1.0.0", lifespan=lifespan)

app.add_middleware(GZipMiddleware, minimum_size=1024)
app.include_router(api_router)
app.include_router(pages_router)
app.include_router(for_react_router)
app.include_router(files_router)

# Descomenta esto solo mientras desarrollas:
app.add_middleware(
    CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# --- Montar carpetas generadas por Vite ---
# Montar assets solo si el directorio existe
assets_dir = DIST_DIR / "assets"
if assets_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

# Montar otros directorios opcionales
for d in ("images", "products"):
    p = DIST_DIR / d
    if p.exists():
        app.mount(f"/{d}", StaticFiles(directory=str(p)), name=d)

# Montar carpeta data/public para archivos dinámicos públicos subidos
data_public_dir = Path("data/public")
if data_public_dir.exists():
    app.mount("/data", StaticFiles(directory=str(data_public_dir)), name="data_public")

def _cache(resp: Response, immutable: bool = False):
    resp.headers["Cache-Control"] = "public, max-age=31536000, immutable" if immutable else "no-cache"

# # --- Home: devuelve index.html ---
# @app.get("/")
# async def home():
#     index_path = DIST_DIR / "index.html"
#     if not index_path.exists():
#         return JSONResponse({"error": f"Falta {index_path}. Ejecuta `npm run build`."}, status_code=500)
#     return FileResponse(index_path, headers={"Cache-Control": "no-cache"})

# --- Fallback SPA (AL FINAL) ---
@app.get("/{full_path:path}", include_in_schema=False)
async def spa_fallback_react(full_path: str):
    # Si no hay path, servir index.html
    print("full_path", full_path)
    candidate = DIST_DIR / full_path
    if candidate.is_file():                           # sirve archivos reales (p.ej. /vite.svg)
        return FileResponse(candidate)
    return FileResponse(DIST_DIR / "index.html")      # rutas del SPA -> index.html
