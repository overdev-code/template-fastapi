from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlmodel import Session
from app.models.database import get_session
from app.controllers.user_controller import UserController

pages_router = APIRouter(include_in_schema=False)
BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(directory=str(BASE_DIR / "views" / "templates")) 

@pages_router.get("/incio")
async def home(request: Request):
    return templates.TemplateResponse("app/index.html", {"request": request})

@pages_router.get("/login")
async def login(request: Request):
    
    return templates.TemplateResponse("app/login.html", {"request": request})

@pages_router.post("/login")
async def login(
    request: Request, 
    session: Session = Depends(get_session),
    user_sol: str = Form(...),
    clave_sol: str = Form(...)
):
    try:
        
        # Validar que se recibieron los datos
        if not user_sol or not clave_sol:
            return {"success": False, "message": "Por favor complete todos los campos"}
        
        # Usar el método authenticate del UserController
        controller = UserController()
        user = controller.authenticate(session, user_sol, clave_sol)
        
        if user:
            # Login exitoso - guardar user_id en sesión
            request.session["user_id"] = user.id
            request.session["user_sol"] = user.user_sol
            request.session["first_name"] = user.first_name
            request.session["user_level"] = user.user_level
            return {
                "success": True, 
                "message": "Login successful",
                "user_id": user.id,
                "first_name": user.first_name,
                "user_sol": user.user_sol,
                "user_level": user.user_level
            }
        else:
            return {
                "success": False, 
                "message": "Credenciales incorrectas"
            }
            
    except Exception as e:
        print(f"=== ERROR EN LOGIN: {str(e)} ===")
        return {
            "success": False, 
            "message": "Error en el servidor. Intente nuevamente."
        }