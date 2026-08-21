from typing import List, Optional
from sqlalchemy.orm import Session

from backend.usuario.repository import UsuarioRepository
from backend.usuario.model import Usuario, CargoEnum
from backend.usuario.schema import UsuarioCreateSchema, UsuarioUpdateSchema


class UsuarioService:
    def __init__(self, db: Session):
        self.repository = UsuarioRepository(db)

    def criar_usuario(self, data: UsuarioCreateSchema) -> Usuario:
        if self.repository.obter_por_nome(data.nome_usuario):
            raise ValueError("Nome de usuário já cadastrado.")
        
        # Obs: Aplique o hash da senha (ex: bcrypt/passlib) antes de salvar no banco
        senha_hash = data.senha 

        return self.repository.criar(
            nome_usuario=data.nome_usuario,
            senha_hash=senha_hash,
            cargo=data.cargo
        )

    def listar_usuarios(self) -> List[Usuario]:
        return self.repository.obter_todos()

    def buscar_por_id(self, id_usuario: int) -> Usuario:
        usuario = self.repository.obter_por_id(id_usuario)
        if not usuario:
            raise ValueError(f"Usuário {id_usuario} não encontrado.")
        return usuario

    def atualizar_usuario(self, id_usuario: int, data: UsuarioUpdateSchema) -> Usuario:
        usuario = self.buscar_por_id(id_usuario)

        if data.nome_usuario and data.nome_usuario != usuario.nome_usuario:
            if self.repository.obter_por_nome(data.nome_usuario):
                raise ValueError("Nome de usuário já está em uso.")
            usuario.nome_usuario = data.nome_usuario

        if data.senha:
            usuario.senha = data.senha  # Aplicar hash aqui

        if data.cargo:
            usuario.cargo = data.cargo

        self.repository.db.commit()
        self.repository.db.refresh(usuario)
        return usuario

    def deletar_usuario(self, id_usuario: int) -> None:
        if not self.repository.deletar(id_usuario):
            raise ValueError(f"Usuário {id_usuario} não encontrado.")

    def login(self, nome_usuario: str, senha: str) -> Usuario:
        usuario = self.repository.obter_por_nome(nome_usuario)

        if not usuario:
            raise ValueError("Usuário ou senha incorretos.")

        if usuario.senha != senha:
            raise ValueError("Usuário ou senha incorretos.")

        return usuario