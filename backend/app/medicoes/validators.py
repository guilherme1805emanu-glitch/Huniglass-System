def validar_medicao(dados):
    erros = {}

    if not dados.get("cliente_id"):
        erros["cliente_id"] = "Cliente é obrigatório."

    if not dados.get("usuario_id"):
        erros["usuario_id"] = "Usuário responsável é obrigatório."

    if not dados.get("local_instalacao"):
        erros["local_instalacao"] = "Local de instalação é obrigatório."
    elif not isinstance(dados["local_instalacao"], str):
        erros["local_instalacao"] = "Local de instalação deve ser um texto."

    if dados.get("status"):
        status_validos = ["pendente", "realizada", "cancelada"]

        if dados["status"] not in status_validos:
            erros["status"] = (
                "Status inválido. Use: pendente, realizada ou cancelada."
            )

    return erros


def validar_edicao_medicao(dados):
    erros = {}

    if "cliente_id" in dados and not dados["cliente_id"]:
        erros["cliente_id"] = "Cliente é obrigatório."

    if "usuario_id" in dados and not dados["usuario_id"]:
        erros["usuario_id"] = "Usuário responsável é obrigatório."

    if "local_instalacao" in dados:
        if not dados["local_instalacao"]:
            erros["local_instalacao"] = "Local de instalação é obrigatório."
        elif not isinstance(dados["local_instalacao"], str):
            erros["local_instalacao"] = (
                "Local de instalação deve ser um texto."
            )

    if "status" in dados:
        status_validos = ["pendente", "realizada", "cancelada"]

        if dados["status"] not in status_validos:
            erros["status"] = (
                "Status inválido. Use: pendente, realizada ou cancelada."
            )

    return erros


def validar_item_medicao(dados):
    erros = {}

    if not dados.get("medicao_id"):
        erros["medicao_id"] = "Medição é obrigatória."

    if not dados.get("descricao"):
        erros["descricao"] = "Descrição é obrigatória."
    elif not isinstance(dados["descricao"], str):
        erros["descricao"] = "Descrição deve ser um texto."

    if "largura" not in dados:
        erros["largura"] = "Largura é obrigatória."
    else:
        try:
            largura = float(dados["largura"])

            if largura <= 0:
                erros["largura"] = "Largura deve ser maior que zero."

        except (TypeError, ValueError):
            erros["largura"] = "Largura deve ser um número."

    if "altura" not in dados:
        erros["altura"] = "Altura é obrigatória."
    else:
        try:
            altura = float(dados["altura"])

            if altura <= 0:
                erros["altura"] = "Altura deve ser maior que zero."

        except (TypeError, ValueError):
            erros["altura"] = "Altura deve ser um número."

    if "quantidade" in dados:
        try:
            quantidade = int(dados["quantidade"])

            if quantidade <= 0:
                erros["quantidade"] = (
                    "Quantidade deve ser maior que zero."
                )

        except (TypeError, ValueError):
            erros["quantidade"] = "Quantidade deve ser um número inteiro."

    return erros


def validar_edicao_item_medicao(dados):
    erros = {}

    if "medicao_id" in dados and not dados["medicao_id"]:
        erros["medicao_id"] = "Medição é obrigatória."

    if "descricao" in dados:
        if not dados["descricao"]:
            erros["descricao"] = "Descrição é obrigatória."
        elif not isinstance(dados["descricao"], str):
            erros["descricao"] = "Descrição deve ser um texto."

    if "largura" in dados:
        try:
            largura = float(dados["largura"])

            if largura <= 0:
                erros["largura"] = "Largura deve ser maior que zero."

        except (TypeError, ValueError):
            erros["largura"] = "Largura deve ser um número."

    if "altura" in dados:
        try:
            altura = float(dados["altura"])

            if altura <= 0:
                erros["altura"] = "Altura deve ser maior que zero."

        except (TypeError, ValueError):
            erros["altura"] = "Altura deve ser um número."

    if "quantidade" in dados:
        try:
            quantidade = int(dados["quantidade"])

            if quantidade <= 0:
                erros["quantidade"] = (
                    "Quantidade deve ser maior que zero."
                )

        except (TypeError, ValueError):
            erros["quantidade"] = "Quantidade deve ser um número inteiro."

    return erros