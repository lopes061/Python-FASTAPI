# Este arquivo é o ponto de entrada da aplicação FastAPI.
# FastAPI é um framework moderno para criar APIs web em Python.
# Uma API REST permite que diferentes sistemas troquem informações usando métodos HTTP (GET, POST, PUT, DELETE).

from fastapi import FastAPI  # Importa o FastAPI para criar a aplicação web
from passlib.context import CryptContext  # Usado para criptografar senhas
from fastapi.security import OAuth2PasswordBearer  # Gerencia autenticação via token
from dotenv import load_dotenv  # Carrega variáveis de ambiente de um arquivo .env
import os  # Permite acessar variáveis do sistema operacional

load_dotenv()  # Carrega as variáveis do arquivo .env

# Variáveis de configuração para autenticação e segurança
SECRET_KEY = os.getenv("SECRET_KEY")  # Chave secreta usada para criar tokens
ALGORITHM = os.getenv("ALGORITHM")  # Algoritmo usado para criptografia dos tokens
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))  # Tempo de expiração do token

app = FastAPI()  # Cria a aplicação FastAPI

# Configuração para criptografia de senhas usando bcrypt
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Configuração do esquema de autenticação OAuth2 (token JWT)
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

# Importa as rotas de autenticação e pedidos
from auth_routes import auth_router
from order_routes import order_router

# Adiciona as rotas de autenticação e pedidos à aplicação
app.include_router(auth_router)
app.include_router(order_router)

# Para rodar o nosso código, executar no terminal: uvicorn main:app --reload
# Isso inicia o servidor web local para testar a API

# Exemplos de endpoints:
# dominio.com/pedidos

# Métodos REST APIs:
# GET -> leitura/pegar dados
# POST -> enviar/criar dados
# PUT/PATCH -> editar dados
# DELETE -> deletar dados