from flask import Blueprint, request
from database import db
from app.auth.models import Usuario
from app.common.responses import resposta_sucesso, resposta_erro
from app.common.permissions import verificar_permissao, CARGOS

from app.clientes.models import Cliente
from sqlalchemy import func

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)
# ------------------------------------------------------------------------------------

@auth_bp.route("/usuarios", methods=["POST"])
@verificar_permissao("usuarios", "criar")
def criar_usuario():

    dados = request.get_json()

    if not dados:
        return resposta_erro(
            "Nenhum dado foi enviado.",
            400
        )

    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")
    cargo = dados.get("cargo")

    if not nome or not email or not senha or not cargo:
        return resposta_erro(
            "Nome, email, senha e cargo são obrigatórios.",
            400
        )

    if cargo not in CARGOS.values():
        return resposta_erro("Cargo inválido.", 400)

    usuario_existente = Usuario.query.filter_by(
        email=email
    ).first()

    if usuario_existente:
        return resposta_erro(
            "Este email já está cadastrado.",
            400
        )

    usuario = Usuario(
        nome=nome,
        email=email,
        cargo=cargo
    )

    usuario.definir_senha(senha)

    try:
        db.session.add(usuario)
        db.session.commit()

    except Exception as erro:
        db.session.rollback()

        return resposta_erro(
            "Erro ao cadastrar o usuário.",
            500
        )

    return resposta_sucesso(
        "Usuário criado com sucesso!",
        {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "cargo": usuario.cargo
        },
        201
    )
# ------------------------------------------------------------------------------------------


@auth_bp.route("/cadastro-cliente", methods=["POST"])
def cadastrar_cliente():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return resposta_erro("Envie os dados do cadastro.", 400)

    nome = dados.get("nome")
    email = dados.get("email")
    telefone = dados.get("telefone")
    cpf_cnpj = dados.get("cpf_cnpj") or None
    senha = dados.get("senha")

    # Validar os campos recebidos
    if not all(isinstance(valor, str) for valor in (nome, email, telefone, senha)):
        return resposta_erro(
            "Nome, e-mail, telefone e senha são obrigatórios.",
            400
        )

    nome = nome.strip()
    email = email.strip().lower()
    telefone = telefone.strip()
    cpf_cnpj = cpf_cnpj.strip() if cpf_cnpj else None

    if not nome or not email or not telefone or not senha:
        return resposta_erro(
            "Preencha todos os campos obrigatórios.",
            400
        )

    if len(nome) > 150 or len(email) > 150 or len(telefone) > 20:
        return resposta_erro("Um ou mais campos excedem o limite permitido.", 400)

    if cpf_cnpj and len(cpf_cnpj) > 20:
        return resposta_erro("CPF/CNPJ excede o limite permitido.", 400)

    if "@" not in email or email.startswith("@") or email.endswith("@"):
        return resposta_erro("Informe um e-mail válido.", 400)

    if len(senha) < 8:
        return resposta_erro(
            "A senha deve possuir pelo menos 8 caracteres.",
            400
        )

    # Não permitir contas duplicadas, inclusive com diferenças de maiúsculas.
    usuario_existente = Usuario.query.filter(
        func.lower(Usuario.email) == email
    ).first()

    if usuario_existente:
        return resposta_erro(
            "Este e-mail já possui uma conta. Faça login ou utilize outro e-mail.",
            409
        )

    # Não associar automaticamente uma conta a um cadastro comercial antigo.
    # Essa associação precisará de um processo seguro de verificação.
    cliente_existente = Cliente.query.filter(
        func.lower(Cliente.email) == email
    ).first()

    if cliente_existente:
        return resposta_erro(
            "Este e-mail já consta no cadastro comercial. Entre em contato com a equipe para vincular sua conta.",
            409
        )

    usuario = Usuario(
        nome=nome,
        email=email,
        cargo="cliente",
        ativo=True
    )
    usuario.definir_senha(senha)

    cliente = Cliente(
        nome=nome,
        email=email,
        telefone=telefone,
        cpf_cnpj=cpf_cnpj
    )

    try:
        # As duas gravações são confirmadas juntas.
        db.session.add(usuario)
        db.session.add(cliente)
        db.session.commit()

    except Exception:
        db.session.rollback()
        return resposta_erro(
            "Não foi possível concluir o cadastro. Tente novamente.",
            500
        )

    return resposta_sucesso(
        "Cadastro realizado com sucesso! Você já pode entrar.",
        {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "cargo": usuario.cargo
        },
        201
    )

# -------------------------------------------------------------------------------------------------



