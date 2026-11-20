from datetime import datetime

from flask import Blueprint, request

from database import db

from app.financeiro.models import LancamentoFinanceiro

from app.financeiro.validators import (
    validar_lancamento,
    validar_edicao_lancamento
)

from app.common.permissions import verificar_permissao

from app.common.responses import (
    resposta_sucesso,
    resposta_erro
)

from app.pedidos.models import Pedido
from app.estoque.models import Fornecedor
from app.auth.models import Usuario

from flask_jwt_extended import get_jwt_identity


financeiro_bp = Blueprint(
    "financeiro",
    __name__,
    url_prefix="/financeiro"
)

@financeiro_bp.route("", methods=["POST"])
@verificar_permissao("financeiro", "criar")
def criar_lancamento():
    dados = request.get_json()

    if not dados:
        return resposta_erro(
            "Nenhum dado foi enviado.",
            400
        )

    erros = validar_lancamento(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    try:
        usuario_id = get_jwt_identity()

        usuario = db.session.get(
            Usuario,
            usuario_id
        )

        if not usuario:
            return resposta_erro(
                "Usuário não encontrado.",
                404
            )

        pedido_id = dados.get("pedido_id")

        if pedido_id is not None:
            pedido = db.session.get(
                Pedido,
                pedido_id
            )

            if not pedido:
                return resposta_erro(
                    "Pedido não encontrado.",
                    404
                )

        fornecedor_id = dados.get("fornecedor_id")

        if fornecedor_id is not None:
            fornecedor = db.session.get(
                Fornecedor,
                fornecedor_id
            )

            if not fornecedor:
                return resposta_erro(
                    "Fornecedor não encontrado.",
                    404
                )

        tipo = dados.get("tipo")
        categoria = dados.get("categoria")

        # Receita relacionada a pedido
        if tipo == "receita":
            if categoria in ["entrada", "pagamento_final"]:
                if pedido_id is None:
                    return resposta_erro(
                        "O pedido_id é obrigatório para "
                        "entradas e pagamentos finais.",
                        400
                    )

        # Despesa relacionada a fornecedor
        if tipo == "despesa":
            if categoria in ["material", "fornecedor"]:
                if fornecedor_id is None:
                    return resposta_erro(
                        "O fornecedor_id é obrigatório para "
                        "despesas de material ou fornecedor.",
                        400
                    )

        lancamento = LancamentoFinanceiro(
            tipo=tipo,
            categoria=categoria,
            descricao=dados.get("descricao"),
            valor=float(dados.get("valor")),
            pedido_id=pedido_id,
            fornecedor_id=fornecedor_id,
            usuario_id=usuario_id,
            status=dados.get("status", "pendente"),
            data_vencimento=(
                datetime.fromisoformat(dados["data_vencimento"])
                .date()
                if dados.get("data_vencimento")
                else None
            ),

            data_pagamento=(
                datetime.fromisoformat(dados["data_pagamento"])
                if dados.get("data_pagamento")
                else None
            ),
            forma_pagamento=dados.get("forma_pagamento"),
            observacoes=dados.get("observacoes")
        )

        db.session.add(lancamento)
        db.session.commit()

        return resposta_sucesso(
            "Lançamento financeiro criado com sucesso.",
            {
                "id": lancamento.id,
                "tipo": lancamento.tipo,
                "categoria": lancamento.categoria,
                "descricao": lancamento.descricao,
                "valor": lancamento.valor,
                "pedido_id": lancamento.pedido_id,
                "fornecedor_id": lancamento.fornecedor_id,
                "usuario_id": lancamento.usuario_id,
                "status": lancamento.status,
                "data_vencimento": (
                    lancamento.data_vencimento.isoformat()
                    if lancamento.data_vencimento
                    else None
                ),
                "data_pagamento": (
                    lancamento.data_pagamento.isoformat()
                    if lancamento.data_pagamento
                    else None
                ),
                "forma_pagamento": lancamento.forma_pagamento,
                "observacoes": lancamento.observacoes
            },
            201
        )

    except Exception as erro:
        db.session.rollback()

        return resposta_erro(
            "Erro ao criar lançamento financeiro.",
            500,
            str(erro)
        )


@financeiro_bp.route("", methods=["GET"])
@verificar_permissao("financeiro", "visualizar")
def listar_lancamentos():
    try:
        lancamentos = LancamentoFinanceiro.query.order_by(
            LancamentoFinanceiro.id.desc()
        ).all()

        dados = []

        for lancamento in lancamentos:
            dados.append({
                "id": lancamento.id,
                "tipo": lancamento.tipo,
                "categoria": lancamento.categoria,
                "descricao": lancamento.descricao,
                "valor": lancamento.valor,
                "pedido_id": lancamento.pedido_id,
                "fornecedor_id": lancamento.fornecedor_id,
                "usuario_id": lancamento.usuario_id,
                "status": lancamento.status,
                "data_lancamento": (
                    lancamento.data_lancamento.isoformat()
                    if lancamento.data_lancamento
                    else None
                ),
                "data_vencimento": (
                    lancamento.data_vencimento.isoformat()
                    if lancamento.data_vencimento
                    else None
                ),
                "data_pagamento": (
                    lancamento.data_pagamento.isoformat()
                    if lancamento.data_pagamento
                    else None
                ),
                "forma_pagamento": lancamento.forma_pagamento,
                "observacoes": lancamento.observacoes
            })

        return resposta_sucesso(
            "Lançamentos financeiros encontrados com sucesso.",
            dados
        )

    except Exception as erro:
        return resposta_erro(
            "Erro ao listar lançamentos financeiros.",
            500,
            str(erro)
        )


@financeiro_bp.route("/<int:lancamento_id>", methods=["GET"])
@verificar_permissao("financeiro", "visualizar")
def buscar_lancamento(lancamento_id):
    lancamento = db.session.get(
        LancamentoFinanceiro,
        lancamento_id
    )

    if not lancamento:
        return resposta_erro(
            "Lançamento financeiro não encontrado.",
            404
        )

    dados = {
        "id": lancamento.id,
        "tipo": lancamento.tipo,
        "categoria": lancamento.categoria,
        "descricao": lancamento.descricao,
        "valor": lancamento.valor,
        "pedido_id": lancamento.pedido_id,
        "fornecedor_id": lancamento.fornecedor_id,
        "usuario_id": lancamento.usuario_id,
        "status": lancamento.status,
        "data_lancamento": (
            lancamento.data_lancamento.isoformat()
            if lancamento.data_lancamento
            else None
        ),
        "data_vencimento": (
            lancamento.data_vencimento.isoformat()
            if lancamento.data_vencimento
            else None
        ),
        "data_pagamento": (
            lancamento.data_pagamento.isoformat()
            if lancamento.data_pagamento
            else None
        ),
        "forma_pagamento": lancamento.forma_pagamento,
        "observacoes": lancamento.observacoes
    }

    return resposta_sucesso(
        "Lançamento financeiro encontrado com sucesso.",
        dados
    )


@financeiro_bp.route("/<int:lancamento_id>", methods=["PUT"])
@verificar_permissao("financeiro", "editar")
def editar_lancamento(lancamento_id):
    dados = request.get_json()

    if not dados:
        return resposta_erro(
            "Nenhum dado foi enviado.",
            400
        )

    lancamento = db.session.get(
        LancamentoFinanceiro,
        lancamento_id
    )

    if not lancamento:
        return resposta_erro(
            "Lançamento financeiro não encontrado.",
            404
        )

    erros = validar_edicao_lancamento(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    try:
        if "pedido_id" in dados:
            pedido_id = dados.get("pedido_id")

            if pedido_id is not None:
                pedido = db.session.get(
                    Pedido,
                    pedido_id
                )

                if not pedido:
                    return resposta_erro(
                        "Pedido não encontrado.",
                        404
                    )

            lancamento.pedido_id = pedido_id

        if "fornecedor_id" in dados:
            fornecedor_id = dados.get("fornecedor_id")

            if fornecedor_id is not None:
                fornecedor = db.session.get(
                    Fornecedor,
                    fornecedor_id
                )

                if not fornecedor:
                    return resposta_erro(
                        "Fornecedor não encontrado.",
                        404
                    )

            lancamento.fornecedor_id = fornecedor_id

        if "tipo" in dados:
            lancamento.tipo = dados["tipo"]

        if "categoria" in dados:
            lancamento.categoria = dados["categoria"]

        if "descricao" in dados:
            lancamento.descricao = dados["descricao"]

        if "valor" in dados:
            lancamento.valor = float(dados["valor"])

        if "status" in dados:
            lancamento.status = dados["status"]

        if "data_vencimento" in dados:
            lancamento.data_vencimento = (
                datetime.fromisoformat(
                    dados["data_vencimento"]
                ).date()
                if dados["data_vencimento"]
                else None
            )

        if "data_pagamento" in dados:
            lancamento.data_pagamento = (
                datetime.fromisoformat(
                    dados["data_pagamento"]
                )
                if dados["data_pagamento"]
                else None
            )

        if "forma_pagamento" in dados:
            lancamento.forma_pagamento = dados["forma_pagamento"]

        if "observacoes" in dados:
            lancamento.observacoes = dados["observacoes"]

        db.session.commit()

        return resposta_sucesso(
            "Lançamento financeiro atualizado com sucesso.",
            {
                "id": lancamento.id,
                "tipo": lancamento.tipo,
                "categoria": lancamento.categoria,
                "descricao": lancamento.descricao,
                "valor": lancamento.valor,
                "pedido_id": lancamento.pedido_id,
                "fornecedor_id": lancamento.fornecedor_id,
                "usuario_id": lancamento.usuario_id,
                "status": lancamento.status,
                "data_vencimento": (
                    lancamento.data_vencimento.isoformat()
                    if lancamento.data_vencimento
                    else None
                ),
                "data_pagamento": (
                    lancamento.data_pagamento.isoformat()
                    if lancamento.data_pagamento
                    else None
                ),
                "forma_pagamento": lancamento.forma_pagamento,
                "observacoes": lancamento.observacoes
            }
        )

    except Exception as erro:
        db.session.rollback()

        return resposta_erro(
            "Erro ao editar lançamento financeiro.",
            500,
            str(erro)
        )


@financeiro_bp.route("/<int:lancamento_id>", methods=["DELETE"])
@verificar_permissao("financeiro", "excluir")
def excluir_lancamento(lancamento_id):
    lancamento = db.session.get(
        LancamentoFinanceiro,
        lancamento_id
    )

    if not lancamento:
        return resposta_erro(
            "Lançamento financeiro não encontrado.",
            404
        )

    try:
        db.session.delete(lancamento)
        db.session.commit()

        return resposta_sucesso(
            "Lançamento financeiro excluído com sucesso."
        )

    except Exception as erro:
        db.session.rollback()

        return resposta_erro(
            "Erro ao excluir lançamento financeiro.",
            500,
            str(erro)
        )
