from flask import Blueprint, request

from database import db

from app.pedidos.models import Pedido, ItemPedido

from app.common.permissions import verificar_permissao
from app.common.responses import resposta_sucesso, resposta_erro

from app.pedidos.validators import (
    validar_pedido,
    validar_edicao_pedido,
    validar_edicao_item_pedido,
    validar_item_pedido
)


pedidos_bp = Blueprint(
    "pedidos",
    __name__,
    url_prefix="/pedidos"
)


@pedidos_bp.route("", methods=["POST"])
@verificar_permissao("pedidos", "criar")
def criar_pedido():

    dados = request.get_json() or {}

    erros = validar_pedido(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    try:
        pedido = Pedido(
            cliente_id=dados["cliente_id"],
            orcamento_id=dados["orcamento_id"],
            usuario_id=dados["usuario_id"],
            status=dados.get(
                "status",
                "aguardando_producao"
            ),
            valor_total=float(
                dados.get("valor_total", 0)
            ),
            entrada=float(
                dados.get("entrada", 0)
            ),
            observacoes=dados.get("observacoes")
        )

        pedido.restante = (
            pedido.valor_total - pedido.entrada
        )

        if pedido.restante < 0:
            pedido.restante = 0

        db.session.add(pedido)
        db.session.commit()

        return resposta_sucesso(
            "Pedido criado com sucesso.",
            {
                "id": pedido.id,
                "cliente_id": pedido.cliente_id,
                "orcamento_id": pedido.orcamento_id,
                "usuario_id": pedido.usuario_id,
                "data": pedido.data,
                "status": pedido.status,
                "valor_total": pedido.valor_total,
                "entrada": pedido.entrada,
                "restante": pedido.restante,
                "observacoes": pedido.observacoes
            },
            201
        )

    except Exception as erro:
        db.session.rollback()

        return resposta_erro(
            "Erro ao criar pedido.",
            500,
            str(erro)
        )


@pedidos_bp.route("", methods=["GET"])
@verificar_permissao("pedidos", "visualizar")
def listar_pedidos():

    pedidos = Pedido.query.all()

    dados = []

    for pedido in pedidos:
        dados.append({
            "id": pedido.id,
            "cliente_id": pedido.cliente_id,
            "orcamento_id": pedido.orcamento_id,
            "usuario_id": pedido.usuario_id,
            "data": pedido.data,
            "status": pedido.status,
            "valor_total": pedido.valor_total,
            "entrada": pedido.entrada,
            "restante": pedido.restante,
            "observacoes": pedido.observacoes
        })

    return resposta_sucesso(
        "Pedidos encontrados com sucesso.",
        dados
    )


@pedidos_bp.route("/<int:pedido_id>", methods=["GET"])
@verificar_permissao("pedidos", "visualizar")
def buscar_pedido(pedido_id):

    pedido = db.session.get(
        Pedido,
        pedido_id
    )

    if not pedido:
        return resposta_erro(
            "Pedido não encontrado.",
            404
        )

    dados = {
        "id": pedido.id,
        "cliente_id": pedido.cliente_id,
        "orcamento_id": pedido.orcamento_id,
        "usuario_id": pedido.usuario_id,
        "data": pedido.data,
        "status": pedido.status,
        "valor_total": pedido.valor_total,
        "entrada": pedido.entrada,
        "restante": pedido.restante,
        "observacoes": pedido.observacoes
    }

    return resposta_sucesso(
        "Pedido encontrado com sucesso.",
        dados
    )


@pedidos_bp.route("/<int:pedido_id>", methods=["PUT"])
@verificar_permissao("pedidos", "editar")
def editar_pedido(pedido_id):

    pedido = db.session.get(
        Pedido,
        pedido_id
    )

    if not pedido:
        return resposta_erro(
            "Pedido não encontrado.",
            404
        )

    dados = request.get_json() or {}

    erros = validar_edicao_pedido(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    try:

        if "status" in dados:
            pedido.status = dados["status"]

        if "entrada" in dados:
            pedido.entrada = float(
                dados["entrada"]
            )

        if "observacoes" in dados:
            pedido.observacoes = dados["observacoes"]

        pedido.restante = (
            pedido.valor_total - pedido.entrada
        )

        if pedido.restante < 0:
            pedido.restante = 0

        db.session.commit()

        return resposta_sucesso(
            "Pedido atualizado com sucesso.",
            {
                "id": pedido.id,
                "cliente_id": pedido.cliente_id,
                "orcamento_id": pedido.orcamento_id,
                "usuario_id": pedido.usuario_id,
                "data": pedido.data,
                "status": pedido.status,
                "valor_total": pedido.valor_total,
                "entrada": pedido.entrada,
                "restante": pedido.restante,
                "observacoes": pedido.observacoes
            }
        )

    except Exception as erro:
        db.session.rollback()

        return resposta_erro(
            "Erro ao atualizar pedido.",
            500,
            str(erro)
        )


@pedidos_bp.route("/<int:pedido_id>", methods=["DELETE"])
@verificar_permissao("pedidos", "excluir")
def excluir_pedido(pedido_id):

    pedido = db.session.get(
        Pedido,
        pedido_id
    )

    if not pedido:
        return resposta_erro(
            "Pedido não encontrado.",
            404
        )

    try:

        db.session.delete(pedido)
        db.session.commit()

        return resposta_sucesso(
            "Pedido excluído com sucesso."
        )

    except Exception as erro:
        db.session.rollback()

        return resposta_erro(
            "Erro ao excluir pedido.",
            500,
            str(erro)
        )


@pedidos_bp.route(
    "/<int:pedido_id>/itens",
    methods=["POST"]
)
@verificar_permissao("pedidos", "criar")
def criar_item_pedido(pedido_id):

    pedido = db.session.get(
        Pedido,
        pedido_id
    )

    if not pedido:
        return resposta_erro(
            "Pedido não encontrado.",
            404
        )

    dados = request.get_json() or {}
    dados["pedido_id"] = pedido_id

    from app.pedidos.validators import validar_item_pedido

    erros = validar_item_pedido(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    try:
        quantidade = float(
            dados["quantidade"]
        )

        valor_unitario = float(
            dados["valor_unitario"]
        )

        valor_total = (
            quantidade * valor_unitario
        )

        item = ItemPedido(
            pedido_id=pedido_id,
            descricao=dados["descricao"],
            quantidade=quantidade,
            valor_unitario=valor_unitario,
            valor_total=valor_total,
            observacoes=dados.get("observacoes")
        )

        db.session.add(item)

        db.session.flush()

        pedido.valor_total = sum(
            item_pedido.valor_total
            for item_pedido in pedido.itens
        )

        pedido.restante = (
            pedido.valor_total - pedido.entrada
        )

        if pedido.restante < 0:
            pedido.restante = 0

        db.session.commit()

        return resposta_sucesso(
            "Item do pedido criado com sucesso.",
            {
                "id": item.id,
                "pedido_id": item.pedido_id,
                "descricao": item.descricao,
                "quantidade": item.quantidade,
                "valor_unitario": item.valor_unitario,
                "valor_total": item.valor_total,
                "observacoes": item.observacoes
            },
            201
        )

    except Exception as erro:
        db.session.rollback()

        return resposta_erro(
            "Erro ao criar item do pedido.",
            500,
            str(erro)
        )


@pedidos_bp.route(
    "/<int:pedido_id>/itens",
    methods=["GET"]
)
@verificar_permissao("pedidos", "visualizar")
def listar_itens_pedido(pedido_id):

    pedido = db.session.get(
        Pedido,
        pedido_id
    )

    if not pedido:
        return resposta_erro(
            "Pedido não encontrado.",
            404
        )

    dados = []

    for item in pedido.itens:
        dados.append({
            "id": item.id,
            "pedido_id": item.pedido_id,
            "descricao": item.descricao,
            "quantidade": item.quantidade,
            "valor_unitario": item.valor_unitario,
            "valor_total": item.valor_total,
            "observacoes": item.observacoes
        })

    return resposta_sucesso(
        "Itens do pedido encontrados com sucesso.",
        dados
    )


@pedidos_bp.route(
    "/<int:pedido_id>/itens/<int:item_id>",
    methods=["GET"]
)
@verificar_permissao("pedidos", "visualizar")
def buscar_item_pedido(pedido_id, item_id):

    pedido = db.session.get(Pedido, pedido_id)

    if not pedido:
        return resposta_erro(
            "Pedido não encontrado.",
            404
        )

    item = db.session.get(ItemPedido, item_id)

    if not item or item.pedido_id != pedido_id:
        return resposta_erro(
            "Item não encontrado neste pedido.",
            404
        )

    dados = {
        "id": item.id,
        "pedido_id": item.pedido_id,
        "descricao": item.descricao,
        "quantidade": item.quantidade,
        "valor_unitario": item.valor_unitario,
        "valor_total": item.valor_total,
        "observacoes": item.observacoes
    }

    return resposta_sucesso(
        "Item do pedido encontrado com sucesso.",
        dados
    )


@pedidos_bp.route(
    "/<int:pedido_id>/itens/<int:item_id>",
    methods=["PUT"]
)
@verificar_permissao("pedidos", "editar")
def editar_item_pedido(pedido_id, item_id):

    pedido = db.session.get(Pedido, pedido_id)

    if not pedido:
        return resposta_erro(
            "Pedido não encontrado.",
            404
        )

    item = db.session.get(ItemPedido, item_id)

    if not item or item.pedido_id != pedido_id:
        return resposta_erro(
            "Item não encontrado neste pedido.",
            404
        )

    dados = request.get_json() or {}

    erros = validar_edicao_item_pedido(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    if "descricao" in dados:
        item.descricao = dados["descricao"]

    if "quantidade" in dados:
        item.quantidade = dados["quantidade"]

    if "valor_unitario" in dados:
        item.valor_unitario = dados["valor_unitario"]

    if "observacoes" in dados:
        item.observacoes = dados["observacoes"]

    item.valor_total = (
        item.quantidade * item.valor_unitario
    )

    pedido.valor_total = sum(
        item_pedido.valor_total
        for item_pedido in pedido.itens
    )

    pedido.restante = max(
        pedido.valor_total - pedido.entrada,
        0
    )

    try:
        db.session.commit()

        return resposta_sucesso(
            "Item do pedido atualizado com sucesso.",
            {
                "id": item.id,
                "pedido_id": item.pedido_id,
                "descricao": item.descricao,
                "quantidade": item.quantidade,
                "valor_unitario": item.valor_unitario,
                "valor_total": item.valor_total,
                "observacoes": item.observacoes
            }
        )

    except Exception:
        db.session.rollback()

        return resposta_erro(
            "Erro ao atualizar item do pedido.",
            500
        )


@pedidos_bp.route(
    "/<int:pedido_id>/itens/<int:item_id>",
    methods=["DELETE"]
)
@verificar_permissao("pedidos", "editar")
def excluir_item_pedido(pedido_id, item_id):

    pedido = db.session.get(Pedido, pedido_id)

    if not pedido:
        return resposta_erro(
            "Pedido não encontrado.",
            404
        )

    item = db.session.get(ItemPedido, item_id)

    if not item or item.pedido_id != pedido_id:
        return resposta_erro(
            "Item não encontrado neste pedido.",
            404
        )

    try:
        db.session.delete(item)
        db.session.flush()

        pedido.valor_total = sum(
            item_pedido.valor_total
            for item_pedido in pedido.itens
        )

        pedido.restante = max(
            pedido.valor_total - pedido.entrada,
            0
        )

        db.session.commit()

        return resposta_sucesso(
            "Item do pedido excluído com sucesso.",
            {
                "pedido_id": pedido.id,
                "valor_total": pedido.valor_total,
                "entrada": pedido.entrada,
                "restante": pedido.restante
            }
        )

    except Exception:
        db.session.rollback()

        return resposta_erro(
            "Erro ao excluir item do pedido.",
            500
        )