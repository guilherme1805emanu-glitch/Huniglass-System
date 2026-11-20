from flask import Blueprint, request
from database import db

from app.orcamentos.models import ItemOrcamento, Orcamento
from app.orcamentos.validators import (
    validar_orcamento,
    validar_edicao_orcamento
)

from app.common.responses import resposta_sucesso, resposta_erro
from app.common.permissions import verificar_permissao

from datetime import datetime

orcamentos_bp = Blueprint(
    "orcamentos",
    __name__,
    url_prefix="/orcamentos"
)


@orcamentos_bp.route("", methods=["POST"])
@verificar_permissao("orcamentos", "criar")
def criar_orcamento():
    dados = request.get_json() or {}

    erros = validar_orcamento(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    cliente = db.session.get(
        Orcamento.cliente.property.mapper.class_,
        dados["cliente_id"]
    )

    if not cliente:
        return resposta_erro(
            "Cliente não encontrado.",
            404
        )

    medicao = db.session.get(
        Orcamento.medicao.property.mapper.class_,
        dados["medicao_id"]
    )

    if not medicao:
        return resposta_erro(
            "Medição não encontrada.",
            404
        )

    usuario = db.session.get(
        Orcamento.usuario.property.mapper.class_,
        dados["usuario_id"]
    )

    if not usuario:
        return resposta_erro(
            "Usuário não encontrado.",
            404
        )


    validade = None

    if dados.get("validade"):
        try:
            validade = datetime.strptime(
                dados["validade"],
                "%Y-%m-%d"
            ).date()
        except ValueError:
            return resposta_erro(
                "Data de validade inválida. Use o formato YYYY-MM-DD.",
                400
            )

    try:
        orcamento = Orcamento(
            cliente_id=dados["cliente_id"],
            medicao_id=dados["medicao_id"],
            usuario_id=dados["usuario_id"],
            validade=validade,  
            status=dados.get("status", "rascunho"),
            desconto=float(dados.get("desconto", 0)),
            observacoes=dados.get("observacoes")
        )

        db.session.add(orcamento)
        db.session.commit()

        return resposta_sucesso(
            "Orçamento criado com sucesso.",
            {
                "id": orcamento.id,
                "cliente_id": orcamento.cliente_id,
                "medicao_id": orcamento.medicao_id,
                "usuario_id": orcamento.usuario_id,
                "data": orcamento.data,
                "validade": orcamento.validade,
                "status": orcamento.status,
                "subtotal": orcamento.subtotal,
                "desconto": orcamento.desconto,
                "valor_total": orcamento.valor_total,
                "observacoes": orcamento.observacoes
            },
            201
        )

    except Exception as erro:
        db.session.rollback()

        return resposta_erro(
            "Erro ao criar orçamento.",
            500,
            str(erro)
        )


@orcamentos_bp.route("", methods=["GET"])
@verificar_permissao("orcamentos", "visualizar")
def listar_orcamentos():
    orcamentos = Orcamento.query.all()

    dados = []

    for orcamento in orcamentos:
        dados.append({
            "id": orcamento.id,
            "cliente_id": orcamento.cliente_id,
            "medicao_id": orcamento.medicao_id,
            "usuario_id": orcamento.usuario_id,
            "data": orcamento.data,
            "validade": orcamento.validade,
            "status": orcamento.status,
            "subtotal": orcamento.subtotal,
            "desconto": orcamento.desconto,
            "valor_total": orcamento.valor_total,
            "observacoes": orcamento.observacoes
        })

    return resposta_sucesso(
        "Orçamentos encontrados com sucesso.",
        dados
    )


@orcamentos_bp.route("/<int:orcamento_id>", methods=["GET"])
@verificar_permissao("orcamentos", "visualizar")
def buscar_orcamento(orcamento_id):
    orcamento = db.session.get(Orcamento, orcamento_id)

    if not orcamento:
        return resposta_erro(
            "Orçamento não encontrado.",
            404
        )

    dados = {
        "id": orcamento.id,
        "cliente_id": orcamento.cliente_id,
        "medicao_id": orcamento.medicao_id,
        "usuario_id": orcamento.usuario_id,
        "data": orcamento.data,
        "validade": orcamento.validade,
        "status": orcamento.status,
        "subtotal": orcamento.subtotal,
        "desconto": orcamento.desconto,
        "valor_total": orcamento.valor_total,
        "observacoes": orcamento.observacoes
    }

    return resposta_sucesso(
        "Orçamento encontrado com sucesso.",
        dados
    )


@orcamentos_bp.route("/<int:orcamento_id>", methods=["PUT"])
@verificar_permissao("orcamentos", "editar")
def editar_orcamento(orcamento_id):
    orcamento = db.session.get(Orcamento, orcamento_id)

    if not orcamento:
        return resposta_erro(
            "Orçamento não encontrado.",
            404
        )

    dados = request.get_json() or {}

    erros = validar_edicao_orcamento(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    try:
        campos = [
            "cliente_id",
            "medicao_id",
            "usuario_id",
            "validade",
            "status",
            "desconto",
            "observacoes"
        ]

        for campo in campos:
            if campo in dados:
                setattr(orcamento, campo, dados[campo])

        if "desconto" in dados:
            orcamento.desconto = float(dados["desconto"])

        db.session.commit()

        return resposta_sucesso(
            "Orçamento atualizado com sucesso.",
            {
                "id": orcamento.id,
                "cliente_id": orcamento.cliente_id,
                "medicao_id": orcamento.medicao_id,
                "usuario_id": orcamento.usuario_id,
                "data": orcamento.data,
                "validade": orcamento.validade,
                "status": orcamento.status,
                "subtotal": orcamento.subtotal,
                "desconto": orcamento.desconto,
                "valor_total": orcamento.valor_total,
                "observacoes": orcamento.observacoes
            }
        )

    except Exception as erro:
        db.session.rollback()

        return resposta_erro(
            "Erro ao atualizar orçamento.",
            500,
            str(erro)
        )


@orcamentos_bp.route("/<int:orcamento_id>", methods=["DELETE"])
@verificar_permissao("orcamentos", "excluir")
def excluir_orcamento(orcamento_id):
    orcamento = db.session.get(Orcamento, orcamento_id)

    if not orcamento:
        return resposta_erro(
            "Orçamento não encontrado.",
            404
        )

    try:
        db.session.delete(orcamento)
        db.session.commit()

        return resposta_sucesso(
            "Orçamento excluído com sucesso."
        )

    except Exception as erro:
        db.session.rollback()

        return resposta_erro(
            "Erro ao excluir orçamento.",
            500,
            str(erro)
        )


@orcamentos_bp.route("/<int:orcamento_id>/itens", methods=["POST"])
@verificar_permissao("orcamentos", "criar")
def criar_item_orcamento(orcamento_id):
    orcamento = db.session.get(Orcamento, orcamento_id)

    if not orcamento:
        return resposta_erro(
            "Orçamento não encontrado.",
            404
        )

    dados = request.get_json() or {}
    dados["orcamento_id"] = orcamento_id

    from app.orcamentos.validators import validar_item_orcamento

    erros = validar_item_orcamento(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    try:
        quantidade = float(dados["quantidade"])
        valor_unitario = float(dados["valor_unitario"])

        valor_total = quantidade * valor_unitario

        item = ItemOrcamento(
            orcamento_id=orcamento_id,
            descricao=dados["descricao"],
            quantidade=quantidade,
            valor_unitario=valor_unitario,
            valor_total=valor_total,
            observacoes=dados.get("observacoes")
        )

        db.session.add(item)

        db.session.flush()

        orcamento.subtotal = sum(
            item_orcamento.valor_total
            for item_orcamento in orcamento.itens
        )

        orcamento.valor_total = (
            orcamento.subtotal - orcamento.desconto
        )

        if orcamento.valor_total < 0:
            orcamento.valor_total = 0

        db.session.commit()

        return resposta_sucesso(
            "Item do orçamento criado com sucesso.",
            {
                "id": item.id,
                "orcamento_id": item.orcamento_id,
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
            "Erro ao criar item do orçamento.",
            500,
            str(erro)
        )

@orcamentos_bp.route("/<int:orcamento_id>/itens", methods=["GET"])
@verificar_permissao("orcamentos", "visualizar")
def listar_itens_orcamento(orcamento_id):
    orcamento = db.session.get(Orcamento, orcamento_id)

    if not orcamento:
        return resposta_erro(
            "Orçamento não encontrado.",
            404
        )

    dados = []

    for item in orcamento.itens:
        dados.append({
            "id": item.id,
            "orcamento_id": item.orcamento_id,
            "descricao": item.descricao,
            "quantidade": item.quantidade,
            "valor_unitario": item.valor_unitario,
            "valor_total": item.valor_total,
            "observacoes": item.observacoes
        })

    return resposta_sucesso(
        "Itens do orçamento encontrados com sucesso.",
        dados
    )


@orcamentos_bp.route(
    "/<int:orcamento_id>/itens/<int:item_id>",
    methods=["GET"]
)
@verificar_permissao("orcamentos", "visualizar")
def buscar_item_orcamento(orcamento_id, item_id):
    orcamento = db.session.get(Orcamento, orcamento_id)

    if not orcamento:
        return resposta_erro(
            "Orçamento não encontrado.",
            404
        )

    item = ItemOrcamento.query.filter_by(
        id=item_id,
        orcamento_id=orcamento_id
    ).first()

    if not item:
        return resposta_erro(
            "Item do orçamento não encontrado.",
            404
        )

    dados = {
        "id": item.id,
        "orcamento_id": item.orcamento_id,
        "descricao": item.descricao,
        "quantidade": item.quantidade,
        "valor_unitario": item.valor_unitario,
        "valor_total": item.valor_total,
        "observacoes": item.observacoes
    }

    return resposta_sucesso(
        "Item do orçamento encontrado com sucesso.",
        dados
    )


@orcamentos_bp.route(
    "/<int:orcamento_id>/itens/<int:item_id>",
    methods=["PUT"]
)
@verificar_permissao("orcamentos", "editar")
def editar_item_orcamento(orcamento_id, item_id):
    orcamento = db.session.get(Orcamento, orcamento_id)

    if not orcamento:
        return resposta_erro(
            "Orçamento não encontrado.",
            404
        )

    item = ItemOrcamento.query.filter_by(
        id=item_id,
        orcamento_id=orcamento_id
    ).first()

    if not item:
        return resposta_erro(
            "Item do orçamento não encontrado.",
            404
        )

    dados = request.get_json() or {}

    from app.orcamentos.validators import validar_edicao_item_orcamento

    erros = validar_edicao_item_orcamento(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    try:
        if "descricao" in dados:
            item.descricao = dados["descricao"]

        if "quantidade" in dados:
            item.quantidade = float(dados["quantidade"])

        if "valor_unitario" in dados:
            item.valor_unitario = float(dados["valor_unitario"])

        if "observacoes" in dados:
            item.observacoes = dados["observacoes"]

        # Recalcula o valor do item
        item.valor_total = (
            item.quantidade * item.valor_unitario
        )

        # Recalcula o orçamento
        orcamento.subtotal = sum(
            item_orcamento.valor_total
            for item_orcamento in orcamento.itens
        )

        orcamento.valor_total = (
            orcamento.subtotal - orcamento.desconto
        )

        if orcamento.valor_total < 0:
            orcamento.valor_total = 0

        db.session.commit()

        return resposta_sucesso(
            "Item do orçamento atualizado com sucesso.",
            {
                "id": item.id,
                "orcamento_id": item.orcamento_id,
                "descricao": item.descricao,
                "quantidade": item.quantidade,
                "valor_unitario": item.valor_unitario,
                "valor_total": item.valor_total,
                "observacoes": item.observacoes
            }
        )

    except Exception as erro:
        db.session.rollback()

        return resposta_erro(
            "Erro ao atualizar item do orçamento.",
            500,
            str(erro)
        )


@orcamentos_bp.route(
    "/<int:orcamento_id>/itens/<int:item_id>",
    methods=["DELETE"]
)
@verificar_permissao("orcamentos", "excluir")
def excluir_item_orcamento(orcamento_id, item_id):
    orcamento = db.session.get(Orcamento, orcamento_id)

    if not orcamento:
        return resposta_erro(
            "Orçamento não encontrado.",
            404
        )

    item = ItemOrcamento.query.filter_by(
        id=item_id,
        orcamento_id=orcamento_id
    ).first()

    if not item:
        return resposta_erro(
            "Item do orçamento não encontrado.",
            404
        )

    try:
        db.session.delete(item)

        db.session.flush()

        orcamento.subtotal = sum(
            item_orcamento.valor_total
            for item_orcamento in orcamento.itens
            if item_orcamento.id != item_id
        )

        orcamento.valor_total = (
            orcamento.subtotal - orcamento.desconto
        )

        if orcamento.valor_total < 0:
            orcamento.valor_total = 0

        db.session.commit()

        return resposta_sucesso(
            "Item do orçamento excluído com sucesso."
        )

    except Exception as erro:
        db.session.rollback()

        return resposta_erro(
            "Erro ao excluir item do orçamento.",
            500,
            str(erro)
        )