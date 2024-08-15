from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from fastapi import HTTPException
from core.utils import generate_user_id
from core.security import get_hashed_password
from sqlalchemy.orm import Session



    

# Consultar permisos de un rol por cada modulo
def get_permissions(db: Session, rol: str, module: str):
    try:
        sql = text("SELECT p_select, p_insert, p_update, p_delete FROM permissions  WHERE rol_name = :rol AND module_name = :module")
        result = db.execute(sql, {"rol": rol, "module": module}).fetchone()
        return result
    except SQLAlchemyError as e:
        print(f"Error al obtener permisos : {e}")
        raise HTTPException(status_code=500, detail="Error al obtneer permisso")





# Consultar un usuario por su ID
def get_user_by_id(db: Session, user_id: str):
    sql = text("SELECT * FROM users WHERE user_id = :user_id")
    result = db.execute(sql, {"user_id": user_id}).fetchone()
    return result    

