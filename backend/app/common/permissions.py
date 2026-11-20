from functools import wraps

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt
from flask import jsonify

from database import db
from app.auth.models import Usuario

CARGOS = {
    "SOCIO": "socio",
    "ADMINISTRATIVO": "administrativo",
    "PRODUCAO": "producao",
    "INSTALADOR": "instalador",
    "MOTORISTA": "motorista"
}

PERMISSOES = {
    "clientes": {
        "visualizar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"]
        ],
        "criar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"]
        ],
        "editar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"]
        ],
        "excluir": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"]
        ]
    },
    
    "usuarios": {
        "visualizar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"]
        ],
        "criar": [
            CARGOS["SOCIO"]
        ],
        "editar": [
            CARGOS["SOCIO"]
        ]
    },

    "estoque": {
        "visualizar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"]
        ],
        "criar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"]
        ],
        "editar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"]
        ],
        "excluir": [
            CARGOS["SOCIO"]
        ]
    },

    "medicoes": {
        "visualizar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"]
        ],
        "criar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"]
        ],
        "editar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"]
        ],
        "excluir": [
            CARGOS["SOCIO"]
        ]
    },

    "orcamentos": {
        "visualizar": [
            CARGOS["SOCIO"], 
            CARGOS["ADMINISTRATIVO"]
        ],
        "criar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"]
        ],
        "editar": [
            CARGOS["SOCIO"], 
            CARGOS["ADMINISTRATIVO"]
        ],
        "excluir": [
            CARGOS["SOCIO"]
        ]
    },

    "pedidos": {
        "visualizar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"]
        ],
        "criar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"]
        ],
        "editar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"]
        ],
        "excluir": [
            CARGOS["SOCIO"]
        ]
    },    
    "financeiro": {
        "visualizar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"]
        ],
        "criar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"]
        ],
        "editar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"]
        ],
        "excluir": [
            CARGOS["SOCIO"]
        ]
    },


    "producao": {
        "visualizar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"],
            CARGOS["PRODUCAO"]
        ],
        "criar": [
            CARGOS["SOCIO"],
            CARGOS["PRODUCAO"]
        ],
        "editar": [
            CARGOS["SOCIO"],
            CARGOS["PRODUCAO"]
        ],
        "excluir": [
            CARGOS["SOCIO"]
        ]
    },

    "instalacoes": {
        "visualizar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"],
            CARGOS["INSTALADOR"]
        ],
        "criar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"]
        ],
        "editar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"],
            CARGOS["INSTALADOR"]
        ],
        "excluir": [
            CARGOS["SOCIO"]
        ]
    },

    "agenda": {
        "visualizar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"],
            CARGOS["PRODUCAO"],
            CARGOS["INSTALADOR"],
            CARGOS["MOTORISTA"]
        ],
        "criar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"]
        ],
        "editar": [
            CARGOS["SOCIO"],
            CARGOS["ADMINISTRATIVO"],
            CARGOS["PRODUCAO"],
            CARGOS["INSTALADOR"],
            CARGOS["MOTORISTA"]
        ],
        "excluir": [
            CARGOS["SOCIO"]
        ]
    },

    "relatorios": {
        "visualizar": [
            CARGOS ["SOCIO"], 
            CARGOS ["ADMINISTRATIVO"]
        ]
    },
    
}

def verificar_permissao(modulo, acao):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            usuario_id = get_jwt_identity()
            usuario = db.session.get(Usuario, usuario_id)

            if not usuario:
                return jsonify({
                    "sucesso": False,
                    "mensagem": "Usuário não encontrado."
                }), 404

            if not usuario.ativo:
                return jsonify({
                    "sucesso": False,
                    "mensagem": "Usuário inativo."
                }), 403

            cargo = usuario.cargo

            permissoes_modulo = PERMISSOES.get(modulo)

            if not permissoes_modulo:
                return jsonify({
                    "sucesso": False,
                    "mensagem": "Módulo não encontrado."
                }), 404

            cargos_permitidos = permissoes_modulo.get(acao, [])

            if cargo not in cargos_permitidos:
                return jsonify({
                    "sucesso": False,
                    "mensagem": "Você não tem permissão para realizar esta ação."
                }), 403

            return func(*args, **kwargs)

        return wrapper
    return decorator
# ------------------------------------------------------------------------------------------------------
def exigir_cargo(*cargos):
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            verify_jwt_in_request()

            usuario_id = get_jwt_identity()

            usuario = db.session.get(Usuario, usuario_id)

            if not usuario:
                return jsonify({
                    "sucesso": False,
                    "mensagem": "Usuário não encontrado."
                }), 404

            if not usuario.ativo:
                return jsonify({
                    "sucesso": False,
                    "mensagem": "Usuário inativo."
                }), 403

            cargo = usuario.cargo

            if cargo not in cargos:
                return jsonify({
                    "sucesso": False,
                    "mensagem": "Você não tem permissão para realizar esta ação."
                }), 403

            return func(*args, **kwargs)

        return wrapper

    return decorator


def verificar_responsavel_agenda(atividade):
    """
    Verifica se o usuário logado pode alterar a atividade da agenda.

    - socio: pode alterar qualquer atividade
    - administrativo: pode alterar qualquer atividade
    - producao: somente atividades próprias
    - instalador: somente atividades próprias
    - motorista: somente atividades próprias
    """

    usuario_id = int(get_jwt_identity())

    usuario = db.session.get(Usuario, usuario_id)

    if not usuario:
        return False, "Usuário não encontrado."

    if not usuario.ativo:
        return False, "Usuário inativo."

    # Sócio e administrativo podem gerenciar
    # atividades de qualquer responsável.
    if usuario.cargo in [
        CARGOS["SOCIO"],
        CARGOS["ADMINISTRATIVO"]
    ]:
        return True, None

    # Cargos operacionais só podem alterar
    # atividades atribuídas a eles mesmos.
    if atividade.usuario_id != usuario_id:
        return False, "Você só pode alterar atividades atribuídas a você."

    return True, None