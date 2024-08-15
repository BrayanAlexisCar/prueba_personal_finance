from typing import Annotated
from pydantic import BaseModel, EmailStr, StringConstraints
from datetime import datetime



class CategoryCreate(BaseModel):
   
    category_name: Annotated[str, StringConstraints(max_length=50)]
    category_description:  Annotated[str, StringConstraints(max_length=120)]
    
    
class CategoryResponse(BaseModel):
    category_id: int
    category_name: str
    category_description:  str
    category_status: int
    
