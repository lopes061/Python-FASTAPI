# Este arquivo define os modelos (estruturas) das tabelas do banco de dados usando SQLAlchemy.
# Cada classe representa uma tabela no banco de dados.

from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey  # Ferramentas para criar tabelas
from sqlalchemy.orm import declarative_base, relationship  # Base para os modelos e relacionamentos
from sqlalchemy_utils.types import ChoiceType  # Permite criar campos com opções fixas

# Cria a conexão com o banco de dados SQLite
db = create_engine("sqlite:///banco.db")

# Cria a base para os modelos do banco de dados
Base = declarative_base()

# Classe/tabela de Usuário
class Usuario(Base):
    __tablename__ = "usuarios"  # Nome da tabela no banco

    id = Column("id", Integer, primary_key=True, autoincrement=True)  # ID único do usuário
    nome = Column("nome", String)  # Nome do usuário
    email = Column("email", String, nullable=False)  # E-mail do usuário
    senha = Column("senha", String)  # Senha criptografada
    ativo = Column("ativo", Boolean)  # Se o usuário está ativo
    admin = Column("admin", Boolean, default=False)  # Se o usuário é administrador

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin
    

# Classe/tabela de Pedido
class Pedido(Base):
    __tablename__ = "pedidos"  # Nome da tabela no banco

    # Campos do pedido
    id = Column("id", Integer, primary_key=True, autoincrement=True)  # ID do pedido
    status = Column("status", String)  # Status do pedido (ex: PENDENTE, CANCELADO)
    usuario = Column("usuario", ForeignKey("usuarios.id"))  # ID do usuário que fez o pedido
    preco = Column("preco", Float)  # Preço total do pedido
    itens = relationship("ItemPedido", cascade="all, delete")  # Lista de itens do pedido

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.preco = preco
        self.status = status

    def calcular_preco(self):
        """
        Calcula o preço total do pedido somando o preço de todos os itens.
        """
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)
        

# Classe/tabela de ItemPedido
class ItemPedido(Base):
    __tablename__ = "itens_pedido"  # Nome da tabela no banco

    id = Column("id", Integer, primary_key=True, autoincrement=True)  # ID do item
    quantidade = Column("quantidade", Integer)  # Quantidade do item
    sabor = Column("sabor", String)  # Sabor do item
    tamanho = Column("tamanho", String)  # Tamanho do item
    preco_unitario = Column("preco_unitario", Float)  # Preço unitário do item
    pedido = Column("pedido", ForeignKey("pedidos.id"))  # ID do pedido ao qual pertence

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido

# Para criar as tabelas no banco, é necessário executar os metadados do banco.
# Para atualizar o banco de dados, usamos migrações:
# criar a migração: alembic revision --autogenerate -m "mensagem"
# executar a migração: alembic upgrade head