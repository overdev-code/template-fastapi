from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from pathlib import Path
import os
from sqlmodel import Session
from app.models.database import get_session

files_router = APIRouter(prefix="/files", tags=["files"])

DATA_DIR = Path("data")

@files_router.get("/public/{file_path:path}")
async def get_public_file(file_path: str):
    """
    Sirve archivos públicos de data/public (alternativa al montaje directo)
    """
    file_location = DATA_DIR / "public" / file_path
    
    if not file_location.exists():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    content_type = "application/octet-stream"
    if file_path.lower().endswith(('.jpg', '.jpeg')):
        content_type = "image/jpeg"
    elif file_path.lower().endswith('.png'):
        content_type = "image/png"
    elif file_path.lower().endswith('.pdf'):
        content_type = "application/pdf"
    
    return FileResponse(
        path=str(file_location),
        media_type=content_type,
        filename=file_location.name
    )

@files_router.get("/private/{file_path:path}")
async def get_private_file(file_path: str, session: Session = Depends(get_session)):
    """
    Sirve archivos privados de data/private (requiere autenticación/validación)
    """
    # Aquí puedes añadir lógica de autenticación
    # Ejemplo: verificar si el usuario tiene permiso para acceder a este archivo
    
    file_location = DATA_DIR / "private" / file_path
    
    if not file_location.exists():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    # Validar que esté dentro de data/private (seguridad)
    try:
        file_location.resolve().relative_to((DATA_DIR / "private").resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    content_type = "application/octet-stream"
    if file_path.lower().endswith(('.jpg', '.jpeg')):
        content_type = "image/jpeg"
    elif file_path.lower().endswith('.png'):
        content_type = "image/png"
    elif file_path.lower().endswith('.pdf'):
        content_type = "application/pdf"
    
    return FileResponse(
        path=str(file_location),
        media_type=content_type,
        filename=file_location.name
    )
