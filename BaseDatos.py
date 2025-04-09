from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# URL de la base de datos
DATABASE_URL = "sqlite:///./misionesRPG.db"

# Crear la conexión al motor
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crear la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definir la base para los modelos de SQLAlchemy
Base = declarative_base()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
