from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from BaseDatos import SessionLocal, engine, get_db # Base de datos
from ModelosDB import Personaje, Mision, MisionPersonaje # Modelos

app = FastAPI()

# Crear las tablas en la base de datos
from ModelosDB import Base
Base.metadata.create_all(bind=engine)

# Crear nuevo personaje
# RECORDAR : añadir xp
@app.post("/personajes")
def crear_personaje(nombre: str, db: Session = Depends(get_db)):
    personaje = Personaje(nombre=nombre)
    db.add(personaje)
    db.commit()
    db.refresh(personaje)
    return personaje

# Crear nueva mision
@app.post("/misiones")
def crear_mision(nombre: str, descripcion: str, experiencia: int, estado: bool, db: Session = Depends(get_db)):
    mision = Mision(
        nombre=nombre,
        descripcion=descripcion,
        experiencia=experiencia,
        estado=estado,
        fecha_creacion=datetime.timezone.utc
    )
    db.add(mision)
    db.commit()
    db.refresh(mision)
    return mision

# Aceptar mision (encolar)
@app.post("/personajes/{personaje_id}/misiones/{mision_id}")
def aceptar_mision(personaje_id: int, mision_id: int, db: Session = Depends(get_db)):
    personaje = db.query(Personaje).filter_by(id=personaje_id).first()
    mision = db.query(Mision).filter_by(id=mision_id).first()
    
    if not personaje or not mision:
        return {"error": "Personaje o misión no encontrados"}

    personaje.misiones.append(mision)
    db.commit()
    return {"mensaje": "Misión aceptada"}

# Completar mision (desencolar y sumar XP)
@app.post("/personajes/{personaje_id}/completar")
def completar_mision(personaje_id: int, db: Session = Depends(get_db)):
    personaje = db.query(Personaje).filter_by(id=personaje_id).first()
    
    if not personaje or not personaje.misiones:
        return {"error": "No hay misiones para completar"}

    # Sacar la primera misión (FIFO)
    mision = personaje.misiones.pop(0)
    personaje.xp += mision.recompensa_xp

    db.commit()
    return {"mensaje": f"Misión '{mision.descripcion}' completada", "xp_actual": personaje.xp}

# Obtener la lista de misiones en orden
@app.get("/personajes/{personaje_id}/misiones")
def listar_misiones(personaje_id: int, db: Session = Depends(get_db)):
    personaje = db.query(Personaje).filter(Personaje.id == personaje_id).first()
    
    if not personaje:
        return {"error": "Personaje no encontrado"}

    return [mision.descripcion for mision in personaje.misiones]