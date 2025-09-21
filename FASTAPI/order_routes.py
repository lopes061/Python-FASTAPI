# Este arquivo define as rotas relacionadas aos pedidos.
# Todas as rotas de pedidos exigem autenticação do usuário.

from fastapi import APIRouter, Depends, HTTPException  # Ferramentas para xrotas e tratar erros
from sqlalchemy.orm import Session  # Sessão do banco de dados
from dependencies import pegar_sessao, verificar_token  # Funções auxiliares para banco e autenticação
from schemas import PedidoSchema, ItemPedidoSchema  # Esquemas para validar dados recebidos
from models import Pedido, Usuario, ItemPedido  # Modelos do banco de dados

# Cria um grupo de rotas com prefixo "/pedidos"
# Todas as rotas exigem autenticação (verificar_token)
order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def pedidos():
    """
    Rota padrão de pedidos.
    Apenas retorna uma mensagem informando que está na rota de pedidos.
    """
    return {"mensagem": "Você acessou a rota de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    """
    Cria um novo pedido para o usuário informado.
    Salva o pedido no banco de dados.
    """
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Cancela um pedido existente.
    Apenas o administrador ou o dono do pedido pode cancelar.
    """
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido número: {pedido.id} cancelado com sucesso",
        "pedido": pedido
    }

@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Lista todos os pedidos do sistema.
    Apenas administradores podem acessar essa rota.
    """
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
        }

@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int, 
                                item_pedido_schema: ItemPedidoSchema, 
                                session: Session = Depends(pegar_sessao), 
                                usuario: Usuario = Depends(verificar_token)):
    """
    Adiciona um item a um pedido existente.
    Apenas o administrador ou o dono do pedido pode adicionar itens.
    """
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não existente")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação")
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, 
                             item_pedido_schema.preco_unitario, id_pedido)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": "Item criado com sucesso",
        "item_id": item_pedido.id,
        "preco_pedido": pedido.preco
    }

@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int, 
                                session: Session = Depends(pegar_sessao), 
                                usuario: Usuario = Depends(verificar_token)):
    """
    Remove um item de um pedido existente.
    Apenas o administrador ou o dono do pedido pode remover itens.
    """
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id==id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item no pedido não existente")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação")
    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": "Item removido com sucesso",
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }