from sqlmodel import create_engine, SQLModel

# Reemplaza con tus datos reales de PostgreSQL
DATABASE_URL = "postgresql://root:root@localhost:5432/db_store"

engine = create_engine(DATABASE_URL, echo=True)  # echo=True para ver las consultas SQL en consola (útil en desarrollo)


def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    # Importar en orden correcto para evitar errores de FK
    # Primero las tablas que no dependen de otras
    from app.models import user
    
    # Luego las tablas que tienen FK a las anteriores
    
    SQLModel.metadata.create_all(engine)