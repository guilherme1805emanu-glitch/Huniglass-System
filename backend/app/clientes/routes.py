from flask import Blueprint, jsonify, request
from app.clientes.models import Cliente
from database import db
from app.clientes.validators import validar_cliente
from app.common.responses import resposta_sucesso, resposta_erro
from flask_jwt_extended import jwt_required
from app.common.permissions import exigir_cargo, CARGOS, verificar_permissao


clientes_bp = Blueprint( "clientes", __name__, url_prefix= "/clientes")

@clientes_bp.route("/", methods= ["GET"])
@verificar_permissao("clientes", "visualizar")
def listar_clientes():
        clientes = Cliente.query.all()

        return jsonify([
                {
                    "id": cliente.id,
                    "nome": cliente.nome,
                    "telefone": cliente.telefone,
                    "email": cliente.email
                }
                for cliente in clientes
        ])
# ----------------------------------------------------------------------------------------

@clientes_bp.route("/", methods=["POST"])
@verificar_permissao("clientes", "criar")
def criar_cliente():

    dados = request.get_json()

    if not dados:
        return resposta_erro(
        "Nenhum dado foi enviado.",
        400
    )
    
    erros = validar_cliente(dados)

    if erros:
        return resposta_erro(
            "Os dados enviados são inválidos.",
            400,
            erros
    )
    
    cliente = Cliente(
        nome=dados["nome"],
        telefone=dados["telefone"],
        email=dados.get("email"),
        cpf_cnpj=dados.get("cpf_cnpj"),
        endereco=dados.get("endereco"),
        cidade=dados.get("cidade"),
        estado=dados.get("estado"),
        observacoes=dados.get("observacoes")
    )

    try:
        db.session.add(cliente)
        db.session.commit()

    except Exception as erro:
        db.session.rollback()

        return resposta_erro(
            "Erro ao salvar o cliente.",
            500
        )

    return resposta_sucesso(
        "Cliente criado com sucesso!",
        {"id": cliente.id},
        201
    )



# ------------------------------------------------------------------------------------

@clientes_bp.route("/<int:id>", methods=["GET"])
@verificar_permissao("clientes", "visualizar")
def buscar_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    return jsonify({
        "id": cliente.id,
        "nome": cliente.nome,
        "telefone": cliente.telefone,
        "email": cliente.email,
        "cpf_cnpj": cliente.cpf_cnpj,
        "endereco": cliente.endereco,
        "cidade": cliente.cidade,
        "estado": cliente.estado,
        "observacoes": cliente.observacoes
    })

# -------------------------------------------------------------------------

@clientes_bp.route("/<int:id>", methods=["PUT"])
@verificar_permissao("clientes", "editar")
def atualizar_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    dados = request.get_json()

    if not dados:
        return resposta_erro(
            "Nenhum dado foi enviado.",
            400
        )

    dados_atualizados = {
        "nome": dados.get("nome", cliente.nome),
        "telefone": dados.get("telefone", cliente.telefone),
        "email": dados.get("email", cliente.email),
        "cpf_cnpj": dados.get("cpf_cnpj", cliente.cpf_cnpj),
        "endereco": dados.get("endereco", cliente.endereco),
        "cidade": dados.get("cidade", cliente.cidade),
        "estado": dados.get("estado", cliente.estado),
        "observacoes": dados.get("observacoes", cliente.observacoes)
    }

    erros = validar_cliente(dados_atualizados, cliente_id=id)
    
    if erros:
        return resposta_erro(
            "Os dados enviados são inválidos.",
            400,
            erros
        )

    cliente.nome = dados_atualizados["nome"]
    cliente.telefone = dados_atualizados["telefone"]
    cliente.email = dados_atualizados["email"]
    cliente.cpf_cnpj = dados_atualizados["cpf_cnpj"]
    cliente.endereco = dados_atualizados["endereco"]
    cliente.cidade = dados_atualizados["cidade"]
    cliente.estado = dados_atualizados["estado"]
    cliente.observacoes = dados_atualizados["observacoes"]

    try:
        db.session.commit()

    except Exception as erro:
        db.session.rollback()

        return resposta_erro(
            "Erro ao atualizar o cliente.",
            500
        )

    return resposta_sucesso(
        "Cliente atualizado com sucesso!",
        {"id": cliente.id}
    )

# -----------------------------------------------------------------------------

@clientes_bp.route("/<int:id>", methods=["DELETE"])
@verificar_permissao("clientes", "excluir")
def excluir_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    try:
        db.session.delete(cliente)
        db.session.commit()

    except Exception as erro:
        db.session.rollback()

        return resposta_erro(
            "Erro ao excluir o cliente.",
            500
        )

    return resposta_sucesso(
        "Cliente excluído com sucesso!",
        {"id": id}
    )