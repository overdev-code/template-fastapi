from typing import List, Dict, Any, Optional
from sqlmodel import Session, select
from app.models.database import engine
from app.models.user import User, UserCreate, UserUpdate

class UserController():

    def create(self, session:Session, user_data: UserCreate) -> UserCreate:
        session.add(user_data)
        session.commit()
        session.refresh(user_data)
        return user_data

    def read_all(self, session:Session, name:str | None, min_age:int | None) -> List[User]:
        statement = select(User)
        conditions = []
        if name:
            conditions.append(User.name == name)
        
        if min_age:
            conditions.append(User.edad >= min_age)

        if conditions:
            statement = statement.where(*conditions) # Aplicar todas las condiciones con AND

        statement = statement.order_by(User.id.desc())  # o por nombre
        users = session.exec(statement).all()
        return users

    def read_one(self, session:Session, user_id: int) -> Optional[User]:
        user = session.get(User, user_id)
        return user

    def update(self, session:Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        user = session.get(User, user_id)
        if not user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(user, key, value)

        session.add(user)
        session.commit()
        session.refresh(user)  # opcional, pero recomendado
        return user

    def delete(self, session:Session, user_id:int) -> bool:
        user = session.get(User, user_id)
        if not user:
            return False
        
        session.delete(user)
        session.commit()
        return user