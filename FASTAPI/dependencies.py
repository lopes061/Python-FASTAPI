# Este arquivo contém funções que ajudam na autenticação e acesso ao banco de dados.
# "Dependências" são funções que podem ser usadas em várias rotas para evitar repetição de código.

from fastapi import Depends, HTTPException  # Importa ferramentas para dependências e erros HTTP
from main import SECRET_KEY, ALGORITHM, oauth2_schema  # Importa configurações de segurança
from models import db  # Importa a conexão com o banco de dados
from sqlalchemy.orm import sessionmaker, Session  # Gerencia sessões do banco de dados
from models import Usuario  # Importa o modelo de usuário
from jose import jwt, JWTError  # Usado para criar e verificar tokens JWT

def pegar_sessao():
    """
    Cria uma sessão com o banco de dados para executar comandos SQL.
    Sempre fecha a sessão após o uso.
    """
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    """
    Verifica se o token JWT enviado pelo usuário é válido.
    Se for válido, retorna o usuário correspondente.
    Se não for, retorna erro de acesso negado.
    """
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)  # Decodifica o token
        id_usuario = int(dic_info.get("sub"))  # Extrai o ID do usuário do token
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token")
    # Busca o usuário no banco de dados
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    return usuario