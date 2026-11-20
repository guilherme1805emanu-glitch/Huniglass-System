from flask import Blueprint, request

from datetime import datetime

from database import db

from app.producao.models import Producao,ItemProducao,MaterialProducao
from app.producao.validators import (
    validar_producao,
    validar_edicao_producao,
    validar_item_producao,
    validar_edicao_item_producao,
    validar_edicao_material_producao,
    validar_material_producao
)

from app.estoque.models import Material,MovimentacaoEstoque
from app.pedidos.models import Pedido, ItemPedido

from app.auth.models import Usuario
from app.common.permissions import verificar_permissao

from app.common.responses import (
    resposta_sucesso,
    resposta_erro
)


producao_bp = Blueprint(
    "producao",
    __name__,
    url_prefix="/producao"
)


# ============================================================
# CRIAR PRODUÇÃO
# ============================================================

@producao_bp.route("", methods=["POST"])
@verificar_permissao("producao", "criar")
def criar_producao():

    dados = request.get_json()

    if not dados:
        return resposta_erro(
            "Nenhum dado foi enviado."
        )

    erros = validar_producao(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            erros=erros
        )

    pedido = db.session.get(
        Pedido,
        dados["pedido_id"]
    )

    if not pedido:
        return resposta_erro(
            "Pedido não encontrado.",
            status=404
        )

    usuario = db.session.get(
        Usuario,
        dados["usuario_id"]
    )

    if not usuario:
        return resposta_erro(
            "Usuário não encontrado.",
            status=404
        )

    producao_existente = Producao.query.filter_by(
        pedido_id=dados["pedido_id"]
    ).first()

    if producao_existente:
        return resposta_erro(
            "Este pedido já possui uma produção.",
            status=409
        )

    producao = Producao(
        pedido_id=dados["pedido_id"],
        usuario_id=dados["usuario_id"],
        status=dados.get(
            "status",
            "aguardando"
        ),
        observacoes=dados.get(
            "observacoes"
        )
    )

    db.session.add(producao)

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()

        return resposta_erro(
            "Erro ao criar produção.",
            status=500
        )

    return resposta_sucesso(
        "Produção criada com sucesso.",
        dados={
            "id": producao.id,
            "pedido_id": producao.pedido_id,
            "usuario_id": producao.usuario_id,
            "status": producao.status,
            "observacoes": producao.observacoes
        },
        status=201
    )


# ============================================================
# LISTAR PRODUÇÕES
# ============================================================

@producao_bp.route("", methods=["GET"])
@verificar_permissao("producao", "visualizar")
def listar_producoes():

    producoes = Producao.query.all()

    dados = []

    for producao in producoes:

        dados.append({
            "id": producao.id,
            "pedido_id": producao.pedido_id,
            "usuario_id": producao.usuario_id,
            "status": producao.status,
            "data_inicio": (
                producao.data_inicio.isoformat()
                if producao.data_inicio
                else None
            ),
            "data_previsao": (
                producao.data_previsao.isoformat()
                if producao.data_previsao
                else None
            ),
            "data_conclusao": (
                producao.data_conclusao.isoformat()
                if producao.data_conclusao
                else None
            ),
            "observacoes": producao.observacoes
        })

    return resposta_sucesso(
        "Produções encontradas.",
        dados=dados
    )


# ============================================================
# BUSCAR PRODUÇÃO POR ID
# ============================================================

@producao_bp.route("/<int:producao_id>", methods=["GET"])
@verificar_permissao("producao", "visualizar")
def buscar_producao(producao_id):

    producao = db.session.get(
        Producao,
        producao_id
    )

    if not producao:
        return resposta_erro(
            "Produção não encontrada.",
            status=404
        )

    return resposta_sucesso(
        "Produção encontrada.",
        dados={
            "id": producao.id,
            "pedido_id": producao.pedido_id,
            "usuario_id": producao.usuario_id,
            "status": producao.status,
            "data_inicio": (
                producao.data_inicio.isoformat()
                if producao.data_inicio
                else None
            ),
            "data_previsao": (
                producao.data_previsao.isoformat()
                if producao.data_previsao
                else None
            ),
            "data_conclusao": (
                producao.data_conclusao.isoformat()
                if producao.data_conclusao
                else None
            ),
            "observacoes": producao.observacoes
        }
    )


# ============================================================
# EDITAR PRODUÇÃO
# ============================================================

