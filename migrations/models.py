from sqlalchemy import Column, Integer, String, MetaData, BigInteger, Text, Date, Float, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base(metadata=MetaData())

class Agente(Base):
    __tablename__ = 'agentes'

    index = Column(BigInteger, primary_key=True, autoincrement=True)
    pk_agente = Column(Text, nullable=True)
    actividad = Column(String, nullable=True)
    estado = Column(String, nullable=True)
    fecha_actual = Column(Date, nullable=True)


class DemandaReal(Base):
    __tablename__ = 'demanda_real'

    index = Column(BigInteger, primary_key=True, autoincrement=True)
    id_demanda_re = Column(Text, nullable=True)
    pk_agente = Column(Text, nullable=True)
    fecha = Column(Date, nullable=True)
    hora = Column(Integer, nullable=True)
    demanda_rea = Column(Float, nullable=True)
    fecha_actuali = Column(Date, nullable=True)


class Generacion(Base):
    __tablename__ = 'generacion'

    index = Column(BigInteger, primary_key=True, autoincrement=True)
    pk_recurso = Column(Text, nullable=True)
    fecha = Column(TIMESTAMP, nullable=True)
    hora = Column(Integer, nullable=True)
    generacion = Column(Float, nullable=True)
    fecha_actuali = Column(Date, nullable=True)

class Recurso(Base):
    __tablename__ = 'recursos'

    index = Column(BigInteger, primary_key=True, autoincrement=True)
    pk_recurso = Column(Text, nullable=True)
    pk_agente = Column(Text, nullable=True)
    nombre_recurso = Column(Text, nullable=True)
    tipo_recurso = Column(Text, nullable=True)
    fecha_actuali = Column(Date, nullable=True)

class TemperaturaSolar(Base):
    __tablename__ = 'temperatura_solar'

    index = Column(BigInteger, primary_key=True, autoincrement=True)
    pk_recurso = Column(Text, nullable=True)
    fecha = Column(TIMESTAMP, nullable=True)
    temperatura = Column(Float, nullable=True)
    fecha_actuali = Column(Date, nullable=True)