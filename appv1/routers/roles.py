from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from appv1.crud.roles import create_role_sql,get_all_roles
from appv1.schemas.role import RolCreate, RolResponse

from db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/create")
async def insert_role(rol: RolCreate, db: Session = Depends(get_db)):
    respuesta = create_role_sql(db, rol)
    if respuesta:
        return {"mensaje":"Rol regitrado con exito"}
    else:
        return {"mensaje": "Hubo un error al registrar el rol"}
    

    


@router.get("/get-all/", response_model=list[RolResponse])
async def read_all_roles( db: Session = Depends(get_db)):
    rol = get_all_roles(db)
    if len(rol) == 0:
        raise HTTPException(status_code=404, detail="no hay usuarios")
    return rol
  