@producao_bp.route("/<int:producao_id>", methods=["PUT"])
@verificar_permissao("producao", "editar")
def editar_producao(producao_id):

    producao = db.session.get(
        Producao,
        producao_id
    )

    if not producao:
        return resposta_erro(
            "Produção não encontrada.",
            status=404
        )

    dados = request.get_json()

    if not dados:
        return resposta_erro(
            "Nenhum dado foi enviado."
        )

    erros = validar_edicao_producao(
        dados
    )

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            erros=erros
        )

    if "pedido_id" in dados:

        pedido = db.session.get(
            Pedido,
            dados["pedido_id"]
        )

        if not pedido:
            return resposta_erro(
                "Pedido não encontrado.",
                status=404
            )

        outra_producao = Producao.query.filter(
            Producao.pedido_id == dados["pedido_id"],
            Producao.id != producao.id
        ).first()

        if outra_producao:
            return resposta_erro(
                "Este pedido já possui outra produção.",
                status=409
            )

        producao.pedido_id = dados[
            "pedido_id"
        ]

    if "usuario_id" in dados:

        usuario = db.session.get(
            Usuario,
            dados["usuario_id"]
        )

        if not usuario:
            return resposta_erro(
                "Usuário não encontrado.",
                status=404
            )

        producao.usuario_id = dados[
            "usuario_id"
        ]

    if "status" in dados:
        novo_status = dados["status"]

        if (
            novo_status == "em_producao"
            and producao.status != "em_producao"
            and producao.data_inicio is None
        ):
            producao.data_inicio = db.func.now()

        if (
            novo_status == "concluida"
            and producao.status != "concluida"
            and producao.data_conclusao is None
        ):
            producao.data_conclusao = db.func.now()

        producao.status = novo_status

    if "observacoes" in dados:
        producao.observacoes = dados[
            "observacoes"
        ]

    if "data_previsao" in dados:
        if producao.status == "concluida":
            return resposta_erro(
                "Não é possível alterar a data de previsão de uma produção concluída.",
                status=400
            )

        if dados["data_previsao"] is None:
            producao.data_previsao = None
        else:
            try:
                producao.data_previsao = datetime.fromisoformat(
                    dados["data_previsao"]
                )
            except ValueError:
                return resposta_erro(
                    "Data de previsão inválida.",
                    status=400
                )
            
    try:
        db.session.commit()

    except Exception:
        db.session.rollback()

        return resposta_erro(
            "Erro ao editar produção.",
            status=500
        )

    return resposta_sucesso(
        "Produção atualizada com sucesso.",
        dados={
            "id": producao.id,
            "pedido_id": producao.pedido_id,
            "usuario_id": producao.usuario_id,
            "status": producao.status,
            "observacoes": producao.observacoes
        }
    )


# ============================================================
# EXCLUIR PRODUÇÃO
# ============================================================

@producao_bp.route("/<int:producao_id>", methods=["DELETE"])
@verificar_permissao("producao", "excluir")
def excluir_producao(producao_id):

    producao = db.session.get(
        Producao,
        producao_id
    )

    if not producao:
        return resposta_erro(
            "Produção não encontrada.",
            status=404
        )

    try:
        db.session.delete(
            producao
        )

        db.session.commit()

    except Exception:
        db.session.rollback()

        return resposta_erro(
            "Erro ao excluir produção.",
            status=500
        )

    return resposta_sucesso(
        "Produção excluída com sucesso."
    )


@producao_bp.route("/<int:producao_id>/itens", methods=["POST"])
@verificar_permissao("producao", "criar")
def criar_item_producao(producao_id):
    dados = request.get_json()

    if not dados:
        return resposta_erro("Nenhum dado foi enviado.")

    erros = validar_item_producao(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            erros=erros
        )

    producao = db.session.get(Producao, producao_id)

    if not producao:
        return resposta_erro(
            "Produção não encontrada.",
            status=404
        )

    item_pedido = db.session.get(
        ItemPedido,
        dados["item_pedido_id"]
    )

    if not item_pedido:
        return resposta_erro(
            "Item do pedido não encontrado.",
            status=404
        )

    if item_pedido.pedido_id != producao.pedido_id:
        return resposta_erro(
            "O item do pedido não pertence ao pedido desta produção.",
            status=400
        )

    item_existente = ItemProducao.query.filter_by(
        producao_id=producao_id,
        item_pedido_id=dados["item_pedido_id"]
    ).first()

    if item_existente:
        return resposta_erro(
            "Este item do pedido já está vinculado a esta produção.",
            status=409
        )

    item = ItemProducao(
        producao_id=producao_id,
        item_pedido_id=dados["item_pedido_id"],
        quantidade=float(dados["quantidade"]),
        status=dados.get("status", "aguardando"),
        observacoes=dados.get("observacoes")
    )

    db.session.add(item)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return resposta_erro(
            "Erro ao criar item da produção.",
            status=500
        )

    return resposta_sucesso(
        "Item da produção criado com sucesso.",
        dados={
            "id": item.id,
            "producao_id": item.producao_id,
            "item_pedido_id": item.item_pedido_id,
            "quantidade": item.quantidade,
            "status": item.status,
            "observacoes": item.observacoes
        },
        status=201
    )


