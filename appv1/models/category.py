from xmlrpc.client import boolean
from sqlalchemy import Boolean, Column, SmallInteger, String, SMALLINT
from models.base_class import Base

class Category(Base):
    __tablename__ = 'category'
    category_id = Column(SmallInteger, autoincrement=True, primary_key=True)
    category_name= Column(String(50))
    category_description= Column(String(120))
    category_status= Column(Boolean, default=True)




