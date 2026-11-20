from datetime import date, datetime


TIPOS_VALIDOS = [
    "receita",
    "despesa"
]

CATEGORIAS_VALIDAS = [
    "entrada",
    "pagamento_final",
    "outra_receita",
    "material",
    "fornecedor",
    "salario",
    "manutencao",
    "outra_despesa"
]

STATUS_VALIDOS = [
    "pendente",
    "pago",
    "cancelado"
]

FORMAS_PAGAMENTO_VALIDAS = [
    "dinheiro",
    "pix",
    "cartao",
    "transferencia",
    "boleto",
    "outro"
]


def validar_data(data, campo):
    if data is None:
        return None

    if isinstance(data, datetime):
        return data

    if isinstance(data, date):
        return data

    if not isinstance(data, str):
        raise ValueError(
            f"O campo '{campo}' deve ser uma data válida."
        )

    try:
        return datetime.fromisoformat(data)
    except ValueError:
        try:
            return date.fromisoformat(data)
        except ValueError:
            raise ValueError(
                f"O campo '{campo}' deve estar em formato de data válido."
            )


def validar_lancamento(dados):
    erros = {}

    tipo = dados.get("tipo")
    categoria = dados.get("categoria")
    descricao = dados.get("descricao")
    valor = dados.get("valor")
    status = dados.get("status", "pendente")
    forma_pagamento = dados.get("forma_pagamento")

    # Tipo
    if not tipo:
        erros["tipo"] = "O tipo é obrigatório."
    elif tipo not in TIPOS_VALIDOS:
        erros["tipo"] = (
            f"Tipo inválido. Use: {', '.join(TIPOS_VALIDOS)}."
        )

    # Categoria
    if not categoria:
        erros["categoria"] = "A categoria é obrigatória."
    elif categoria not in CATEGORIAS_VALIDAS:
        erros["categoria"] = (
            f"Categoria inválida. Use: {', '.join(CATEGORIAS_VALIDAS)}."
        )

    # Descrição
    if not descricao:
        erros["descricao"] = "A descrição é obrigatória."
    elif not isinstance(descricao, str):
        erros["descricao"] = "A descrição deve ser um texto."
    elif not descricao.strip():
        erros["descricao"] = "A descrição não pode estar vazia."

    # Valor
    if valor is None:
        erros["valor"] = "O valor é obrigatório."
    else:
        try:
            valor = float(valor)

            if valor <= 0:
                erros["valor"] = "O valor deve ser maior que zero."

        except (TypeError, ValueError):
            erros["valor"] = "O valor deve ser numérico."

    # Status
    if status not in STATUS_VALIDOS:
        erros["status"] = (
            f"Status inválido. Use: {', '.join(STATUS_VALIDOS)}."
        )

    # Forma de pagamento
    if forma_pagamento is not None:
        if forma_pagamento not in FORMAS_PAGAMENTO_VALIDAS:
            erros["forma_pagamento"] = (
                "Forma de pagamento inválida. "
                f"Use: {', '.join(FORMAS_PAGAMENTO_VALIDAS)}."
            )

    # Regras de categoria
    if tipo in TIPOS_VALIDOS and categoria in CATEGORIAS_VALIDAS:

        if tipo == "receita" and categoria not in [
            "entrada",
            "pagamento_final",
            "outra_receita"
        ]:
            erros["categoria"] = (
                "Essa categoria não pode ser utilizada em uma receita."
            )

        if tipo == "despesa" and categoria not in [
            "material",
            "fornecedor",
            "salario",
            "manutencao",
            "outra_despesa"
        ]:
            erros["categoria"] = (
                "Essa categoria não pode ser utilizada em uma despesa."
            )

    # Pedido
    pedido_id = dados.get("pedido_id")

    if pedido_id is not None:
        try:
            if int(pedido_id) <= 0:
                erros["pedido_id"] = (
                    "O pedido_id deve ser maior que zero."
                )
        except (TypeError, ValueError):
            erros["pedido_id"] = (
                "O pedido_id deve ser um número inteiro."
            )

    # Fornecedor
    fornecedor_id = dados.get("fornecedor_id")

    if fornecedor_id is not None:
        try:
            if int(fornecedor_id) <= 0:
                erros["fornecedor_id"] = (
                    "O fornecedor_id deve ser maior que zero."
                )
        except (TypeError, ValueError):
            erros["fornecedor_id"] = (
                "O fornecedor_id deve ser um número inteiro."
            )

    # Data de vencimento
    if "data_vencimento" in dados:
        try:
            validar_data(
                dados.get("data_vencimento"),
                "data_vencimento"
            )
        except ValueError as erro:
            erros["data_vencimento"] = str(erro)

    # Data de pagamento
    if "data_pagamento" in dados:
        try:
            validar_data(
                dados.get("data_pagamento"),
                "data_pagamento"
            )
        except ValueError as erro:
            erros["data_pagamento"] = str(erro)

    # Observações
    observacoes = dados.get("observacoes")

    if observacoes is not None and not isinstance(observacoes, str):
        erros["observacoes"] = "As observações devem ser um texto."

    if erros:
        return erros

    return None


