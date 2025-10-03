# importamos paquetes de sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# url de la base de datos (MySQL)

database_url = "mysql+mysqlconnector://root:@localhost:3306/biblioteca"

# motor de sqlAlchemy
engine = create_engine(database_url)

# sesion local para obtener sesiones de DB

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# clase base para los modelos de la DB

class Base(DeclarativeBase):
    pass