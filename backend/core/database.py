import os
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# 1. Caminho de fallback para SQLite local
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "escola.db"
DEFAULT_SQLITE_URL = f"sqlite:///{DB_PATH}"

# 2. Pega a URL do Postgres das variáveis de ambiente (.env ou Render).
# Se não encontrar nada, usa o SQLite local.
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)

# Trata a compatibilidade de prefixo (alguns provedores enviam 'postgres://' em vez de 'postgresql://')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Configura o engine conforme o banco detectado
engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, echo=False, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()