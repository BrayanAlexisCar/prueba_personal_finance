from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from appv1.crud.categorys import create_category_sql, get_category_by_name
from appv1.schemas.category import CategoryCreate, CategoryResponse

from db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/create")
async def insert_category(category: CategoryCreate, db: Session = Depends(get_db)):
    respuesta = create_category_sql(db, category)
    if respuesta:
        return {"mensaje":"Categoria registrada con exito"}
    else:
        return {"mensaje": "Hubo un error al registrar la Categoria"}
    

    

  
@router.get("/get-category-by-name/", response_model=CategoryResponse)
async def read_category_by_name(nombre: str, db: Session = Depends(get_db)):
    categoria = get_category_by_name(db, nombre)
    if categoria is None:
        raise HTTPException(status_code=404, detail="categoria  no encontrado")
    return categoria

