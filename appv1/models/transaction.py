from sqlalchemy import Column, Date, Enum, Float, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from models.base_class import Base


class TransactionType(Enum.Enum):
    revenue = "revenue"
    expenses = "expenses"

class Transaction(Base):
    __tablename__ = 'transactions'
    transactions_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(30), ForeignKey('users.user_id'))
    category_id = Column(Integer, ForeignKey('category.category_id'))
    amount = Column(Float(10,2))
    t_description = Column(String(120))
    t_type = Column(Enum(TransactionType))
    t_date = Column(Date)

    user = relationship("User")
    category  = relationship("Category")
    


