from fastapi import APIRouter, Depends, HTTPException
from appv1.crud.permissions import get_permissions
from appv1.crud.users import create_user_sql, get_user_by_email, get_all_users, update_user, get_all_users_by_rol, get_all_users_paginated, delete_user, get_user_by_id
from appv1.schemas.user import UserCreate, UserResponse, UserUpdate, PaginatedUsersResponse
from db.database import get_db
from typing import List
from sqlalchemy.orm import Session
from appv1.routers.login import get_current_user


router = APIRouter()
MODULE = 'usuarios'



@router.post("/create")
def insert_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)

):
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if not permisos.p_insert:
        raise HTTPException(status_code=401, detail="usuario no autorizado")
    
    if current_user.user_role != 'SuperAdmin':
        if user.user_role == 'SuperAdmin':
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        
    respuesta = create_user_sql(db, user)
    if respuesta:
        return {"mensaje": "usuario registrado con éxito"}    
   



@router.get("/get-user-by-email/", response_model=UserResponse)
def read_user_by_email(email: str,
                        db: Session = Depends(get_db),
                         current_user: UserResponse = Depends(get_current_user)
                        
):
    
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if current_user.mail != email:
        if not permisos.p_select:
            raise HTTPException(status_code=401, detail="usuario no encontrado")

    usuario = get_user_by_email(db, email)
    if usuario is None:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    return usuario





@router.get("/user/get_all/", response_model=List[UserResponse])
def read_all_users(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    
    permisos = get_permissions(db, current_user.user_role, MODULE)
    if not permisos.p_select:
        raise HTTPException(status_code=401, detail="usuario no autorizado")

    usuarios = get_all_users(db)
    if not usuarios:
        raise HTTPException(status_code=404, detail="No hay usuarios")
    return usuarios

@router.get("/get-user-by-rol/", response_model=List[UserResponse])
def get_all_users_by_rol_endpoint(user_rol: str, db=Depends(get_db)):
    usuarios = get_all_users_by_rol(db, user_rol)
    if not usuarios:
        raise HTTPException(status_code=404, detail="No hay usuarios con ese rol")
    return usuarios



#si un usuario se quiere actualizar a si mismo se puede, si es uno diferente debe mirar si tiene permisos de actualizar - EJERCICIO
@router.put("/update/", response_model=dict)
def update_user_by_id(
    user_id: str, user: UserUpdate, 
     db: Session = Depends(get_db),
                         current_user: UserResponse = Depends(get_current_user)
                        
):
    

    permisos = get_permissions(db, current_user.user_role, MODULE)
    if user_id != current_user.user_id:
        if not permisos.p_update:
            raise HTTPException(status_code=401, detail="usuario no autorizado")
        
    
    verufy_user = get_user_by_id(db, user_id)
    if verufy_user is None:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
   

      
    respuesta = update_user(db, user)
    if respuesta:
        return {"mensaje": "usuario actualizado con éxito"}    
   



# usuarios paginados
@router.get("/users-by-page/", response_model=PaginatedUsersResponse)
def get_all_users_by_page(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    
    users, total_pages = get_all_users_paginated(db, page, page_size)

    return {
        "users": users,
        "total_pages": total_pages,
        "current_page": page,
        "page_size": page_size
    }


@router.delete("/delete/{user_id}", response_model=dict)
def delete_user_by_id(user_id: str, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    result = delete_user(db, user_id)
    if result:
        return {"mensaje": "Usuario eliminado con éxito"}
    

    


#INSERT INTO users (user_id, full_name, mail, passhash, user_role) VALUES ('123312', 'alejo', 'alejo@example.com','12345', 'Admin');