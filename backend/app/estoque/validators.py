def validar_material(dados):

    erros = {}

    if not dados:
        erros["geral"] = "Nenhum dado foi enviado."
        return erros

    nome = dados.get("nome")
    categoria = dados.get("categoria")
    unidade = dados.get("unidade")
    quantidade = dados.get("quantidade")
    estoque_minimo = dados.get("estoque_minimo")
    ativo = dados.get("ativo")

    # Nome
    if nome is None:
        erros["nome"] = "O nome é obrigatório."

    elif not isinstance(nome, str) or not nome.strip():
        erros["nome"] = "O nome não pode estar vazio."

    # Categoria
    if categoria is None:
        erros["categoria"] = "A categoria é obrigatória."

    elif not isinstance(categoria, str) or not categoria.strip():
        erros["categoria"] = "A categoria não pode estar vazia."

    # Unidade
    if unidade is None:
        erros["unidade"] = "A unidade é obrigatória."

    elif not isinstance(unidade, str) or not unidade.strip():
        erros["unidade"] = "A unidade não pode estar vazia."

    # Quantidade
    if quantidade is not None:

        if not isinstance(quantidade, (int, float)) or isinstance(quantidade, bool):
            erros["quantidade"] = "A quantidade deve ser numérica."

        elif quantidade < 0:
            erros["quantidade"] = "A quantidade não pode ser negativa."

    # Estoque mínimo
    if estoque_minimo is not None:

        if not isinstance(estoque_minimo, (int, float)) or isinstance(estoque_minimo, bool):
            erros["estoque_minimo"] = "O estoque mínimo deve ser numérico."

        elif estoque_minimo < 0:
            erros["estoque_minimo"] = "O estoque mínimo não pode ser negativo."

    # Ativo
    if ativo is not None:

        if not isinstance(ativo, bool):
            erros["ativo"] = "O campo ativo deve ser verdadeiro ou falso."

    return erros

# ------------------------------------------------------------------------------------------
# VALIDAÇÃO DE EDIÇÃO DE MATERIAL

def validar_edicao_material(dados):

    erros = {}

    if not dados:
        erros["geral"] = "Nenhum dado foi enviado."
        return erros

    # Nome
    if "nome" in dados:
        if not isinstance(dados["nome"], str) or not dados["nome"].strip():
            erros["nome"] = "O nome não pode estar vazio."

    # Categoria
    if "categoria" in dados:
        if not isinstance(dados["categoria"], str) or not dados["categoria"].strip():
            erros["categoria"] = "A categoria não pode estar vazia."

    # Unidade
    if "unidade" in dados:
        if not isinstance(dados["unidade"], str) or not dados["unidade"].strip():
            erros["unidade"] = "A unidade não pode estar vazia."

    # Quantidade
    if "quantidade" in dados:
        quantidade = dados["quantidade"]

        if not isinstance(quantidade, (int, float)) or isinstance(quantidade, bool):
            erros["quantidade"] = "A quantidade deve ser numérica."
        elif quantidade < 0:
            erros["quantidade"] = "A quantidade não pode ser negativa."

    # Estoque mínimo
    if "estoque_minimo" in dados:
        estoque_minimo = dados["estoque_minimo"]

        if not isinstance(estoque_minimo, (int, float)) or isinstance(estoque_minimo, bool):
            erros["estoque_minimo"] = "O estoque mínimo deve ser numérico."
        elif estoque_minimo < 0:
            erros["estoque_minimo"] = "O estoque mínimo não pode ser negativo."

    # Fornecedor
    if "fornecedor_id" in dados:
        if dados["fornecedor_id"] is not None:
            if not isinstance(dados["fornecedor_id"], int) or isinstance(dados["fornecedor_id"], bool):
                erros["fornecedor_id"] = "O fornecedor deve ser um ID numérico inteiro."

    # Ativo
    if "ativo" in dados:
        if not isinstance(dados["ativo"], bool):
            erros["ativo"] = "O campo ativo deve ser verdadeiro ou falso."

    # Observações
    if "observacoes" in dados:
        if dados["observacoes"] is not None and not isinstance(dados["observacoes"], str):
            erros["observacoes"] = "As observações devem ser um texto."

    return erros

# ------------------------------------------------------------------------------------------
# VALIDAÇÃO DE MOVIMENTAÇÃO DE ESTOQUE