@producao_bp.route("/<int:producao_id>/itens", methods=["GET"])
@verificar_permissao("producao", "visualizar")
def listar_itens_producao(producao_id):
    producao = db.session.get(Producao, producao_id)

    if not producao:
        return resposta_erro(
            "Produção não encontrada.",
            status=404
        )

    itens = ItemProducao.query.filter_by(
        producao_id=producao_id
    ).all()

    dados = []

    for item in itens:
        dados.append({
            "id": item.id,
            "producao_id": item.producao_id,
            "item_pedido_id": item.item_pedido_id,
            "quantidade": item.quantidade,
            "status": item.status,
            "observacoes": item.observacoes
        })

    return resposta_sucesso(
        "Itens da produção encontrados.",
        dados=dados
    )


@producao_bp.route(
    "/<int:producao_id>/itens/<int:item_id>",
    methods=["GET"]
)
@verificar_permissao("producao", "visualizar")
def buscar_item_producao(producao_id, item_id):
    producao = db.session.get(Producao, producao_id)

    if not producao:
        return resposta_erro(
            "Produção não encontrada.",
            status=404
        )

    item = ItemProducao.query.filter_by(
        id=item_id,
        producao_id=producao_id
    ).first()

    if not item:
        return resposta_erro(
            "Item da produção não encontrado.",
            status=404
        )

    return resposta_sucesso(
        "Item da produção encontrado.",
        dados={
            "id": item.id,
            "producao_id": item.producao_id,
            "item_pedido_id": item.item_pedido_id,
            "quantidade": item.quantidade,
            "status": item.status,
            "observacoes": item.observacoes
        }
    )


@producao_bp.route(
    "/<int:producao_id>/itens/<int:item_id>",
    methods=["PUT"]
)
@verificar_permissao("producao", "editar")
def editar_item_producao(producao_id, item_id):
    producao = db.session.get(Producao, producao_id)

    if not producao:
        return resposta_erro(
            "Produção não encontrada.",
            status=404
        )

    item = ItemProducao.query.filter_by(
        id=item_id,
        producao_id=producao_id
    ).first()

    if not item:
        return resposta_erro(
            "Item da produção não encontrado.",
            status=404
        )

    dados = request.get_json()

    if not dados:
        return resposta_erro("Nenhum dado foi enviado.")

    erros = validar_edicao_item_producao(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            erros=erros
        )

    if "quantidade" in dados:
        item.quantidade = float(dados["quantidade"])

    if "status" in dados:
        item.status = dados["status"]

    if "observacoes" in dados:
        item.observacoes = dados["observacoes"]

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return resposta_erro(
            "Erro ao editar item da produção.",
            status=500
        )

    return resposta_sucesso(
        "Item da produção atualizado com sucesso.",
        dados={
            "id": item.id,
            "producao_id": item.producao_id,
            "item_pedido_id": item.item_pedido_id,
            "quantidade": item.quantidade,
            "status": item.status,
            "observacoes": item.observacoes
        }
    )


@producao_bp.route(
    "/<int:producao_id>/itens/<int:item_id>",
    methods=["DELETE"]
)
@verificar_permissao("producao", "excluir")
def excluir_item_producao(producao_id, item_id):
    producao = db.session.get(Producao, producao_id)

    if not producao:
        return resposta_erro(
            "Produção não encontrada.",
            status=404
        )

    item = ItemProducao.query.filter_by(
        id=item_id,
        producao_id=producao_id
    ).first()

    if not item:
        return resposta_erro(
            "Item da produção não encontrado.",
            status=404
        )

    try:
        db.session.delete(item)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return resposta_erro(
            "Erro ao excluir item da produção.",
            status=500
        )

    return resposta_sucesso(
        "Item da produção excluído com sucesso."
    )


