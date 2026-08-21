from typing import List, Optional
from sqlalchemy.orm import Session

from backend.usuario.model import Usuario, CargoEnum


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, nome_usuario: str, senha_hash: str, cargo: CargoEnum) -> Usuario:
        usuario = Usuario(
            nome_usuario=nome_usuario,
            senha=senha_hash,
            cargo=cargo,
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def obter_todos(self) -> List[Usuario]:
        return self.db.query(Usuario).order_by(Usuario.nome_usuario).all()

    def obter_por_id(self, id_usuario: int) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    def obter_por_nome(self, nome_usuario: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.nome_usuario == nome_usuario).first()

    def deletar(self, id_usuario: int) -> bool:
        usuario = self.obter_por_id(id_usuario)
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False