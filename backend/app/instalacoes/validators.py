def validar_instalacao(dados):
    erros = {}

    if not dados.get("pedido_id"):
        erros["pedido_id"] = "Pedido é obrigatório."

    if not dados.get("usuario_id"):
        erros["usuario_id"] = "Usuário é obrigatório."

    if not dados.get("instalador_id"):
        erros["instalador_id"] = "Instalador é obrigatório."

    if not dados.get("endereco"):
        erros["endereco"] = "Endereço é obrigatório."
    elif not isinstance(dados["endereco"], str):
        erros["endereco"] = "Endereço deve ser um texto."
    elif not dados["endereco"].strip():
        erros["endereco"] = "Endereço não pode estar vazio."

    status_validos = [
        "agendada",
        "em_andamento",
        "concluida",
        "cancelada"
    ]

    if "status" in dados:
        if dados["status"] not in status_validos:
            erros["status"] = "Status inválido."

    if "observacoes" in dados:
        if dados["observacoes"] is not None:
            if not isinstance(dados["observacoes"], str):
                erros["observacoes"] = "Observações devem ser um texto."

    return erros


def validar_edicao_instalacao(dados):
    erros = {}

    if "pedido_id" in dados:
        if not dados["pedido_id"]:
            erros["pedido_id"] = "Pedido é obrigatório."

    if "usuario_id" in dados:
        if not dados["usuario_id"]:
            erros["usuario_id"] = "Usuário é obrigatório."

    if "instalador_id" in dados:
        if not dados["instalador_id"]:
            erros["instalador_id"] = "Instalador é obrigatório."

    if "endereco" in dados:
        if not dados["endereco"]:
            erros["endereco"] = "Endereço é obrigatório."
        elif not isinstance(dados["endereco"], str):
            erros["endereco"] = "Endereço deve ser um texto."
        elif not dados["endereco"].strip():
            erros["endereco"] = "Endereço não pode estar vazio."

    status_validos = [
        "agendada",
        "em_andamento",
        "concluida",
        "cancelada"
    ]

    if "status" in dados:
        if dados["status"] not in status_validos:
            erros["status"] = "Status inválido."

    if "observacoes" in dados:
        if dados["observacoes"] is not None:
            if not isinstance(dados["observacoes"], str):
                erros["observacoes"] = "Observações devem ser um texto."

    if "data_inicio" in dados:
        erros["data_inicio"] = (
            "Data de início é definida automaticamente pelo sistema."
        )

    if "data_conclusao" in dados:
        erros["data_conclusao"] = (
            "Data de conclusão é definida automaticamente pelo sistema."
        )

    return erros
