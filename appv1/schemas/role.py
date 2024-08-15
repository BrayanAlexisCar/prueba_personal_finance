from typing import Annotated
from pydantic import BaseModel, EmailStr, StringConstraints
from datetime import datetime



class RolCreate(BaseModel):
    rol_name: Annotated[str, StringConstraints(max_length=20)]
   


    
    
class RolResponse(BaseModel):
    rol_name: str
  

    