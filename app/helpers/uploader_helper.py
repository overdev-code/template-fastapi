import os
import uuid
from typing import List, Optional
from fastapi import UploadFile, HTTPException
from pathlib import Path

class FileUploader:
    """
    Uso ejemplo en una ruta FastAPI:
    async def upload_route(files: List[UploadFile] = File(...)):
        uploader = FileUploader()
        paths = await uploader.imagesUpload(files, custom_path="custom/images")
        return {"saved_paths": paths}
    """

    # Configuraciones por defecto
    DEFAULT_BASE_PATH = "react-dist/static/files"
    ALLOWED_EXTENSIONS = {
        "images": {"jpg", "jpeg", "png", "gif", "webp"},
        "docs": {"pdf", "doc", "docx", "txt", "md"},
        "any": set()  # Sin restricción para anyUpload
    }
    MAX_FILE_SIZE_MB = 5  # Máximo 5MB por archivo (ajustable)
    MAX_FILES = 10  # Máximo 10 archivos en subida múltiple

    def __init__(self, max_size_mb: int = MAX_FILE_SIZE_MB, max_files: int = MAX_FILES):
        self.max_size_mb = max_size_mb
        self.max_files = max_files

    async def _upload_single(self, file: UploadFile, save_dir: Path) -> str:
        """
        Sube un solo archivo de forma segura.
        """
        # Validar tamaño
        contents = await file.read()
        if len(contents) > self.max_size_mb * 1024 * 1024:
            raise HTTPException(status_code=400, detail=f"Archivo demasiado grande (máx {self.max_size_mb}MB)")

        # Generar nombre único seguro
        file_extension = file.filename.split(".")[-1].lower()
        filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = save_dir / filename

        # Crear directorio si no existe
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Guardar
        with open(file_path, "wb") as f:
            f.write(contents)

        # Devolver ruta relativa (para servir con StaticFiles)
        # return str(file_path.relative_to(self.DEFAULT_BASE_PATH))
        relative_path = file_path.relative_to(Path(self.DEFAULT_BASE_PATH))
        return relative_path.as_posix()  # ← Ahora devuelve "images/uuid.png"

    async def _upload_files(
        self,
        files: UploadFile | List[UploadFile],
        default_subpath: str,
        custom_path: Optional[str] = None,
        allowed_extensions: Optional[set] = None
    ) -> List[str]:
        """
        Método interno para subir uno o múltiples archivos.
        """
        # Convertir a lista si es un solo archivo
        if not isinstance(files, list):
            files = [files]

        # Validar cantidad
        if len(files) > self.max_files:
            raise HTTPException(status_code=400, detail=f"Demasiados archivos (máx {self.max_files})")

        # Ruta de guardado
        base_path = Path(self.DEFAULT_BASE_PATH)
        subpath = Path(custom_path) if custom_path else Path(default_subpath)
        save_dir = base_path / subpath

        saved_paths = []

        for file in files:
            if file.filename == '':  # Skip si no se envió archivo
                continue

            # Validar extensión si aplica
            ext = file.filename.split(".")[-1].lower()
            if allowed_extensions and ext not in allowed_extensions:
                raise HTTPException(status_code=400, detail=f"Extensión no permitida: {ext}")

            # Validar tipo de contenido (MIME)
            if "image" in default_subpath and not file.content_type.startswith("image/"):
                raise HTTPException(status_code=400, detail="Archivo no es una imagen válida")

            # Subir y agregar ruta
            path = await self._upload_single(file, save_dir)
            saved_paths.append(path)

        return saved_paths

    async def imagesUpload(
        self,
        files: UploadFile | List[UploadFile],
        custom_path: Optional[str] = None
    ) -> List[str]:
        """
        Sube una o múltiples imágenes.
        Default: static/files/images
        """
        return await self._upload_files(files, "images", custom_path, self.ALLOWED_EXTENSIONS["images"])

    async def docsUpload(
        self,
        files: UploadFile | List[UploadFile],
        custom_path: Optional[str] = None
    ) -> List[str]:
        """
        Sube uno o múltiples documentos (pdf, doc, etc.).
        Default: static/files/docs
        """
        return await self._upload_files(files, "docs", custom_path, self.ALLOWED_EXTENSIONS["docs"])

    async def anyUpload(
        self,
        files: UploadFile | List[UploadFile],
        custom_path: Optional[str] = None
    ) -> List[str]:
        """
        Sube cualquier tipo de archivo (sin restricción de extensión).
        Default: static/files/any
        """
        return await self._upload_files(files, "any", custom_path)