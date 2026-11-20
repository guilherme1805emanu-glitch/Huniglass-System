from flask import Blueprint, request
from database import db
from app.medicoes.models import Medicao, ItemMedicao
from app.medicoes.validators import (
    validar_medicao,
    validar_edicao_medicao,
    validar_item_medicao,
    validar_edicao_item_medicao
)
from app.common.responses import resposta_sucesso, resposta_erro
from app.common.permissions import verificar_permissao

medicoes_bp = Blueprint("medicoes", __name__, url_prefix="/medicoes")


# ============================================================
# CRIAR MEDIÇÃO
# ============================================================

@medicoes_bp.route("", methods=["POST"])
@verificar_permissao("medicoes", "criar")
def criar_medicao():
    dados = request.get_json()

    if not dados:
        return resposta_erro("Nenhum dado foi enviado.", 400)

    erros = validar_medicao(dados)

    if erros:
        return resposta_erro(erros, 400)

    try:
        medicao = Medicao(
            cliente_id=dados["cliente_id"],
            usuario_id=dados["usuario_id"],
            local_instalacao=dados["local_instalacao"],
            descricao=dados.get("descricao"),
            observacoes=dados.get("observacoes"),
            status=dados.get("status", "pendente")
        )

        db.session.add(medicao)
        db.session.commit()

        return resposta_sucesso(
            "Medição criada com sucesso.",
            {
                "id": medicao.id,
                "cliente_id": medicao.cliente_id,
                "usuario_id": medicao.usuario_id,
                "data": medicao.data,
                "local_instalacao": medicao.local_instalacao,
                "descricao": medicao.descricao,
                "observacoes": medicao.observacoes,
                "status": medicao.status
            },
            201
        )
    except Exception as e:
        db.session.rollback()
        return resposta_erro(
            f"Erro ao criar medição: {str(e)}",
            500
        )


# ============================================================
# LISTAR MEDIÇÕES
# ============================================================

@medicoes_bp.route("", methods=["GET"])
@verificar_permissao("medicoes", "visualizar")
def listar_medicoes():
    try:
        medicoes = Medicao.query.all()

        dados = []

        for medicao in medicoes:
            dados.append({
                "id": medicao.id,
                "cliente_id": medicao.cliente_id,
                "usuario_id": medicao.usuario_id,
                "data": medicao.data,
                "local_instalacao": medicao.local_instalacao,
                "descricao": medicao.descricao,
                "observacoes": medicao.observacoes,
                "status": medicao.status
            })

        return resposta_sucesso(
            "Medições encontradas com sucesso.",
            dados
        )
    
    except Exception as e:
        return resposta_erro(
            f"Erro ao listar medições: {str(e)}",
            500
        )


# ============================================================
# BUSCAR MEDIÇÃO POR ID
# ============================================================

@medicoes_bp.route("/<int:medicao_id>", methods=["GET"])
@verificar_permissao("medicoes", "visualizar")
def buscar_medicao(medicao_id):
    medicao = db.session.get(Medicao, medicao_id)

    if not medicao:
        return resposta_erro(
            "Medição não encontrada.",
            404
        )

    return resposta_sucesso(        
        "Medição encontrada com sucesso.",
        {
            "id": medicao.id,
            "cliente_id": medicao.cliente_id,
            "usuario_id": medicao.usuario_id,
            "data": medicao.data,
            "local_instalacao": medicao.local_instalacao,
            "descricao": medicao.descricao,
            "observacoes": medicao.observacoes,
            "status": medicao.status
        }
    )


# ============================================================
# EDITAR MEDIÇÃO
# ============================================================

