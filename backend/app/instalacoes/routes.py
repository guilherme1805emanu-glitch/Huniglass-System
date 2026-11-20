from flask import Blueprint, request
from datetime import datetime

from database import db

from app.instalacoes.models import Instalacao

from app.instalacoes.validators import (
    validar_instalacao,
    validar_edicao_instalacao
)

from app.pedidos.models import Pedido
from app.auth.models import Usuario
from app.common.permissions import verificar_permissao

from app.common.responses import (
    resposta_sucesso,
    resposta_erro
)


instalacao_bp = Blueprint(
    "instalacao",
    __name__,
    url_prefix="/instalacoes"
)


@instalacao_bp.route("", methods=["POST"])
@verificar_permissao("instalacoes", "criar")
def criar_instalacao():

    dados = request.get_json()

    erros = validar_instalacao(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    pedido = Pedido.query.get(dados["pedido_id"])

    if not pedido:
        return resposta_erro(
            "Pedido não encontrado.",
            404
        )

    instalacao_existente = Instalacao.query.filter_by(
        pedido_id=dados["pedido_id"]
    ).first()

    if instalacao_existente:
        return resposta_erro(
            "Este pedido já possui uma instalação.",
            400
        )

    usuario = Usuario.query.get(dados["usuario_id"])

    if not usuario:
        return resposta_erro(
            "Usuário não encontrado.",
            404
        )

    instalador = Usuario.query.get(dados["instalador_id"])

    if not instalador:
        return resposta_erro(
            "Instalador não encontrado.",
            404
        )

    if instalador.cargo != "instalador":
        return resposta_erro(
            "O usuário informado não possui o cargo de instalador.",
            400
        )

    data_agendada = None

    if dados.get("data_agendada"):

        try:
            data_agendada = datetime.fromisoformat(
                dados["data_agendada"]
            )

        except (ValueError, TypeError):

            return resposta_erro(
                "Data agendada inválida. Use o formato ISO 8601.",
                400
            )

    instalacao = Instalacao(
        pedido_id=dados["pedido_id"],
        usuario_id=dados["usuario_id"],
        instalador_id=dados["instalador_id"],
        data_agendada=data_agendada,
        status=dados.get("status", "agendada"),
        endereco=dados["endereco"],
        observacoes=dados.get("observacoes")
    )

    try:

        db.session.add(instalacao)
        db.session.commit()

    except Exception:

        db.session.rollback()

        return resposta_erro(
            "Erro ao criar instalação.",
            500
        )

    return resposta_sucesso(
        "Instalação criada com sucesso.",
        {
            "id": instalacao.id,
            "pedido_id": instalacao.pedido_id,
            "usuario_id": instalacao.usuario_id,
            "instalador_id": instalacao.instalador_id,
            "data_agendada": (
                instalacao.data_agendada.isoformat()
                if instalacao.data_agendada
                else None
            ),
            "status": instalacao.status,
            "endereco": instalacao.endereco,
            "observacoes": instalacao.observacoes
        },
        201
    )


@instalacao_bp.route("", methods=["GET"])
@verificar_permissao("instalacoes", "visualizar")
def listar_instalacoes():

    instalacoes = Instalacao.query.all()

    dados = []

    for instalacao in instalacoes:

        dados.append({
            "id": instalacao.id,
            "pedido_id": instalacao.pedido_id,
            "usuario_id": instalacao.usuario_id,
            "instalador_id": instalacao.instalador_id,
            "data_agendada": (
                instalacao.data_agendada.isoformat()
                if instalacao.data_agendada
                else None
            ),
            "data_inicio": (
                instalacao.data_inicio.isoformat()
                if instalacao.data_inicio
                else None
            ),
            "data_conclusao": (
                instalacao.data_conclusao.isoformat()
                if instalacao.data_conclusao
                else None
            ),
            "status": instalacao.status,
            "endereco": instalacao.endereco,
            "observacoes": instalacao.observacoes
        })

    return resposta_sucesso(
        "Instalações encontradas.",
        dados
    )


@instalacao_bp.route("/<int:instalacao_id>", methods=["GET"])
@verificar_permissao("instalacoes", "visualizar")
def buscar_instalacao(instalacao_id):

    instalacao = Instalacao.query.get(instalacao_id)

    if not instalacao:
        return resposta_erro(
            "Instalação não encontrada.",
            404
        )

    return resposta_sucesso(
        "Instalação encontrada.",
        {
            "id": instalacao.id,
            "pedido_id": instalacao.pedido_id,
            "usuario_id": instalacao.usuario_id,
            "instalador_id": instalacao.instalador_id,
            "data_agendada": (
                instalacao.data_agendada.isoformat()
                if instalacao.data_agendada
                else None
            ),
            "data_inicio": (
                instalacao.data_inicio.isoformat()
                if instalacao.data_inicio
                else None
            ),
            "data_conclusao": (
                instalacao.data_conclusao.isoformat()
                if instalacao.data_conclusao
                else None
            ),
            "status": instalacao.status,
            "endereco": instalacao.endereco,
            "observacoes": instalacao.observacoes
        }
    )


@instalacao_bp.route("/<int:instalacao_id>", methods=["PUT"])
@verificar_permissao("instalacoes", "editar")
def editar_instalacao(instalacao_id):

    instalacao = Instalacao.query.get(instalacao_id)

    if not instalacao:
        return resposta_erro(
            "Instalação não encontrada.",
            404
        )

    dados = request.get_json()

    erros = validar_edicao_instalacao(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    if "pedido_id" in dados:

        pedido = Pedido.query.get(dados["pedido_id"])

        if not pedido:
            return resposta_erro(
                "Pedido não encontrado.",
                404
            )

        outra_instalacao = Instalacao.query.filter(
            Instalacao.pedido_id == dados["pedido_id"],
            Instalacao.id != instalacao.id
        ).first()

        if outra_instalacao:
            return resposta_erro(
                "Este pedido já possui outra instalação.",
                400
            )

        instalacao.pedido_id = dados["pedido_id"]

    if "usuario_id" in dados:

        usuario = Usuario.query.get(
            dados["usuario_id"]
        )

        if not usuario:
            return resposta_erro(
                "Usuário não encontrado.",
                404
            )

        instalacao.usuario_id = dados["usuario_id"]

    if "instalador_id" in dados:

        instalador = Usuario.query.get(
            dados["instalador_id"]
        )

        if not instalador:
            return resposta_erro(
                "Instalador não encontrado.",
                404
            )

        if instalador.cargo != "instalador":
            return resposta_erro(
                "O usuário informado não possui o cargo de instalador.",
                400
            )

        instalacao.instalador_id = dados["instalador_id"]

    if "data_agendada" in dados:

        if dados["data_agendada"] is None:

            instalacao.data_agendada = None

        else:

            try:

                instalacao.data_agendada = datetime.fromisoformat(
                    dados["data_agendada"]
                )

            except (ValueError, TypeError):

                return resposta_erro(
                    "Data agendada inválida. Use o formato ISO 8601.",
                    400
                )

    if "status" in dados:

        novo_status = dados["status"]

        if novo_status == "em_andamento":
            if instalacao.data_inicio is None:
                instalacao.data_inicio = db.func.now()

        if novo_status == "concluida":
            if instalacao.data_conclusao is None:
                instalacao.data_conclusao = db.func.now()

        instalacao.status = novo_status

    if "endereco" in dados:
        instalacao.endereco = dados["endereco"]

    if "observacoes" in dados:
        instalacao.observacoes = dados["observacoes"]

    try:

        db.session.commit()

    except Exception:

        db.session.rollback()

        return resposta_erro(
            "Erro ao atualizar instalação.",
            500
        )

    return resposta_sucesso(
        "Instalação atualizada com sucesso.",
        {
            "id": instalacao.id,
            "pedido_id": instalacao.pedido_id,
            "usuario_id": instalacao.usuario_id,
            "instalador_id": instalacao.instalador_id,
            "status": instalacao.status,
            "endereco": instalacao.endereco,
            "observacoes": instalacao.observacoes
        }
    )


@instalacao_bp.route("/<int:instalacao_id>", methods=["DELETE"])
@verificar_permissao("instalacoes", "excluir")
def excluir_instalacao(instalacao_id):

    instalacao = Instalacao.query.get(instalacao_id)

    if not instalacao:
        return resposta_erro(
            "Instalação não encontrada.",
            404
        )

    try:

        db.session.delete(instalacao)
        db.session.commit()

    except Exception:

        db.session.rollback()

        return resposta_erro(
            "Erro ao excluir instalação.",
            500
        )

    return resposta_sucesso(
        "Instalação excluída com sucesso."
    )