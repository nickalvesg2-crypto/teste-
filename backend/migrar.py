import sqlite3

conn = sqlite3.connect("backend/escola.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE reunioes RENAME TO reunioes_antiga;")

    cursor.execute("""
    CREATE TABLE reunioes (
        id_reuniao INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno VARCHAR(150) NOT NULL,
        responsavel VARCHAR(150) NOT NULL DEFAULT '',
        turma VARCHAR(50) NOT NULL,
        data_dia DATE NOT NULL,
        hora_inicio TIME NOT NULL,
        hora_fim TIME NOT NULL,
        solicitado_por_id INTEGER NOT NULL DEFAULT 1,
        destinatario_id INTEGER,
        status VARCHAR(24) NOT NULL,
        motivo_reagendamento TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        FOREIGN KEY (solicitado_por_id) REFERENCES usuarios (id_usuario) ON DELETE RESTRICT,
        FOREIGN KEY (destinatario_id) REFERENCES usuarios (id_usuario) ON DELETE RESTRICT
    );
    """)

    cursor.execute("""
    INSERT INTO reunioes (
        id_reuniao, aluno, responsavel, turma, data_dia,
        hora_inicio, hora_fim, solicitado_por_id, destinatario_id,
        status, motivo_reagendamento
    )
    SELECT 
        id_reuniao,
        aluno,
        '' AS responsavel,
        turma,
        data_dia,
        hora_inicio,
        hora_fim,
        1 AS solicitado_por_id,
        NULL AS destinatario_id,
        status,
        motivo_reagendamento
    FROM reunioes_antiga;
    """)

    cursor.execute("DROP TABLE reunioes_antiga;")
    conn.commit()
    print("✅ Banco antigo adaptado para o novo esquema com sucesso!")

except Exception as e:
    conn.rollback()
    print(f"❌ Erro na migração: {e}")
finally:
    conn.close()