@auth_bp.route("/login", methods=["POST"])
def login():

    dados = request.get_json()

    if not dados:
        return resposta_erro(
            "Nenhum dado foi enviado.",
            400
        )

    email = dados.get("email")
    senha = dados.get("senha")

    if not email or not senha:
        return resposta_erro(
            "Email e senha são obrigatórios.",
            400
        )

    usuario = Usuario.query.filter_by(
        email=email
    ).first()

    if not usuario:
        return resposta_erro(
            "Email ou senha inválidos.",
            401
        )

    if not usuario.verificar_senha(senha):
        return resposta_erro(
            "Email ou senha inválidos.",
            401
        )

    if not usuario.ativo:
        return resposta_erro(
            "Usuário inativo.",
            403
        )

    token = create_access_token(
        identity=str(usuario.id),
        additional_claims={
            "cargo": usuario.cargo
        }
    )

    return resposta_sucesso(
        "Login realizado com sucesso!",
        {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "cargo": usuario.cargo,
            "token": token
        }
    )

# -----------------------------------------------------------------------------------------

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def usuario_atual():

    usuario_id = get_jwt_identity()

    usuario = db.session.get(Usuario, usuario_id)

    if not usuario:
        return resposta_erro(
            "Usuário não encontrado.",
            404
        )

    return resposta_sucesso(
        "Usuário autenticado.",
        {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "cargo": usuario.cargo,
            "ativo": usuario.ativo
        }
    )
# --------------------------------------------------------------------------------------

@auth_bp.route("/usuarios", methods=["GET"])
@verificar_permissao("usuarios", "visualizar")
def listar_usuarios():

    usuarios = Usuario.query.all()

    lista_usuarios = []

    for usuario in usuarios:
        lista_usuarios.append({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "cargo": usuario.cargo,
            "ativo": usuario.ativo
        })

    return resposta_sucesso(
        "Usuários encontrados com sucesso.",
        lista_usuarios
    )

# ------------------------------------------------------------------------------------------

@auth_bp.route("/usuarios/<int:usuario_id>", methods=["GET"])
@verificar_permissao("usuarios", "visualizar")
def buscar_usuario(usuario_id):

    usuario = db.session.get(Usuario, usuario_id)

    if not usuario:
        return resposta_erro(
            "Usuário não encontrado.",
            404
        )

    return resposta_sucesso(
        "Usuário encontrado com sucesso.",
        {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "cargo": usuario.cargo,
            "ativo": usuario.ativo
        }
    )

# ------------------------------------------------------------------------------------------

@auth_bp.route("/usuarios/<int:usuario_id>", methods=["PUT"])
@verificar_permissao("usuarios", "editar")
def editar_usuario(usuario_id):

    usuario = db.session.get(Usuario, usuario_id)

    if not usuario:
        return resposta_erro(
            "Usuário não encontrado.",
            404
        )

    dados = request.get_json()

    if not dados:
        return resposta_erro(
            "Nenhum dado foi enviado.",
            400
        )

    nome = dados.get("nome")
    email = dados.get("email")
    cargo = dados.get("cargo")
    ativo = dados.get("ativo")

    if nome is not None:
        if not nome.strip():
            return resposta_erro(
                "O nome não pode estar vazio.",
                400
            )

        usuario.nome = nome.strip()

    if email is not None:

        usuario_existente = Usuario.query.filter(
            Usuario.email == email,
            Usuario.id != usuario.id
        ).first()

        if usuario_existente:
            return resposta_erro(
                "Este email já está cadastrado.",
                400
            )

        usuario.email = email

    if cargo is not None:
        if cargo not in CARGOS.values():
            return resposta_erro("Cargo inválido.", 400)
        usuario.cargo = cargo    

    if ativo is not None:

        if not isinstance(ativo, bool):
            return resposta_erro(
                "O campo ativo deve ser verdadeiro ou falso.",
                400
            )

        usuario.ativo = ativo

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()

        return resposta_erro(
            "Erro ao editar o usuário.",
            500
        )

    return resposta_sucesso(
        "Usuário atualizado com sucesso.",
        {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "cargo": usuario.cargo,
            "ativo": usuario.ativo
        }
    )

# ------------------------------------------------------------------------------------------

@auth_bp.route("/usuarios/<int:usuario_id>/senha", methods=["PUT"])
@verificar_permissao("usuarios", "editar")
def alterar_senha(usuario_id):

    usuario = db.session.get(Usuario, usuario_id)

    if not usuario:
        return resposta_erro(
            "Usuário não encontrado.",
            404
        )

    dados = request.get_json()

    if not dados:
        return resposta_erro(
            "Nenhum dado foi enviado.",
            400
        )

    nova_senha = dados.get("nova_senha")

    if not nova_senha:
        return resposta_erro(
            "A nova senha é obrigatória.",
            400
        )

    if len(nova_senha) < 6:
        return resposta_erro(
            "A nova senha deve possuir pelo menos 6 caracteres.",
            400
        )

    usuario.definir_senha(nova_senha)

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()

        return resposta_erro(
            "Erro ao alterar a senha.",
            500
        )

    return resposta_sucesso(
        "Senha alterada com sucesso.",
        {
            "id": usuario.id,
            "nome": usuario.nome
        }
    )

# ------------------------------------------------------------------------------------------