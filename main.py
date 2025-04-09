from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from BaseDatos import SessionLocal, engine
from ModelosDB import Personaje, Mision, Base

app = FastAPI()

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Dependencia de sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/personajes")
def crear_personaje(nombre: str, db: Session = Depends(get_db)):
    personaje = Personaje(nombre=nombre)
    db.add(personaje)
    db.commit()
    db.refresh(personaje)
    return personaje

@app.post("/misiones")
def crear_mision(descripcion: str, recompensa_xp: int, db: Session = Depends(get_db)):
    mision = Mision(descripcion=descripcion, recompensa_xp=recompensa_xp)
    db.add(mision)
    db.commit()
    db.refresh(mision)
    return mision

@app.post("/personajes/{personaje_id}/misiones/{mision_id}")
def aceptar_mision(personaje_id: int, mision_id: int, db: Session = Depends(get_db)):
    personaje = db.query(Personaje).filter(Personaje.id == personaje_id).first()
    mision = db.query(Mision).filter(Mision.id == mision_id).first()
    
    if not personaje or not mision:
        return {"error": "Personaje o misión no encontrados"}

    personaje.misiones.append(mision)
    db.commit()
    return {"mensaje": "Misión aceptada"}

@app.post("/personajes/{personaje_id}/completar")
def completar_mision(personaje_id: int, db: Session = Depends(get_db)):
    personaje = db.query(Personaje).filter(Personaje.id == personaje_id).first()
    
    if not personaje or not personaje.misiones:
        return {"error": "No hay misiones para completar"}

    # Sacar la primera misión (FIFO)
    mision = personaje.misiones.pop(0)
    personaje.xp += mision.recompensa_xp

    db.commit()
    return {"mensaje": f"Misión '{mision.descripcion}' completada", "xp_actual": personaje.xp}

@app.get("/personajes/{personaje_id}/misiones")
def listar_misiones(personaje_id: int, db: Session = Depends(get_db)):
    personaje = db.query(Personaje).filter(Personaje.id == personaje_id).first()
    
    if not personaje:
        return {"error": "Personaje no encontrado"}

    return [mision.descripcion for mision in personaje.misiones]