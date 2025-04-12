import os
import uuid
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Float
from sqlalchemy.types import Enum


# Caminho do diretório onde está o arquivo database.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho para o arquivo do banco de dados SQLite dentro da pasta 'banco_de_dados'
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'ima.db')}"

# Criar engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Criar uma base para a definição das classes do modelo
Base = declarative_base()

# Criar uma SessionLocal para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modelo de dados (Tabela)
class Ima(Base):
    __tablename__ = "imas"

    ima_id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    medida = Column(String(50), nullable=False)
    formato = Column(String, nullable=False)
    forca_N = Column(Enum('N35', 'N42', 'N50', 'N52', name="forca_types"), nullable=False)
    preco = Column(Float, nullable=False)

# Inicializar o banco de dados
def init_db():
    Base.metadata.create_all(bind=engine)