from backend.core.database import engine
from sqlalchemy import text

with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE reunioes, bloqueios_agenda, usuarios RESTART IDENTITY CASCADE"))
    print("RESET_OK")
    print("USERS_COUNT", conn.execute(text("SELECT COUNT(*) FROM usuarios")).scalar())
    print("REUNIOES_COUNT", conn.execute(text("SELECT COUNT(*) FROM reunioes")).scalar())
    print("BLOQUEIOS_COUNT", conn.execute(text("SELECT COUNT(*) FROM bloqueios_agenda")).scalar())
