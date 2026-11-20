from flask import Blueprint, request

from database import db
from app.estoque.models import Material, MovimentacaoEstoque, Fornecedor
from app.estoque.validators import validar_material, validar_movimentacao,validar_edicao_material, validar_fornecedor, validar_edicao_fornecedor

from app.common.responses import resposta_sucesso, resposta_erro
from app.common.permissions import verificar_permissao


estoque_bp = Blueprint(
    "estoque",
    __name__,
    url_prefix="/estoque"
)


# ------------------------------------------------------------------------------------------

@estoque_bp.route("/materiais", methods=["POST"])
@verificar_permissao("estoque", "criar")
def criar_material():

    dados = request.get_json()

    erros = validar_material(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    material = Material(
        nome=dados["nome"].strip(),
        categoria=dados["categoria"].strip(),
        unidade=dados["unidade"].strip(),
        quantidade=dados.get("quantidade", 0),
        estoque_minimo=dados.get("estoque_minimo", 0),
        fornecedor_id=dados.get("fornecedor_id"),
        ativo=dados.get("ativo", True),
        observacoes=dados.get("observacoes")
    )

    try:

        db.session.add(material)
        db.session.commit()

    except Exception:

        db.session.rollback()

        return resposta_erro(
            "Erro ao cadastrar o material.",
            500
        )

    return resposta_sucesso(
        "Material cadastrado com sucesso.",
        {
            "id": material.id,
            "nome": material.nome,
            "categoria": material.categoria,
            "unidade": material.unidade,
            "quantidade": material.quantidade,
            "estoque_minimo": material.estoque_minimo,
            "fornecedor_id": material.fornecedor_id,
            "ativo": material.ativo,
            "observacoes": material.observacoes
        },
        201
    )

# ------------------------------------------------------------------------------------------
# LISTAR MATERIAIS

@estoque_bp.route("/materiais", methods=["GET"])
@verificar_permissao("estoque", "visualizar")
def listar_materiais():

    materiais = Material.query.order_by(Material.nome.asc()).all()

    lista = []

    for material in materiais:
        lista.append({
            "id": material.id,
            "nome": material.nome,
            "categoria": material.categoria,
            "unidade": material.unidade,
            "quantidade": material.quantidade,
            "estoque_minimo": material.estoque_minimo,
            "fornecedor_id": material.fornecedor_id,
            "ativo": material.ativo
        })

    return resposta_sucesso(
        "Materiais encontrados com sucesso.",
        lista
    )

# ------------------------------------------------------------------------------------------
# CADASTRAR FORNECEDOR

@estoque_bp.route("/fornecedores", methods=["POST"])
@verificar_permissao("estoque", "criar")
def criar_fornecedor():

    dados = request.get_json()

    erros = validar_fornecedor(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    fornecedor = Fornecedor(
        nome=dados["nome"].strip(),
        telefone=dados.get("telefone"),
        email=dados.get("email"),
        cpf_cnpj=dados.get("cpf_cnpj"),
        endereco=dados.get("endereco"),
        cidade=dados.get("cidade"),
        estado=dados.get("estado"),
        observacoes=dados.get("observacoes"),
        ativo=dados.get("ativo", True)
    )

    try:

        db.session.add(fornecedor)
        db.session.commit()

    except Exception:

        db.session.rollback()

        return resposta_erro(
            "Erro ao cadastrar o fornecedor.",
            500
        )

    return resposta_sucesso(
        "Fornecedor cadastrado com sucesso.",
        {
            "id": fornecedor.id,
            "nome": fornecedor.nome,
            "telefone": fornecedor.telefone,
            "email": fornecedor.email,
            "cpf_cnpj": fornecedor.cpf_cnpj,
            "endereco": fornecedor.endereco,
            "cidade": fornecedor.cidade,
            "estado": fornecedor.estado,
            "observacoes": fornecedor.observacoes,
            "ativo": fornecedor.ativo
        },
        201
    )

# ------------------------------------------------------------------------------------------
# LISTAR FORNECEDORES

@estoque_bp.route("/fornecedores", methods=["GET"])
@verificar_permissao("estoque", "visualizar")
def listar_fornecedores():

    fornecedores = Fornecedor.query.order_by(
        Fornecedor.nome.asc()
    ).all()

    lista = []

    for fornecedor in fornecedores:

        lista.append({
            "id": fornecedor.id,
            "nome": fornecedor.nome,
            "telefone": fornecedor.telefone,
            "email": fornecedor.email,
            "cpf_cnpj": fornecedor.cpf_cnpj,
            "endereco": fornecedor.endereco,
            "cidade": fornecedor.cidade,
            "estado": fornecedor.estado,
            "observacoes": fornecedor.observacoes,
            "ativo": fornecedor.ativo
        })

    return resposta_sucesso(
        "Fornecedores encontrados com sucesso.",
        lista
    )


# ------------------------------------------------------------------------------------------
# BUSCAR FORNECEDOR POR ID

@estoque_bp.route("/fornecedores/<int:fornecedor_id>", methods=["GET"])
@verificar_permissao("estoque", "visualizar")
def buscar_fornecedor(fornecedor_id):

    fornecedor = db.session.get(Fornecedor, fornecedor_id)

    if not fornecedor:
        return resposta_erro(
            "Fornecedor não encontrado.",
            404
        )

    return resposta_sucesso(
        "Fornecedor encontrado com sucesso.",
        {
            "id": fornecedor.id,
            "nome": fornecedor.nome,
            "telefone": fornecedor.telefone,
            "email": fornecedor.email,
            "cpf_cnpj": fornecedor.cpf_cnpj,
            "endereco": fornecedor.endereco,
            "cidade": fornecedor.cidade,
            "estado": fornecedor.estado,
            "observacoes": fornecedor.observacoes,
            "ativo": fornecedor.ativo
        }
    )



# ------------------------------------------------------------------------------------------
# EDITAR FORNECEDOR

@estoque_bp.route("/fornecedores/<int:fornecedor_id>", methods=["PUT"])
@verificar_permissao("estoque", "editar")
def editar_fornecedor(fornecedor_id):

    fornecedor = db.session.get(Fornecedor, fornecedor_id)

    if not fornecedor:
        return resposta_erro(
            "Fornecedor não encontrado.",
            404
        )

    dados = request.get_json()

    if not dados:
        return resposta_erro(
            "Nenhum dado foi enviado.",
            400
        )

    erros = validar_edicao_fornecedor(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    if "nome" in dados:
        fornecedor.nome = dados["nome"].strip()

    if "telefone" in dados:
        fornecedor.telefone = dados["telefone"]

    if "email" in dados:
        fornecedor.email = dados["email"]

    if "cpf_cnpj" in dados:
        fornecedor.cpf_cnpj = dados["cpf_cnpj"]

    if "endereco" in dados:
        fornecedor.endereco = dados["endereco"]

    if "cidade" in dados:
        fornecedor.cidade = dados["cidade"]

    if "estado" in dados:
        fornecedor.estado = dados["estado"]

    if "observacoes" in dados:
        fornecedor.observacoes = dados["observacoes"]

    if "ativo" in dados:
        fornecedor.ativo = dados["ativo"]

    try:

        db.session.commit()

    except Exception:

        db.session.rollback()

        return resposta_erro(
            "Erro ao editar o fornecedor.",
            500
        )

    return resposta_sucesso(
        "Fornecedor atualizado com sucesso.",
        {
            "id": fornecedor.id,
            "nome": fornecedor.nome,
            "telefone": fornecedor.telefone,
            "email": fornecedor.email,
            "cpf_cnpj": fornecedor.cpf_cnpj,
            "endereco": fornecedor.endereco,
            "cidade": fornecedor.cidade,
            "estado": fornecedor.estado,
            "observacoes": fornecedor.observacoes,
            "ativo": fornecedor.ativo
        }
    )

# ------------------------------------------------------------------------------------------
# EXCLUIR FORNECEDOR

@estoque_bp.route("/fornecedores/<int:fornecedor_id>", methods=["DELETE"])
@verificar_permissao("estoque", "excluir")
def excluir_fornecedor(fornecedor_id):

    fornecedor = db.session.get(Fornecedor, fornecedor_id)

    if not fornecedor:
        return resposta_erro(
            "Fornecedor não encontrado.",
            404
        )

    # Impede exclusão se o fornecedor estiver vinculado a materiais
    if fornecedor.materiais:
        return resposta_erro(
            "Não é possível excluir o fornecedor porque ele está vinculado a materiais.",
            400
        )

    try:

        db.session.delete(fornecedor)
        db.session.commit()

    except Exception:

        db.session.rollback()

        return resposta_erro(
            "Erro ao excluir o fornecedor.",
            500
        )

    return resposta_sucesso(
        "Fornecedor excluído com sucesso."
    )

# -------------------------------------------------------------------------------------------------------
# BUSCAR MATERIAL POR ID


@estoque_bp.route("/materiais/<int:material_id>", methods=["GET"])
@verificar_permissao("estoque", "visualizar")
def buscar_material(material_id):

    material = db.session.get(Material, material_id)

    if not material:
        return resposta_erro(
            "Material não encontrado.",
            404
        )

    return resposta_sucesso(
        "Material encontrado com sucesso.",
        {
            "id": material.id,
            "nome": material.nome,
            "categoria": material.categoria,
            "unidade": material.unidade,
            "quantidade": material.quantidade,
            "estoque_minimo": material.estoque_minimo,
            "fornecedor_id": material.fornecedor_id,          
            "ativo": material.ativo,
            "observacoes": material.observacoes
        }
    )


# ------------------------------------------------------------------------------------------
# EDITAR MATERIAL

@estoque_bp.route("/materiais/<int:material_id>", methods=["PUT"])
@verificar_permissao("estoque", "editar")
def editar_material(material_id):

    material = db.session.get(Material, material_id)

    if not material:
        return resposta_erro(
            "Material não encontrado.",
            404
        )

    dados = request.get_json()

    if not dados:
        return resposta_erro(
            "Nenhum dado foi enviado.",
            400
        )

    # Validação
    erros = validar_edicao_material(dados)
    
    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    if "nome" in dados:
        material.nome = dados["nome"].strip()

    if "categoria" in dados:
        material.categoria = dados["categoria"].strip()

    if "unidade" in dados:
        material.unidade = dados["unidade"].strip()

    if "quantidade" in dados:
        material.quantidade = dados["quantidade"]

    if "estoque_minimo" in dados:
        material.estoque_minimo = dados["estoque_minimo"]

    if "fornecedor_id" in dados:

        fornecedor_id = dados["fornecedor_id"]

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

        material.fornecedor_id = fornecedor_id

    if "ativo" in dados:
        material.ativo = dados["ativo"]

    if "observacoes" in dados:
        material.observacoes = dados["observacoes"]

    try:

        db.session.commit()

    except Exception:

        db.session.rollback()

        return resposta_erro(
            "Erro ao editar o material.",
            500
        )

    return resposta_sucesso(
        "Material atualizado com sucesso.",
        {
            "id": material.id,
            "nome": material.nome,
            "categoria": material.categoria,
            "unidade": material.unidade,
            "quantidade": material.quantidade,
            "estoque_minimo": material.estoque_minimo,
            "fornecedor_id": material.fornecedor_id,
            "ativo": material.ativo,
            "observacoes": material.observacoes
        }
    )


# ------------------------------------------------------------------------------------------
# EXCLUIR MATERIAL

@estoque_bp.route("/materiais/<int:material_id>", methods=["DELETE"])
@verificar_permissao("estoque", "excluir")
def excluir_material(material_id):

    material = db.session.get(Material, material_id)

    if not material:
        return resposta_erro(
            "Material não encontrado.",
            404
        )

    try:

        db.session.delete(material)
        db.session.commit()

    except Exception:

        db.session.rollback()

        return resposta_erro(
            "Erro ao excluir o material.",
            500
        )

    return resposta_sucesso(
        "Material excluído com sucesso."
    )

# ------------------------------------------------------------------------------------------
# REGISTRAR MOVIMENTAÇÃO DE ESTOQUE

@estoque_bp.route("/movimentacoes", methods=["POST"])
@verificar_permissao("estoque", "criar")
def criar_movimentacao():

    dados = request.get_json()

    erros = validar_movimentacao(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    material = db.session.get(
        Material,
        dados["material_id"]
    )

    if not material:
        return resposta_erro(
            "Material não encontrado.",
            404
        )

    tipo = dados["tipo"].lower()
    quantidade = dados["quantidade"]

    # Impede saída maior que o estoque disponível
    if tipo == "saida" and quantidade > material.quantidade:
        return resposta_erro(
            "Quantidade insuficiente em estoque.",
            400
        )

    # Descobre o usuário através do JWT
    from flask_jwt_extended import get_jwt_identity

    usuario_id = get_jwt_identity()

    # Atualiza o estoque
    if tipo == "entrada":
        material.quantidade += quantidade
    else:
        material.quantidade -= quantidade

    movimentacao = MovimentacaoEstoque(
        material_id=material.id,
        tipo=tipo,
        quantidade=quantidade,
        usuario_id=int(usuario_id),
        observacao=dados.get("observacao")
    )

    try:

        db.session.add(movimentacao)
        db.session.commit()

    except Exception:

        db.session.rollback()

        return resposta_erro(
            "Erro ao registrar movimentação.",
            500
        )

    return resposta_sucesso(
        "Movimentação registrada com sucesso.",
        {
            "id": movimentacao.id,
            "material_id": material.id,
            "material": material.nome,
            "tipo": movimentacao.tipo,
            "quantidade": movimentacao.quantidade,
            "estoque_atual": material.quantidade,
            "usuario_id": movimentacao.usuario_id,
            "data": movimentacao.data,
            "observacao": movimentacao.observacao
        },
        201
    )


# ------------------------------------------------------------------------------------------
# LISTAR HISTÓRICO DE MOVIMENTAÇÕES

@estoque_bp.route("/movimentacoes", methods=["GET"])
@verificar_permissao("estoque", "visualizar")
def listar_movimentacoes():

    movimentacoes = MovimentacaoEstoque.query.order_by(
        MovimentacaoEstoque.data.desc()
    ).all()

    lista = []

    for movimentacao in movimentacoes:

        lista.append({
            "id": movimentacao.id,

            "material": {
                "id": movimentacao.material.id,
                "nome": movimentacao.material.nome
            },

            "tipo": movimentacao.tipo,
            "quantidade": movimentacao.quantidade,

            "usuario": {
                "id": movimentacao.usuario.id,
                "nome": movimentacao.usuario.nome
            },

            "data": movimentacao.data,
            "observacao": movimentacao.observacao
        })

    return resposta_sucesso(
        "Histórico de movimentações encontrado com sucesso.",
        lista
    )

# ------------------------------------------------------------------------------------------
# LISTAR MOVIMENTAÇÕES DE UM MATERIAL

@estoque_bp.route(
    "/materiais/<int:material_id>/movimentacoes",
    methods=["GET"]
)
@verificar_permissao("estoque", "visualizar")
def listar_movimentacoes_material(material_id):

    material = db.session.get(
        Material,
        material_id
    )

    if not material:
        return resposta_erro(
            "Material não encontrado.",
            404
        )

    movimentacoes = MovimentacaoEstoque.query.filter_by(
        material_id=material_id
    ).order_by(
        MovimentacaoEstoque.data.desc()
    ).all()

    lista = []

    for movimentacao in movimentacoes:

        lista.append({
            "id": movimentacao.id,
            "tipo": movimentacao.tipo,
            "quantidade": movimentacao.quantidade,

            "usuario": {
                "id": movimentacao.usuario.id,
                "nome": movimentacao.usuario.nome
            },

            "data": movimentacao.data,
            "observacao": movimentacao.observacao
        })

    return resposta_sucesso(
        "Movimentações do material encontradas com sucesso.",
        lista
    )