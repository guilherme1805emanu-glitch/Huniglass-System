
from app.clientes.models import Cliente


def somente_numeros(valor):
    return ''.join(caractere for caractere in (valor or '') if caractere.isdigit())


def normalizar_email(valor):
    return (valor or '').strip().casefold()


def validar_cpf(cpf):
    cpf = somente_numeros(cpf)

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    primeiro = (soma * 10) % 11
    primeiro = 0 if primeiro == 10 else primeiro

    if primeiro != int(cpf[9]):
        return False

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    segundo = (soma * 10) % 11
    segundo = 0 if segundo == 10 else segundo

    return segundo == int(cpf[10])


def validar_cnpj(cnpj):
    cnpj = somente_numeros(cnpj)

    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
    resto = soma % 11
    primeiro = 0 if resto < 2 else 11 - resto

    if primeiro != int(cnpj[12]):
        return False

    soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
    resto = soma % 11
    segundo = 0 if resto < 2 else 11 - resto

    return segundo == int(cnpj[13])


def validar_cliente(dados, cliente_id=None):
    erros = {}

    if not dados:
        return {"geral": "Os dados do cliente são obrigatórios."}

    nome = dados.get("nome")
    telefone = dados.get("telefone")
    email = dados.get("email")
    cpf_cnpj = dados.get("cpf_cnpj")

    # Nome
    if not isinstance(nome, str) or not nome.strip():
        erros["nome"] = "O nome do cliente é obrigatório."

    # Telefone: aceita formatação, mas compara somente os dígitos.
    telefone_permitidos = set("0123456789 ()+-")
    telefone_numeros = somente_numeros(telefone)

    if not isinstance(telefone, str) or not telefone.strip():
        erros["telefone"] = "O telefone do cliente é obrigatório."
    elif any(c not in telefone_permitidos for c in telefone):
        erros["telefone"] = "O telefone contém caracteres inválidos."
    elif len(telefone_numeros) not in (10, 11):
        erros["telefone"] = "O telefone deve ter 10 ou 11 dígitos."

    # E-mail
    email_normalizado = normalizar_email(email)

    if email and (
        not isinstance(email, str)
        or "@" not in email_normalizado
        or "." not in email_normalizado.split("@")[-1]
    ):
        erros["email"] = "O e-mail informado é inválido."

    # CPF/CNPJ
    documento = somente_numeros(cpf_cnpj)

    if cpf_cnpj:
        if not isinstance(cpf_cnpj, str):
            erros["cpf_cnpj"] = "CPF/CNPJ inválido."
        elif any(c not in "0123456789.-/ " for c in cpf_cnpj):
            erros["cpf_cnpj"] = "CPF/CNPJ contém caracteres inválidos."
        elif len(documento) == 11 and not validar_cpf(documento):
            erros["cpf_cnpj"] = "CPF inválido."
        elif len(documento) == 14 and not validar_cnpj(documento):
            erros["cpf_cnpj"] = "CNPJ inválido."
        elif len(documento) not in (11, 14):
            erros["cpf_cnpj"] = "CPF/CNPJ deve ter 11 ou 14 dígitos."

    # Não consulta duplicidades se os campos essenciais forem inválidos.
    if erros:
        return erros

    # Verificação de duplicidade nos clientes existentes.
    clientes_existentes = Cliente.query.all()

    for cliente in clientes_existentes:
        # Na edição, não comparar o cliente consigo mesmo.
        if cliente_id is not None and cliente.id == cliente_id:
            continue

        if telefone_numeros and (
            somente_numeros(cliente.telefone) == telefone_numeros
        ):
            erros["telefone"] = "Este telefone já está cadastrado para outro cliente."

        if email_normalizado and (
            normalizar_email(cliente.email) == email_normalizado
        ):
            erros["email"] = "Este e-mail já está cadastrado para outro cliente."

        documento_existente = somente_numeros(cliente.cpf_cnpj)

        if documento and documento_existente == documento:
            erros["cpf_cnpj"] = "Este CPF/CNPJ já está cadastrado para outro cliente."

    return erros
