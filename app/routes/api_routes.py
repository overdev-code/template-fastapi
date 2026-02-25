from fastapi import APIRouter, Depends, Request, Response, UploadFile, File, Form
from sqlmodel import Session
from typing import List, Optional
from app.controllers.user_controller import UserController
from app.helpers.session_helper import get_session
from app.models.user import User, UserCreate, UserUpdate
from app.helpers.uploader_helper import FileUploader

api_router = APIRouter(prefix="/api/v1", tags=["users"])
userController = UserController()

@api_router.post("/create")
async def create_user(name:str = Form(None), age:int = Form(None), profile_image:Optional[UploadFile] = File(None), session: Session=Depends(get_session)):
    uploader = FileUploader()
    paths = await uploader.imagesUpload(profile_image)
    profile_image_path = paths[0] if len(paths) >=0  else None

    user_to_save = User(name=name, age=age, profile_image_path=profile_image_path)

    data_response = userController.create(session=session, user_data=user_to_save)
    return data_response

@api_router.get("/read")
async def get_users(session:Session=Depends(get_session), skip: int = 0, limit: int = 100, name:str | None = None, min_age:int | None = None):
    response_user = userController.read_all(session=session, name=name, min_age=min_age)
    return response_user

@api_router.get("/read/{user_id}")
async def get_user(session:Session=Depends(get_session), user_id: int=0):
    response_user = userController.read_one(session=session, user_id=user_id)
    return response_user

@api_router.put("/update/{user_id}")
async def update_user(user_id:int, user_update: UserUpdate, session:Session=Depends(get_session)):
    data_response = userController.update(session=session, user_id=user_id, user_update=user_update)
    return data_response

@api_router.delete("/delete/{user_id}")
async def delete_user(user_id: int, session:Session=Depends(get_session)):
    data_response = userController.delete(session=session, user_id=user_id)
    return data_response






