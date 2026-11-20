from flask import jsonify


def resposta_sucesso(mensagem, dados=None, status=200):
    resposta = {
        "sucesso": True,
        "mensagem": mensagem
    }

    if dados is not None:
        resposta["dados"] = dados

    return jsonify(resposta), status


def resposta_erro(mensagem, status=400, erros=None):
    resposta = {
        "sucesso": False,
        "erro": mensagem
    }

    if erros is not None:
        resposta["detalhes"] = erros

    return jsonify(resposta), status