def validar_edicao_lancamento(dados):
    erros = {}

    if "tipo" in dados:
        if dados["tipo"] not in TIPOS_VALIDOS:
            erros["tipo"] = (
                f"Tipo inválido. Use: {', '.join(TIPOS_VALIDOS)}."
            )

    if "categoria" in dados:
        categoria = dados["categoria"]

        if categoria not in CATEGORIAS_VALIDAS:
            erros["categoria"] = (
                f"Categoria inválida. Use: {', '.join(CATEGORIAS_VALIDAS)}."
            )

    if "descricao" in dados:
        descricao = dados["descricao"]

        if not isinstance(descricao, str):
            erros["descricao"] = "A descrição deve ser um texto."
        elif not descricao.strip():
            erros["descricao"] = "A descrição não pode estar vazia."

    if "valor" in dados:
        try:
            valor = float(dados["valor"])

            if valor <= 0:
                erros["valor"] = "O valor deve ser maior que zero."

        except (TypeError, ValueError):
            erros["valor"] = "O valor deve ser numérico."

    if "status" in dados:
        if dados["status"] not in STATUS_VALIDOS:
            erros["status"] = (
                f"Status inválido. Use: {', '.join(STATUS_VALIDOS)}."
            )

    if "forma_pagamento" in dados:
        forma_pagamento = dados["forma_pagamento"]

        if forma_pagamento is not None:
            if forma_pagamento not in FORMAS_PAGAMENTO_VALIDAS:
                erros["forma_pagamento"] = (
                    "Forma de pagamento inválida. "
                    f"Use: {', '.join(FORMAS_PAGAMENTO_VALIDAS)}."
                )

    if "pedido_id" in dados and dados["pedido_id"] is not None:
        try:
            if int(dados["pedido_id"]) <= 0:
                erros["pedido_id"] = (
                    "O pedido_id deve ser maior que zero."
                )
        except (TypeError, ValueError):
            erros["pedido_id"] = (
                "O pedido_id deve ser um número inteiro."
            )

    if "fornecedor_id" in dados and dados["fornecedor_id"] is not None:
        try:
            if int(dados["fornecedor_id"]) <= 0:
                erros["fornecedor_id"] = (
                    "O fornecedor_id deve ser maior que zero."
                )
        except (TypeError, ValueError):
            erros["fornecedor_id"] = (
                "O fornecedor_id deve ser um número inteiro."
            )

    if "data_vencimento" in dados:
        try:
            validar_data(
                dados.get("data_vencimento"),
                "data_vencimento"
            )
        except ValueError as erro:
            erros["data_vencimento"] = str(erro)

    if "data_pagamento" in dados:
        try:
            validar_data(
                dados.get("data_pagamento"),
                "data_pagamento"
            )
        except ValueError as erro:
            erros["data_pagamento"] = str(erro)

    if "observacoes" in dados:
        if dados["observacoes"] is not None:
            if not isinstance(dados["observacoes"], str):
                erros["observacoes"] = (
                    "As observações devem ser um texto."
                )

    if erros:
        return erros

    return None