@medicoes_bp.route("/<int:medicao_id>", methods=["PUT"])
@verificar_permissao("medicoes", "editar")
def editar_medicao(medicao_id):
    medicao = db.session.get(Medicao, medicao_id)

    if not medicao:
        return resposta_erro(
            "Medição não encontrada.",
            404
        )

    dados = request.get_json()

    if not dados:
        return resposta_erro(
            "Nenhum dado foi enviado.",
            400
        )

    erros = validar_edicao_medicao(dados)

    if erros:
        return resposta_erro(erros, 400)

    try:
        if "cliente_id" in dados:
            medicao.cliente_id = dados["cliente_id"]

        if "usuario_id" in dados:
            medicao.usuario_id = dados["usuario_id"]

        if "local_instalacao" in dados:
            medicao.local_instalacao = dados["local_instalacao"]

        if "descricao" in dados:
            medicao.descricao = dados["descricao"]

        if "observacoes" in dados:
            medicao.observacoes = dados["observacoes"]

        if "status" in dados:
            medicao.status = dados["status"]

        db.session.commit()

        return resposta_sucesso(            
            "Medição atualizada com sucesso.",
            {
                "id": medicao.id,
                "cliente_id": medicao.cliente_id,
                "usuario_id": medicao.usuario_id,
                "data": medicao.data,
                "local_instalacao": medicao.local_instalacao,
                "descricao": medicao.descricao,
                "observacoes": medicao.observacoes,
                "status": medicao.status
            }
        )

    except Exception as e:
        db.session.rollback()
        return resposta_erro(
            f"Erro ao editar medição: {str(e)}",
            500
        )


# ============================================================
# EXCLUIR MEDIÇÃO
# ============================================================

@medicoes_bp.route("/<int:medicao_id>", methods=["DELETE"])
@verificar_permissao("medicoes", "excluir")
def excluir_medicao(medicao_id):
    medicao = db.session.get(Medicao, medicao_id)

    if not medicao:
        return resposta_erro(
            "Medição não encontrada.",
            404
        )

    try:
        db.session.delete(medicao)
        db.session.commit()

        return resposta_sucesso(
            "Medição excluída com sucesso."
        )

    except Exception as e:
        db.session.rollback()
        return resposta_erro(
            f"Erro ao excluir medição: {str(e)}",
            500
        )


# ============================================================
# CRIAR ITEM DA MEDIÇÃO
# ============================================================