def validar_movimentacao(dados):

    erros = {}

    if not dados:
        erros["geral"] = "Nenhum dado foi enviado."
        return erros

    material_id = dados.get("material_id")
    tipo = dados.get("tipo")
    quantidade = dados.get("quantidade")

    # Material
    if material_id is None:
        erros["material_id"] = "O material é obrigatório."
    elif not isinstance(material_id, int) or isinstance(material_id, bool):
        erros["material_id"] = "O material deve ser um ID numérico inteiro."

    # Tipo
    if tipo is None:
        erros["tipo"] = "O tipo da movimentação é obrigatório."
    elif not isinstance(tipo, str):
        erros["tipo"] = "O tipo deve ser um texto."
    elif tipo.lower() not in ["entrada", "saida"]:
        erros["tipo"] = "O tipo deve ser 'entrada' ou 'saida'."

    # Quantidade
    if quantidade is None:
        erros["quantidade"] = "A quantidade é obrigatória."
    elif not isinstance(quantidade, (int, float)) or isinstance(quantidade, bool):
        erros["quantidade"] = "A quantidade deve ser numérica."
    elif quantidade <= 0:
        erros["quantidade"] = "A quantidade deve ser maior que zero."

    return erros

# ------------------------------------------------------------------------------------------
# VALIDAÇÃO DE FORNECEDOR

def validar_fornecedor(dados):

    erros = {}

    if not dados:
        erros["geral"] = "Nenhum dado foi enviado."
        return erros

    nome = dados.get("nome")
    telefone = dados.get("telefone")
    email = dados.get("email")
    cpf_cnpj = dados.get("cpf_cnpj")
    estado = dados.get("estado")
    ativo = dados.get("ativo")

    # Nome
    if nome is None:
        erros["nome"] = "O nome é obrigatório."

    elif not isinstance(nome, str) or not nome.strip():
        erros["nome"] = "O nome não pode estar vazio."

    # Telefone
    if telefone is not None:

        if not isinstance(telefone, str):
            erros["telefone"] = "O telefone deve ser um texto."

        elif not telefone.strip():
            erros["telefone"] = "O telefone não pode estar vazio."

    # E-mail
    if email is not None:

        if not isinstance(email, str):
            erros["email"] = "O e-mail deve ser um texto."

        elif email.strip() and "@" not in email:
            erros["email"] = "O e-mail informado não é válido."

    # CPF / CNPJ
    if cpf_cnpj is not None:

        if not isinstance(cpf_cnpj, str):
            erros["cpf_cnpj"] = "O CPF/CNPJ deve ser um texto."

        elif not cpf_cnpj.strip():
            erros["cpf_cnpj"] = "O CPF/CNPJ não pode estar vazio."

    # Estado
    if estado is not None:

        if not isinstance(estado, str):
            erros["estado"] = "O estado deve ser um texto."

        elif estado.strip() and len(estado.strip()) != 2:
            erros["estado"] = "O estado deve possuir 2 caracteres."

    # Ativo
    if ativo is not None:

        if not isinstance(ativo, bool):
            erros["ativo"] = "O campo ativo deve ser verdadeiro ou falso."

    return erros

# ------------------------------------------------------------------------------------------
# VALIDAÇÃO DE EDIÇÃO DE FORNECEDOR

def validar_edicao_fornecedor(dados):

    erros = {}

    if not dados:
        erros["geral"] = "Nenhum dado foi enviado."
        return erros

    # Nome
    if "nome" in dados:
        if not isinstance(dados["nome"], str) or not dados["nome"].strip():
            erros["nome"] = "O nome não pode estar vazio."

    # Telefone
    if "telefone" in dados:
        if dados["telefone"] is not None and not isinstance(dados["telefone"], str):
            erros["telefone"] = "O telefone deve ser um texto."

    # E-mail
    if "email" in dados:
        if dados["email"] is not None and not isinstance(dados["email"], str):
            erros["email"] = "O e-mail deve ser um texto."
        elif dados["email"] and "@" not in dados["email"]:
            erros["email"] = "O e-mail informado não é válido."

    # CPF / CNPJ
    if "cpf_cnpj" in dados:
        if dados["cpf_cnpj"] is not None and not isinstance(dados["cpf_cnpj"], str):
            erros["cpf_cnpj"] = "O CPF/CNPJ deve ser um texto."

    # Endereço
    if "endereco" in dados:
        if dados["endereco"] is not None and not isinstance(dados["endereco"], str):
            erros["endereco"] = "O endereço deve ser um texto."

    # Cidade
    if "cidade" in dados:
        if dados["cidade"] is not None and not isinstance(dados["cidade"], str):
            erros["cidade"] = "A cidade deve ser um texto."

    # Estado
    if "estado" in dados:
        if dados["estado"] is not None:

            if not isinstance(dados["estado"], str):
                erros["estado"] = "O estado deve ser um texto."

            elif dados["estado"].strip() and len(dados["estado"].strip()) != 2:
                erros["estado"] = "O estado deve possuir 2 caracteres."

    # Observações
    if "observacoes" in dados:
        if dados["observacoes"] is not None and not isinstance(dados["observacoes"], str):
            erros["observacoes"] = "As observações devem ser um texto."

    # Ativo
    if "ativo" in dados:
        if not isinstance(dados["ativo"], bool):
            erros["ativo"] = "O campo ativo deve ser verdadeiro ou falso."

    return erros