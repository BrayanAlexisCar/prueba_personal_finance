# Crear un usuario
from sqlalchemy import text

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import IntegrityError
from appv1.schemas.category import CategoryCreate
from core.utils import generate_user_id


def create_category_sql(db: Session, category: CategoryCreate ):
    try:
        sql_query = text(
            "INSERT INTO category (category_id, category_name, category_description ) "
            "VALUES (:category_id, :category_name, :category_description)"
        )
        params = {
            "category_id": generate_user_id(),
            "category_name": category.category_name,
            "category_description": category.category_description,
        }
        db.execute(sql_query, params)
        db.commit()
        return True  # Retorna True si la inserción fue exitosa¿

    except IntegrityError as e:
            db.rollback()  # Revertir la transacción en caso de error de integridad (llave foránea)
            
            if 'Duplicate entry' in str(e.orig):
                if 'PRIMARY' in str(e.orig):
                    raise HTTPException(status_code=400, detail="Error. El id  ya está en uso")
                if 'for key \'category_name\'' in str(e.orig):
                    raise HTTPException(status_code=400, detail="Error. El nombre ya está registrado")
            else:
                raise HTTPException(status_code=400, detail="Error. No hay Integridad de datos al crear categoria")

    except SQLAlchemyError as e:
        db.rollback()  # Revertir la transacción en caso de error de integridad (llave foránea)
        print(f"Error al crear la categoria: {e}")
        raise HTTPException(status_code=500, detail="Error al crear la categoria")
        


    
# Consultar una categoria por su nombre 
def get_category_by_name(db: Session, category_name: str):
    try:
        sql = text("SELECT * FROM category WHERE category_name = :category_name")
        result = db.execute(sql, {"category_name": category_name}).fetchone()
        return result
    
    except SQLAlchemyError as e:
        print(f"Error al buscar categoria por nombre: {e}")
        raise HTTPException(status_code=500, detail="Error al buscar categoria por nombre")
    