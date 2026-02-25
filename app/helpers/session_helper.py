# app/dependencies/database.py
from sqlmodel import Session
from app.models.database import engine

def get_session():
    """Dependencia para inyectar sesión de DB en las rutas"""
    with Session(engine) as session:
        yield session