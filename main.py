# instalar fast api

# sqlalchemy, 
# cryptography, 
# pymysql,
#  python-jose,
#  python-dotenv
# pip install passlib

from fastapi import FastAPI

from appv1.routers import users
from fastapi.middleware.cors import CORSMiddleware
from appv1.routers import roles
from appv1.routers import categorys
from appv1.routers import login

from appv1.schemas.user import UserCreate
from appv1.schemas.role import RolCreate
from appv1.schemas.category import CategoryCreate
from core.security import get_hashed_password, verify_password, create_access_token
from db.database import test_db_connection




app = FastAPI()

#incluir router
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(roles.router, prefix="/roles", tags=["roles"])
app.include_router(categorys.router, prefix="/category", tags=["category"])
app.include_router(login.router, prefix="/access", tags=["access"])


# Configuración de CORS para permitir todas las solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Permitir estos métodos HTTP
    allow_headers=["*"],  # Permitir cualquier encabezado en las solicitudes
)







@app.on_event("startup")
def on_startup():
    test_db_connection()


@app.get("/")
async def read_root():
    return {"mensaje": "hola adso 2670586",
            "autor": "brayan alexis",
          
            }


#@app.post("/create-user/")
#def insert_user(usuario: UserCreate):
#    passencriptada = get_hashed_password(usuario.passhash)
#
#    return {
#        "mensaje":"usuario registrado",
#        "id":usuario.user_id,
#        "contraseña":usuario.passhash,
#        "encriptada": passencriptada
#    }
#
#    
#@app.post("/create-rol/")
#def insert_role(role: RolCreate):
#
#    return {
#        "mensaje":"Rol registrado",
#        "nombre":role.rol_name    
#    }
#
#
#@app.post("/create-category/")
#def insert_role(category: CategoryCreate):
#
#    return {
#        "mensaje":"categoria registrado",
#        "nombre":role.rol_name    
#    }