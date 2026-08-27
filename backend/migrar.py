import sys
import os

# 1. Ajusta os caminhos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 2. Importa apenas o Base e o engine do seu projeto principal
from main import Base

# 3. URLs dos bancos
URL_SQLITE = "sqlite:///escola.db"
URL_POSTGRES = "postgresql://escola_db_stwq_user:0VkDMdnXpsiYJcp31tx8bHRjCqOjR5u2@dpg-da82ve9srm7s73dv0kig-a.oregon-postgres.render.com/escola_db_stwq"

# Conexões
engine_sqlite = create_engine(URL_SQLITE)
engine_postgres = create_engine(URL_POSTGRES)

print("⏳ Criando tabelas no PostgreSQL do Render...")
Base.metadata.create_all(bind=engine_postgres)

print("⏳ Migrando dados das tabelas...")
SessionLocal = sessionmaker(bind=engine_sqlite)
SessionRemote = sessionmaker(bind=engine_postgres)

db_local = SessionLocal()
db_remote = SessionRemote()

try:
    # Percorre automaticamente todas as tabelas registradas na Base
    for mapper in Base.registry.mappers:
        model_class = mapper.class_
        registros = db_local.query(model_class).all()
        print(f"Copiando {len(registros)} registros da tabela '{model_class.__tablename__}'...")
        
        for reg in registros:
            db_remote.merge(reg)
            
    db_remote.commit()
    print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO! Todos os seus dados foram enviados para o Render.")

except Exception as e:
    db_remote.rollback()
    print(f"❌ Ocorreu um erro durante a migração: {e}")

finally:
    db_local.close()
    db_remote.close()