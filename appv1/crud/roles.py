# Crear un usuario
from sqlalchemy import text

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import IntegrityError
from appv1.schemas.role import RolCreate


def create_role_sql(db: Session, role: RolCreate ):
    try:
        sql_query = text(
            "INSERT INTO roles (rol_name) "
            "VALUES (:rol_name)"
        )
        params = {
            "rol_name": role.rol_name
        }
        db.execute(sql_query, params)
        db.commit()
        return True  # Retorna True si la inserción fue exitosa¿

    except IntegrityError as e:
            db.rollback()  # Revertir la transacción en caso de error de integridad (llave foránea)
            
            if 'Duplicate entry' in str(e.orig):
                if 'PRIMARY' in str(e.orig):
                    raise HTTPException(status_code=400, detail="Error. El nombre  ya está en uso")
                if 'for key \'rol_name\'' in str(e.orig):
                    raise HTTPException(status_code=400, detail="Error. El nombre ya está registrado")
            else:
                raise HTTPException(status_code=400, detail="Error. No hay Integridad de datos al crear el rol")

    except SQLAlchemyError as e:
        db.rollback()  # Revertir la transacción en caso de error de integridad (llave foránea)
        print(f"Error al crear usuario: {e}")
        raise HTTPException(status_code=500, detail="Error al crear rol")
        




## Consultar todos los roles
def get_all_roles(db: Session):
    try:
        sql = text("SELECT * FROM roles")
        result = db.execute(sql).fetchall()
        return result
    
    except SQLAlchemyError as e:
        print(f"Error al buscar roles: {e}")
        raise HTTPException(status_code=500, detail="Error al buscar roles")