@producao_bp.route("/<int:producao_id>/materiais", methods=["POST"])
@verificar_permissao("producao", "editar")
def adicionar_material_producao(producao_id):

    producao = Producao.query.get(producao_id)

    if not producao:
        return resposta_erro(
            "Produção não encontrada.",
            status=404
        )

    dados = request.get_json() or {}

    erros = validar_material_producao(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            status=400,
            erros=erros
        )

    material = Material.query.get(dados["material_id"])

    if not material:
        return resposta_erro(
            "Material não encontrado.",
            status=404
        )

    material_existente = MaterialProducao.query.filter_by(
        producao_id=producao_id,
        material_id=dados["material_id"]
    ).first()

    if material_existente:
        return resposta_erro(
            "Este material já foi adicionado à produção.",
            status=409
        )

    novo_material = MaterialProducao(
        producao_id=producao_id,
        material_id=dados["material_id"],
        quantidade=float(dados["quantidade"]),
        observacoes=dados.get("observacoes")
    )

    try:
        db.session.add(novo_material)
        db.session.commit()

        return resposta_sucesso(
            "Material adicionado à produção com sucesso.",
            dados={
                "id": novo_material.id,
                "producao_id": novo_material.producao_id,
                "material_id": novo_material.material_id,
                "quantidade": novo_material.quantidade,
                "consumido": novo_material.consumido,
                "data_consumo": (
                    novo_material.data_consumo.isoformat()
                    if novo_material.data_consumo
                    else None
                ),
                "observacoes": novo_material.observacoes
            },
            status=201
        )

    except Exception:
        db.session.rollback()

        return resposta_erro(
            "Erro ao adicionar material à produção.",
            status=500
        )


@producao_bp.route("/<int:producao_id>/materiais", methods=["GET"])
@verificar_permissao("producao", "visualizar")
def listar_materiais_producao(producao_id):

    producao = Producao.query.get(producao_id)

    if not producao:
        return resposta_erro(
            "Produção não encontrada.",
            status=404
        )

    materiais = MaterialProducao.query.filter_by(
        producao_id=producao_id
    ).all()

    dados = []

    for item in materiais:
        dados.append({
            "id": item.id,
            "producao_id": item.producao_id,
            "material_id": item.material_id,
            "quantidade": item.quantidade,
            "consumido": item.consumido,
            "data_consumo": (
                item.data_consumo.isoformat()
                if item.data_consumo
                else None
            ),
            "observacoes": item.observacoes
        })

    return resposta_sucesso(
        "Materiais da produção encontrados.",
        dados=dados
    )


@producao_bp.route(
    "/<int:producao_id>/materiais/<int:material_producao_id>",
    methods=["GET"]
)
@verificar_permissao("producao", "visualizar")
def obter_material_producao(producao_id, material_producao_id):

    producao = Producao.query.get(producao_id)

    if not producao:
        return resposta_erro(
            "Produção não encontrada.",
            status=404
        )

    material_producao = MaterialProducao.query.filter_by(
        id=material_producao_id,
        producao_id=producao_id
    ).first()

    if not material_producao:
        return resposta_erro(
            "Material da produção não encontrado.",
            status=404
        )

    return resposta_sucesso(
        "Material da produção encontrado.",
        dados={
            "id": material_producao.id,
            "producao_id": material_producao.producao_id,
            "material_id": material_producao.material_id,
            "quantidade": material_producao.quantidade,
            "consumido": material_producao.consumido,
            "data_consumo": (
                material_producao.data_consumo.isoformat()
                if material_producao.data_consumo
                else None
            ),
            "observacoes": material_producao.observacoes
        }
    )


@producao_bp.route(
    "/<int:producao_id>/materiais/<int:material_producao_id>",
    methods=["PUT"]
)
@verificar_permissao("producao", "editar")
def editar_material_producao(producao_id, material_producao_id):

    producao = Producao.query.get(producao_id)

    if not producao:
        return resposta_erro(
            "Produção não encontrada.",
            status=404
        )

    material_producao = MaterialProducao.query.filter_by(
        id=material_producao_id,
        producao_id=producao_id
    ).first()

    if not material_producao:
        return resposta_erro(
            "Material da produção não encontrado.",
            status=404
        )

    dados = request.get_json() or {}

    erros = validar_edicao_material_producao(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            status=400,
            erros=erros
        )

    if "material_id" in dados:
        material = Material.query.get(dados["material_id"])

        if not material:
            return resposta_erro(
                "Material não encontrado.",
                status=404
            )

        material_existente = MaterialProducao.query.filter(
            MaterialProducao.producao_id == producao_id,
            MaterialProducao.material_id == dados["material_id"],
            MaterialProducao.id != material_producao_id
        ).first()

        if material_existente:
            return resposta_erro(
                "Este material já foi adicionado à produção.",
                status=409
            )

        material_producao.material_id = dados["material_id"]

    if "quantidade" in dados:
        material_producao.quantidade = float(dados["quantidade"])

    if "observacoes" in dados:
        material_producao.observacoes = dados["observacoes"]

    try:
        db.session.commit()

        return resposta_sucesso(
            "Material da produção atualizado com sucesso.",
            dados={
                "id": material_producao.id,
                "producao_id": material_producao.producao_id,
                "material_id": material_producao.material_id,
                "quantidade": material_producao.quantidade,
                "consumido": material_producao.consumido,
                "data_consumo": (
                    material_producao.data_consumo.isoformat()
                    if material_producao.data_consumo
                    else None
                ),
                "observacoes": material_producao.observacoes
            }
        )

    except Exception:
        db.session.rollback()

        return resposta_erro(
            "Erro ao atualizar material da produção.",
            status=500
        )


