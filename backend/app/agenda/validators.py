from datetime import datetime


TIPOS_AGENDA = [
    "medicao",
    "instalacao",
    "retirada",
    "entrega",
    "producao",
    "outro"
]

STATUS_AGENDA = [
    "agendado",
    "em_andamento",
    "concluido",
    "cancelado"
]

CARGOS_POR_TIPO = {
    "instalacao": [
        "instalador",
        "socio"
    ],

    "retirada": [
        "motorista",
        "socio"
    ],

    "entrega": [
        "motorista",
        "socio"
    ],

    "medicao": [
        "socio",
        "administrativo"
    ],

    "producao": [
        "socio",
        "producao"
    ],

    "outro": [
        "socio",
        "administrativo",
        "producao",
        "instalador",
        "motorista"
    ]
}

def validar_agenda(dados):
    erros = {}

    if "tipo" not in dados:
        erros["tipo"] = "O tipo da atividade é obrigatório."
    elif dados["tipo"] not in TIPOS_AGENDA:
        erros["tipo"] = (
            "Tipo inválido. Use: medicao, instalacao, retirada, entrega ou outro."
        )

    if "usuario_id" not in dados:
        erros["usuario_id"] = "O responsável é obrigatório."

    if "data_inicio" not in dados:
        erros["data_inicio"] = "A data de início é obrigatória."
    else:
        try:
            datetime.fromisoformat(dados["data_inicio"])
        except (ValueError, TypeError):
            erros["data_inicio"] = (
                "A data de início deve estar em formato ISO válido."
            )

    if "data_fim" in dados and dados["data_fim"] is not None:
        try:
            datetime.fromisoformat(dados["data_fim"])
        except (ValueError, TypeError):
            erros["data_fim"] = (
                "A data de fim deve estar em formato ISO válido."
            )

    if "status" in dados:
        if dados["status"] not in STATUS_AGENDA:
            erros["status"] = (
                "Status inválido. Use: agendado, em_andamento, "
                "concluido ou cancelado."
            )

    if "cliente_id" in dados and dados["cliente_id"] is not None:
        if not isinstance(dados["cliente_id"], int):
            erros["cliente_id"] = "O cliente_id deve ser um número inteiro."

    if "pedido_id" in dados and dados["pedido_id"] is not None:
        if not isinstance(dados["pedido_id"], int):
            erros["pedido_id"] = "O pedido_id deve ser um número inteiro."

    if "descricao" in dados and dados["descricao"] is not None:
        if not str(dados["descricao"]).strip():
            erros["descricao"] = "A descrição não pode estar vazia."

    if "endereco" in dados and dados["endereco"] is not None:
        if not str(dados["endereco"]).strip():
            erros["endereco"] = "O endereço não pode estar vazio."

    return erros


def validar_edicao_agenda(dados):
    erros = {}

    if "tipo" in dados:
        if dados["tipo"] not in TIPOS_AGENDA:
            erros["tipo"] = (
                "Tipo inválido. Use: medicao, instalacao, retirada, entrega ou outro."
            )

    if "usuario_id" in dados and dados["usuario_id"] is None:
        erros["usuario_id"] = "O responsável não pode ser nulo."

    if "data_inicio" in dados:
        try:
            datetime.fromisoformat(dados["data_inicio"])
        except (ValueError, TypeError):
            erros["data_inicio"] = (
                "A data de início deve estar em formato ISO válido."
            )

    if "data_fim" in dados and dados["data_fim"] is not None:
        try:
            datetime.fromisoformat(dados["data_fim"])
        except (ValueError, TypeError):
            erros["data_fim"] = (
                "A data de fim deve estar em formato ISO válido."
            )

    if "status" in dados:
        if dados["status"] not in STATUS_AGENDA:
            erros["status"] = (
                "Status inválido. Use: agendado, em_andamento, "
                "concluido ou cancelado."
            )

    if "cliente_id" in dados and dados["cliente_id"] is not None:
        if not isinstance(dados["cliente_id"], int):
            erros["cliente_id"] = "O cliente_id deve ser um número inteiro."

    if "pedido_id" in dados and dados["pedido_id"] is not None:
        if not isinstance(dados["pedido_id"], int):
            erros["pedido_id"] = "O pedido_id deve ser um número inteiro."

    if "descricao" in dados and dados["descricao"] is not None:
        if not str(dados["descricao"]).strip():
            erros["descricao"] = "A descrição não pode estar vazia."

    if "endereco" in dados and dados["endereco"] is not None:
        if not str(dados["endereco"]).strip():
            erros["endereco"] = "O endereço não pode estar vazio."

    return erros


def validar_conflito_agenda(
    usuario_id,
    data_inicio,
    data_fim,
    agenda_id=None
):
    from app.agenda.models import Agenda

    query = Agenda.query.filter(
        Agenda.usuario_id == usuario_id,
        Agenda.status.in_(["agendado", "em_andamento"])
    )

    if agenda_id is not None:
        query = query.filter(
            Agenda.id != agenda_id
        )

    atividades = query.all()

    for atividade in atividades:

        inicio_existente = atividade.data_inicio
        fim_existente = atividade.data_fim

        # Atividade sem horário de fim:
        # consideramos que ela ocupa o horário até nova definição.
        if fim_existente is None:
            if data_fim is None:
                return True

            if data_inicio <= inicio_existente:
                return True

            continue

        # Nova atividade sem fim
        if data_fim is None:
            if data_inicio < fim_existente:
                return True

            continue

        # Verificar sobreposição normal
        if (
            data_inicio < fim_existente
            and data_fim > inicio_existente
        ):
            return True

    return False