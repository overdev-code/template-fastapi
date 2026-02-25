from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import func
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    age:int

class UserUpdate(BaseModel):
    name: str
    age: int

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(sa_column_kwargs={"server_default": func.now(), "nullable":False})
    updated_at: datetime = Field(sa_column_kwargs={"server_default": func.now(), "nullable":False, "onupdate": func.now()})
    name: str
    age: int
    profile_image_path: Optional[str] = None