@producao_bp.route(
    "/<int:producao_id>/materiais/<int:material_producao_id>",
    methods=["DELETE"]
)
@verificar_permissao("producao", "excluir")
def excluir_material_producao(producao_id, material_producao_id):

    producao = Producao.query.get(producao_id)

    if not producao:
        return resposta_erro(
            "Produção não encontrada.",
            status=404
        )

    material_producao = MaterialProducao.query.filter_by(
        id=material_producao_id,
        producao_id=producao_id
    ).first()

    if not material_producao:
        return resposta_erro(
            "Material da produção não encontrado.",
            status=404
        )

    if material_producao.consumido:
        return resposta_erro(
            "Não é possível excluir um material que já foi consumido.",
            status=400
        )

    try:
        db.session.delete(material_producao)
        db.session.commit()

        return resposta_sucesso(
            "Material removido da produção com sucesso."
        )

    except Exception:
        db.session.rollback()

        return resposta_erro(
            "Erro ao remover material da produção.",
            status=500
        )


@producao_bp.route("/<int:producao_id>/consumir-materiais", methods=["POST"])
@verificar_permissao("producao", "editar")
def consumir_materiais(producao_id):

    producao = Producao.query.get(producao_id)

    if not producao:
        return resposta_erro(
            "Produção não encontrada.",
            404
        )

    if producao.status != "em_producao":
        return resposta_erro(
            "Os materiais só podem ser consumidos quando a produção estiver em produção.",
            400
        )

    materiais_producao = MaterialProducao.query.filter_by(
        producao_id=producao.id
    ).all()

    if not materiais_producao:
        return resposta_erro(
            "A produção não possui materiais cadastrados.",
            400
        )

    # Verifica se algum material já foi consumido
    materiais_ja_consumidos = [
        material for material in materiais_producao
        if material.consumido
    ]

    if materiais_ja_consumidos:
        return resposta_erro(
            "Os materiais desta produção já foram consumidos.",
            400
        )

    # PRIMEIRA ETAPA:
    # verificar todo o estoque antes de fazer qualquer alteração
    materiais_estoque = []

    for item in materiais_producao:

        material = Material.query.get(item.material_id)

        if not material:
            return resposta_erro(
                f"Material ID {item.material_id} não encontrado.",
                404
            )

        if material.quantidade < item.quantidade:
            return resposta_erro(
                f"Estoque insuficiente para o material '{material.nome}'. "
                f"Disponível: {material.quantidade}. "
                f"Necessário: {item.quantidade}.",
                400
            )

        materiais_estoque.append(
            (item, material)
        )

    # SEGUNDA ETAPA:
    # todos os materiais possuem estoque suficiente
    from flask_jwt_extended import get_jwt_identity

    usuario_id = get_jwt_identity()

    agora = datetime.now()

    movimentacoes = []

    for item, material in materiais_estoque:

        material.quantidade -= item.quantidade

        item.consumido = True
        item.data_consumo = agora

        movimentacao = MovimentacaoEstoque(
            material_id=material.id,
            tipo="saida",
            quantidade=item.quantidade,
            usuario_id=int(usuario_id),
            observacao=f"Consumo de material da Produção #{producao.id}"
        )

        db.session.add(movimentacao)

        movimentacoes.append({
            "material_id": material.id,
            "material": material.nome,
            "quantidade_consumida": item.quantidade,
            "estoque_atual": material.quantidade
        })

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()

        return resposta_erro(
            "Erro ao consumir materiais da produção.",
            500
        )

    return resposta_sucesso(
        "Materiais consumidos com sucesso.",
        {
            "producao_id": producao.id,
            "status_producao": producao.status,
            "materiais": movimentacoes
        }
    )