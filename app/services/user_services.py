from typing import List, Optional
from app.controllers.user_controller import UserController
from app.models.user import UserCreate, UserUpdate

class UserService:
    def __init__(self):
        self.controller = UserController()
    
    def create_user_with_validation(self, session, user_data: UserCreate):
        # Lógica de negocio: validaciones complejas
        if user_data.age < 18:
            raise ValueError("Debe ser mayor de edad")
        
        # Lógica de negocio: procesamiento
        user_data.name = user_data.name.title()
        
        return self.controller.create(session, user_data)
    
    def get_active_users(self, session, filters: dict):
        # Lógica de negocio: filtros complejos
        # Procesamiento de datos
        # Reglas de negocio
        pass