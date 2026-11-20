def validar_pedido(dados):
    erros = {}

    if not dados.get("cliente_id"):
        erros["cliente_id"] = "Cliente é obrigatório."

    if not dados.get("orcamento_id"):
        erros["orcamento_id"] = "Orçamento é obrigatório."

    if not dados.get("usuario_id"):
        erros["usuario_id"] = "Usuário é obrigatório."

    status_validos = [
        "aguardando_producao",
        "em_producao",
        "pronto",
        "em_instalacao",
        "concluido",
        "cancelado"
    ]

    if "status" in dados:
        if dados["status"] not in status_validos:
            erros["status"] = (
                "Status inválido."
            )

    if "valor_total" in dados:
        try:
            valor_total = float(dados["valor_total"])

            if valor_total < 0:
                erros["valor_total"] = (
                    "Valor total não pode ser negativo."
                )

        except (ValueError, TypeError):
            erros["valor_total"] = (
                "Valor total deve ser numérico."
            )

    if "entrada" in dados:
        try:
            entrada = float(dados["entrada"])

            if entrada < 0:
                erros["entrada"] = (
                    "Entrada não pode ser negativa."
                )

        except (ValueError, TypeError):
            erros["entrada"] = (
                "Entrada deve ser numérica."
            )

    return erros


def validar_edicao_pedido(dados):
    erros = {}

    status_validos = [
        "aguardando_producao",
        "em_producao",
        "pronto",
        "em_instalacao",
        "concluido",
        "cancelado"
    ]

    if "status" in dados:
        if dados["status"] not in status_validos:
            erros["status"] = (
                "Status inválido."
            )

    if "entrada" in dados:
        try:
            entrada = float(dados["entrada"])

            if entrada < 0:
                erros["entrada"] = (
                    "Entrada não pode ser negativa."
                )

        except (ValueError, TypeError):
            erros["entrada"] = (
                "Entrada deve ser numérica."
            )

    return erros


def validar_item_pedido(dados):
    erros = {}

    if not dados.get("descricao"):
        erros["descricao"] = (
            "Descrição é obrigatória."
        )
    elif not isinstance(dados["descricao"], str):
        erros["descricao"] = (
            "Descrição deve ser um texto."
        )

    if "quantidade" not in dados:
        erros["quantidade"] = (
            "Quantidade é obrigatória."
        )
    else:
        try:
            quantidade = float(dados["quantidade"])

            if quantidade <= 0:
                erros["quantidade"] = (
                    "Quantidade deve ser maior que zero."
                )

        except (ValueError, TypeError):
            erros["quantidade"] = (
                "Quantidade deve ser numérica."
            )

    if "valor_unitario" not in dados:
        erros["valor_unitario"] = (
            "Valor unitário é obrigatório."
        )
    else:
        try:
            valor_unitario = float(
                dados["valor_unitario"]
            )

            if valor_unitario < 0:
                erros["valor_unitario"] = (
                    "Valor unitário não pode ser negativo."
                )

        except (ValueError, TypeError):
            erros["valor_unitario"] = (
                "Valor unitário deve ser numérico."
            )

    return erros


def validar_edicao_item_pedido(dados):
    erros = {}

    if "descricao" in dados:
        if not dados["descricao"]:
            erros["descricao"] = (
                "Descrição não pode ser vazia."
            )
        elif not isinstance(dados["descricao"], str):
            erros["descricao"] = (
                "Descrição deve ser um texto."
            )

    if "quantidade" in dados:
        try:
            quantidade = float(dados["quantidade"])

            if quantidade <= 0:
                erros["quantidade"] = (
                    "Quantidade deve ser maior que zero."
                )

        except (ValueError, TypeError):
            erros["quantidade"] = (
                "Quantidade deve ser numérica."
            )

    if "valor_unitario" in dados:
        try:
            valor_unitario = float(
                dados["valor_unitario"]
            )

            if valor_unitario < 0:
                erros["valor_unitario"] = (
                    "Valor unitário não pode ser negativo."
                )

        except (ValueError, TypeError):
            erros["valor_unitario"] = (
                "Valor unitário deve ser numérico."
            )

    return erros


