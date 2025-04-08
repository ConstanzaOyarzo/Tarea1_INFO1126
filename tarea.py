from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ColaMisiones(Base):
    def __init__(self):
        self.data = []

    def enqueue(self, mision):
    # Añade una misión al final de la cola.
        self.data.append(mision)

    def dequeue(self):
        # Elimina y retorna la primera misión de la cola.
        if self.is_empty():
            print("La cola está vacía.")
            return None
        return self.data.pop(0)

    def first(self):
        if self.is_empty():
            print("La cola está vacía.")
            return None
        return self.data[0]
    
    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)

class Mision(Base):
    __tablename__ = 'misiones'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(Text, nullable=True)
    experiencia = Column(Integer, default=0)
    estado = Column(Enum('pendiente', 'completada', name='estados'), nullable=False)
    fecha_creacion = Column(DateTime, default=DateTime)

    personajes = relationship("MisionPersonaje", back_populates="mision")

class Personaje(Base):
    __tablename__ = 'personajes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(30), nullable=False)

class MisionPersonaje(Base):
    # Tabla intermedia entre personaje y mision
    
    __tablename__ = 'misiones_personaje'

    personaje_id = Column(Integer, ForeignKey('personajes.id'), primary_key=True)
    mision_id = Column(Integer, ForeignKey('misiones.id'), primary_key=True)
    orden = Column(Integer) # Para el orden FIFO de las misiones

    personajes = relationship("Personaje", back_populates='misiones')
    mision = relationship("Mision", back_populates='personajes')