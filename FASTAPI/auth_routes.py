# Este arquivo define as rotas de autenticação (login, cadastro, refresh de token).
# "Rotas" são caminhos da API que executam funções específicas.

from fastapi import APIRouter, Depends, HTTPException  # Ferramentas para criar rotas e tratar erros
from models import Usuario  # Modelo de usuário
from dependencies import pegar_sessao, verificar_token  # Funções auxiliares para banco e autenticação
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY  # Configurações de segurança
from schemas import UsuarioSchema, LoginSchema  # Esquemas para validar dados recebidos
from sqlalchemy.orm import Session  # Sessão do banco de dados
from jose import jwt, JWTError  # Ferramentas para criar/verificar tokens JWT
from datetime import datetime, timedelta, timezone  # Manipulação de datas
from fastapi.security import OAuth2PasswordRequestForm  # Validação de login via formulário

# Cria um grupo de rotas com prefixo "/auth"
auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    """
    Cria um token JWT para autenticação do usuário.
    O token inclui o ID do usuário e a data de expiração.
    """
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado

def autenticar_usuario(email, senha, session):
    """
    Verifica se o usuário existe e se a senha está correta.
    Retorna o usuário se autenticado, senão retorna False.
    """
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

@auth_router.get("/")
async def home():
    """
    Rota padrão de autenticação.
    Apenas retorna uma mensagem informando que está na rota de autenticação.
    """
    return {"mensagem": "Você acessou a rota padrão de autenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    """
    Cria uma nova conta de usuário.
    Verifica se o e-mail já existe, senão salva o novo usuário no banco de dados.
    """
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        # Já existe um usuário com esse email
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"usuário cadastrado com sucesso {usuario_schema.email}"}

# login -> email e senha -> token JWT (Json Web Token)
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    """
    Realiza o login do usuário.
    Se o usuário e senha estiverem corretos, retorna um token JWT de acesso e um de refresh.
    """
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
            }
    
@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    """
    Realiza login usando formulário padrão OAuth2.
    Retorna um token JWT se o login for bem-sucedido.
    """
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
            }

@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    """
    Gera um novo token de acesso usando o token atual (refresh).
    """
    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
        }