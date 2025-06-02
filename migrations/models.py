from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import declarative_base

Base = declarative_base(metadata=MetaData())

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    correo = Column(String(100))