def validar_orcamento(dados):
    erros = {}

    if not dados.get("cliente_id"):
        erros["cliente_id"] = "Cliente é obrigatório."

    if not dados.get("medicao_id"):
        erros["medicao_id"] = "Medição é obrigatória."

    if not dados.get("usuario_id"):
        erros["usuario_id"] = "Usuário responsável é obrigatório."

    if dados.get("status"):
        status_validos = [
            "rascunho",
            "enviado",
            "aprovado",
            "recusado",
            "cancelado"
        ]

        if dados["status"] not in status_validos:
            erros["status"] = (
                "Status inválido. Use: rascunho, enviado, "
                "aprovado, recusado ou cancelado."
            )

    if "desconto" in dados:
        try:
            desconto = float(dados["desconto"])

            if desconto < 0:
                erros["desconto"] = "Desconto não pode ser negativo."

        except (TypeError, ValueError):
            erros["desconto"] = "Desconto deve ser um número."

    return erros


def validar_edicao_orcamento(dados):
    erros = {}

    if "cliente_id" in dados and not dados["cliente_id"]:
        erros["cliente_id"] = "Cliente é obrigatório."

    if "medicao_id" in dados and not dados["medicao_id"]:
        erros["medicao_id"] = "Medição é obrigatória."

    if "usuario_id" in dados and not dados["usuario_id"]:
        erros["usuario_id"] = "Usuário responsável é obrigatório."

    if "status" in dados:
        status_validos = [
            "rascunho",
            "enviado",
            "aprovado",
            "recusado",
            "cancelado"
        ]

        if dados["status"] not in status_validos:
            erros["status"] = (
                "Status inválido. Use: rascunho, enviado, "
                "aprovado, recusado ou cancelado."
            )

    if "desconto" in dados:
        try:
            desconto = float(dados["desconto"])

            if desconto < 0:
                erros["desconto"] = "Desconto não pode ser negativo."

        except (TypeError, ValueError):
            erros["desconto"] = "Desconto deve ser um número."

    return erros


def validar_item_orcamento(dados):
    erros = {}

    if not dados.get("orcamento_id"):
        erros["orcamento_id"] = "Orçamento é obrigatório."

    if not dados.get("descricao"):
        erros["descricao"] = "Descrição é obrigatória."
    elif not isinstance(dados["descricao"], str):
        erros["descricao"] = "Descrição deve ser um texto."

    if "quantidade" not in dados:
        erros["quantidade"] = "Quantidade é obrigatória."
    else:
        try:
            quantidade = float(dados["quantidade"])

            if quantidade <= 0:
                erros["quantidade"] = "Quantidade deve ser maior que zero."

        except (TypeError, ValueError):
            erros["quantidade"] = "Quantidade deve ser um número."

    if "valor_unitario" not in dados:
        erros["valor_unitario"] = "Valor unitário é obrigatório."
    else:
        try:
            valor = float(dados["valor_unitario"])

            if valor < 0:
                erros["valor_unitario"] = (
                    "Valor unitário não pode ser negativo."
                )

        except (TypeError, ValueError):
            erros["valor_unitario"] = (
                "Valor unitário deve ser um número."
            )

    return erros


def validar_edicao_item_orcamento(dados):
    erros = {}

    if "orcamento_id" in dados and not dados["orcamento_id"]:
        erros["orcamento_id"] = "Orçamento é obrigatório."

    if "descricao" in dados:
        if not dados["descricao"]:
            erros["descricao"] = "Descrição é obrigatória."
        elif not isinstance(dados["descricao"], str):
            erros["descricao"] = "Descrição deve ser um texto."

    if "quantidade" in dados:
        try:
            quantidade = float(dados["quantidade"])

            if quantidade <= 0:
                erros["quantidade"] = "Quantidade deve ser maior que zero."

        except (TypeError, ValueError):
            erros["quantidade"] = "Quantidade deve ser um número."

    if "valor_unitario" in dados:
        try:
            valor = float(dados["valor_unitario"])

            if valor < 0:
                erros["valor_unitario"] = (
                    "Valor unitário não pode ser negativo."
                )

        except (TypeError, ValueError):
            erros["valor_unitario"] = (
                "Valor unitário deve ser um número."
            )

    return erros