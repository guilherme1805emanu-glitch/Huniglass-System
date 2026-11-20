def validar_producao(dados):
    erros = {}

    if not dados.get("pedido_id"):
        erros["pedido_id"] = (
            "Pedido é obrigatório."
        )

    if not dados.get("usuario_id"):
        erros["usuario_id"] = (
            "Usuário é obrigatório."
        )

    status_validos = [
        "aguardando",
        "em_producao",
        "pausada",
        "concluida",
        "cancelada"
    ]

    if "status" in dados:
        if dados["status"] not in status_validos:
            erros["status"] = (
                "Status inválido."
            )

    if "observacoes" in dados:
        if dados["observacoes"] is not None:
            if not isinstance(dados["observacoes"], str):
                erros["observacoes"] = (
                    "Observações devem ser um texto."
                )

    return erros


def validar_edicao_producao(dados):
    erros = {}

    status_validos = [
        "aguardando",
        "em_producao",
        "pausada",
        "concluida",
        "cancelada"
    ]

    if "status" in dados:
        if dados["status"] not in status_validos:
            erros["status"] = (
                "Status inválido."
            )

    if "observacoes" in dados:
        if dados["observacoes"] is not None:
            if not isinstance(dados["observacoes"], str):
                erros["observacoes"] = (
                    "Observações devem ser um texto."
                )

    if "data_previsao" in dados:
        if dados["data_previsao"] is not None:
            if not isinstance(dados["data_previsao"], str):
                erros["data_previsao"] = "Data de previsão deve ser um texto."

    if "data_inicio" in dados:
        erros["data_inicio"] = "Data de início é definida automaticamente pelo sistema."

    if "data_conclusao" in dados:
        erros["data_conclusao"] = "Data de conclusão é definida automaticamente pelo sistema."

    return erros


def validar_item_producao(dados):
    erros = {}

    if not dados.get("item_pedido_id"):
        erros["item_pedido_id"] = (
            "Item do pedido é obrigatório."
        )

    if "quantidade" not in dados:
        erros["quantidade"] = (
            "Quantidade é obrigatória."
        )
    else:
        try:
            quantidade = float(
                dados["quantidade"]
            )

            if quantidade <= 0:
                erros["quantidade"] = (
                    "Quantidade deve ser maior que zero."
                )

        except (ValueError, TypeError):
            erros["quantidade"] = (
                "Quantidade deve ser numérica."
            )

    status_validos = [
        "aguardando",
        "em_producao",
        "concluida",
        "cancelada"
    ]

    if "status" in dados:
        if dados["status"] not in status_validos:
            erros["status"] = (
                "Status inválido."
            )

    if "observacoes" in dados:
        if dados["observacoes"] is not None:
            if not isinstance(dados["observacoes"], str):
                erros["observacoes"] = (
                    "Observações devem ser um texto."
                )

    return erros


def validar_edicao_item_producao(dados):
    erros = {}

    if "quantidade" in dados:
        try:
            quantidade = float(
                dados["quantidade"]
            )

            if quantidade <= 0:
                erros["quantidade"] = (
                    "Quantidade deve ser maior que zero."
                )

        except (ValueError, TypeError):
            erros["quantidade"] = (
                "Quantidade deve ser numérica."
            )

    status_validos = [
        "aguardando",
        "em_producao",
        "concluida",
        "cancelada"
    ]

    if "status" in dados:
        if dados["status"] not in status_validos:
            erros["status"] = (
                "Status inválido."
            )

    if "observacoes" in dados:
        if dados["observacoes"] is not None:
            if not isinstance(dados["observacoes"], str):
                erros["observacoes"] = (
                    "Observações devem ser um texto."
                )

    if "pedido_id" in dados:
        if not dados["pedido_id"]:
            erros["pedido_id"] = (
                "Pedido é obrigatório."
            )

    if "usuario_id" in dados:
        if not dados["usuario_id"]:
            erros["usuario_id"] = (
                "Usuário é obrigatório."
            )

    return erros


def validar_material_producao(dados):
    erros = {}

    if not dados.get("material_id"):
        erros["material_id"] = "Material é obrigatório."

    if "quantidade" not in dados:
        erros["quantidade"] = "Quantidade é obrigatória."
    else:
        try:
            quantidade = float(dados["quantidade"])

            if quantidade <= 0:
                erros["quantidade"] = "Quantidade deve ser maior que zero."

        except (ValueError, TypeError):
            erros["quantidade"] = "Quantidade deve ser numérica."

    if "observacoes" in dados:
        if dados["observacoes"] is not None:
            if not isinstance(dados["observacoes"], str):
                erros["observacoes"] = "Observações devem ser um texto."

    return erros


def validar_edicao_material_producao(dados):
    erros = {}

    if "consumido" in dados:
        erros["consumido"] = (
            "O campo consumido é definido automaticamente pelo sistema."
        )

    if "data_consumo" in dados:
        erros["data_consumo"] = (
            "A data de consumo é definida automaticamente pelo sistema."
        )

    if "material_id" in dados:
        if not dados["material_id"]:
            erros["material_id"] = "Material é obrigatório."

    if "quantidade" in dados:
        try:
            quantidade = float(dados["quantidade"])

            if quantidade <= 0:
                erros["quantidade"] = "Quantidade deve ser maior que zero."

        except (ValueError, TypeError):
            erros["quantidade"] = "Quantidade deve ser numérica."

    if "observacoes" in dados:
        if dados["observacoes"] is not None:
            if not isinstance(dados["observacoes"], str):
                erros["observacoes"] = "Observações devem ser um texto."

    return erros