@medicoes_bp.route("/<int:medicao_id>/itens", methods=["POST"])
@verificar_permissao("medicoes", "criar")
def criar_item_medicao(medicao_id):
    medicao = db.session.get(Medicao, medicao_id)

    if not medicao:
        return resposta_erro(
            "Medição não encontrada.",
            404
        )

    dados = request.get_json()

    if not dados:
        return resposta_erro(
            "Nenhum dado foi enviado.",
            400
        )

    dados["medicao_id"] = medicao_id

    erros = validar_item_medicao(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    try:
        item = ItemMedicao(
            medicao_id=medicao_id,
            descricao=dados["descricao"],
            largura=float(dados["largura"]),
            altura=float(dados["altura"]),
            quantidade=int(dados.get("quantidade", 1)),
            observacoes=dados.get("observacoes")
        )

        db.session.add(item)
        db.session.commit()

        return resposta_sucesso(
            "Item da medição criado com sucesso.",
            {
                "id": item.id,
                "medicao_id": item.medicao_id,
                "descricao": item.descricao,
                "largura": item.largura,
                "altura": item.altura,
                "quantidade": item.quantidade,
                "observacoes": item.observacoes
            },
            201
        )

    except Exception as e:
        db.session.rollback()

        return resposta_erro(
            f"Erro ao criar item da medição: {str(e)}",
            500
        )


# ============================================================
# LISTAR ITENS DA MEDIÇÃO
# ============================================================

@medicoes_bp.route("/<int:medicao_id>/itens", methods=["GET"])
@verificar_permissao("medicoes", "visualizar")
def listar_itens_medicao(medicao_id):
    medicao = db.session.get(Medicao, medicao_id)

    if not medicao:
        return resposta_erro(
            "Medição não encontrada.",
            404
        )

    try:
        itens = ItemMedicao.query.filter_by(
            medicao_id=medicao_id
        ).all()

        dados = []

        for item in itens:
            dados.append({
                "id": item.id,
                "medicao_id": item.medicao_id,
                "descricao": item.descricao,
                "largura": item.largura,
                "altura": item.altura,
                "quantidade": item.quantidade,
                "observacoes": item.observacoes
            })

        return resposta_sucesso(
            "Itens da medição encontrados com sucesso.",
            dados
        )

    except Exception as e:
        return resposta_erro(
            f"Erro ao listar itens da medição: {str(e)}",
            500
        )


# ============================================================
# BUSCAR ITEM POR ID
# ============================================================

@medicoes_bp.route(
    "/<int:medicao_id>/itens/<int:item_id>",
    methods=["GET"]
)
@verificar_permissao("medicoes", "visualizar")
def buscar_item_medicao(medicao_id, item_id):
    item = ItemMedicao.query.filter_by(
        id=item_id,
        medicao_id=medicao_id
    ).first()

    if not item:
        return resposta_erro(
            "Item da medição não encontrado.",
            404
        )

    return resposta_sucesso(
        "Item da medição encontrado com sucesso.",
        {
            "id": item.id,
            "medicao_id": item.medicao_id,
            "descricao": item.descricao,
            "largura": item.largura,
            "altura": item.altura,
            "quantidade": item.quantidade,
            "observacoes": item.observacoes
        }
    )


# ============================================================
# EDITAR ITEM DA MEDIÇÃO
# ============================================================

@medicoes_bp.route(
    "/<int:medicao_id>/itens/<int:item_id>",
    methods=["PUT"]
)
@verificar_permissao("medicoes", "editar")
def editar_item_medicao(medicao_id, item_id):
    item = ItemMedicao.query.filter_by(
        id=item_id,
        medicao_id=medicao_id
    ).first()

    if not item:
        return resposta_erro(
            "Item da medição não encontrado.",
            404
        )

    dados = request.get_json()

    if not dados:
        return resposta_erro(
            "Nenhum dado foi enviado.",
            400
        )

    erros = validar_edicao_item_medicao(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    try:
        if "descricao" in dados:
            item.descricao = dados["descricao"]

        if "largura" in dados:
            item.largura = float(dados["largura"])

        if "altura" in dados:
            item.altura = float(dados["altura"])

        if "quantidade" in dados:
            item.quantidade = int(dados["quantidade"])

        if "observacoes" in dados:
            item.observacoes = dados["observacoes"]

        db.session.commit()

        return resposta_sucesso(
            "Item da medição atualizado com sucesso.",
            {
                "id": item.id,
                "medicao_id": item.medicao_id,
                "descricao": item.descricao,
                "largura": item.largura,
                "altura": item.altura,
                "quantidade": item.quantidade,
                "observacoes": item.observacoes
            }
        )

    except Exception as e:
        db.session.rollback()

        return resposta_erro(
            f"Erro ao editar item da medição: {str(e)}",
            500
        )


# ============================================================
# EXCLUIR ITEM DA MEDIÇÃO
# ============================================================

@medicoes_bp.route(
    "/<int:medicao_id>/itens/<int:item_id>",
    methods=["DELETE"]
)
@verificar_permissao("medicoes", "excluir")
def excluir_item_medicao(medicao_id, item_id):
    item = ItemMedicao.query.filter_by(
        id=item_id,
        medicao_id=medicao_id
    ).first()

    if not item:
        return resposta_erro(
            "Item da medição não encontrado.",
            404
        )

    try:
        db.session.delete(item)
        db.session.commit()

        return resposta_sucesso(
            "Item da medição excluído com sucesso."
        )

    except Exception as e:
        db.session.rollback()

        return resposta_erro(
            f"Erro ao excluir item da medição: {str(e)}",
            500
        )