from flask import Blueprint

from database import db

from app.common.permissions import verificar_permissao
from app.common.responses import (
    resposta_sucesso,
    resposta_erro
)

from app.financeiro.models import LancamentoFinanceiro
from app.estoque.models import Material
from app.pedidos.models import Pedido
from app.producao.models import Producao
from app.instalacoes.models import Instalacao


dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


@dashboard_bp.route("/resumo", methods=["GET"])
@verificar_permissao("financeiro", "visualizar")
def resumo_dashboard():
    try:
        lancamentos = LancamentoFinanceiro.query.all()

        total_receitas = sum(
            lancamento.valor
            for lancamento in lancamentos
            if lancamento.tipo == "receita"
            and lancamento.status != "cancelado"
        )

        total_despesas = sum(
            lancamento.valor
            for lancamento in lancamentos
            if lancamento.tipo == "despesa"
            and lancamento.status != "cancelado"
        )

        total_pendente = sum(
            lancamento.valor
            for lancamento in lancamentos
            if lancamento.status == "pendente"
        )

        saldo = total_receitas - total_despesas

        dados = {
            "total_receitas": total_receitas,
            "total_despesas": total_despesas,
            "saldo": saldo,
            "total_pendente": total_pendente,
            "quantidade_lancamentos": len(lancamentos)
        }

        return resposta_sucesso(
            "Resumo do dashboard carregado com sucesso.",
            dados
        )

    except Exception as erro:
        return resposta_erro(
            "Erro ao carregar resumo do dashboard.",
            500,
            str(erro)
        )


@dashboard_bp.route("/pedidos", methods=["GET"])
@verificar_permissao("financeiro", "visualizar")
def resumo_pedidos():
    try:
        pedidos = Pedido.query.all()

        total_pedidos = len(pedidos)

        aguardando_producao = sum(
            1
            for pedido in pedidos
            if pedido.status == "aguardando_producao"
        )

        dados = {
            "total_pedidos": total_pedidos,
            "aguardando_producao": aguardando_producao
        }

        return resposta_sucesso(
            "Resumo dos pedidos carregado com sucesso.",
            dados
        )

    except Exception as erro:
        return resposta_erro(
            "Erro ao carregar resumo dos pedidos.",
            500,
            str(erro)
        )


@dashboard_bp.route("/producao", methods=["GET"])
@verificar_permissao("producao", "visualizar")
def resumo_producao():
    try:
        producoes = Producao.query.all()

        total_producoes = len(producoes)

        aguardando = sum(
            1 for producao in producoes
            if producao.status == "aguardando"
        )

        dados = {
            "total_producoes": total_producoes,
            "aguardando": aguardando
        }

        return resposta_sucesso(
            "Resumo da produção carregado com sucesso.",
            dados
        )

    except Exception as erro:
        return resposta_erro(
            "Erro ao carregar resumo da produção.",
            500,
            str(erro)
        )


@dashboard_bp.route("/instalacoes", methods=["GET"])
@verificar_permissao("instalacoes", "visualizar")
def resumo_instalacoes():
    try:
        instalacoes = Instalacao.query.all()

        total_instalacoes = len(instalacoes)

        agendadas = sum(
            1 for instalacao in instalacoes
            if instalacao.status == "agendada"
        )

        em_andamento = sum(
            1 for instalacao in instalacoes
            if instalacao.status == "em_andamento"
        )

        concluidas = sum(
            1 for instalacao in instalacoes
            if instalacao.status == "concluida"
        )

        canceladas = sum(
            1 for instalacao in instalacoes
            if instalacao.status == "cancelada"
        )

        dados = {
            "total_instalacoes": total_instalacoes,
            "agendadas": agendadas,
            "em_andamento": em_andamento,
            "concluidas": concluidas,
            "canceladas": canceladas
        }

        return resposta_sucesso(
            "Resumo das instalações carregado com sucesso.",
            dados
        )

    except Exception as erro:
        return resposta_erro(
            "Erro ao carregar resumo das instalações.",
            500,
            str(erro)
        )


@dashboard_bp.route("/estoque", methods=["GET"])
@verificar_permissao("estoque", "visualizar")
def resumo_estoque():
    try:
        materiais = Material.query.filter_by(ativo=True).all()

        total_materiais = len(materiais)

        estoque_baixo = sum(
            1 for material in materiais
            if material.quantidade <= material.estoque_minimo
        )

        estoque_zerado = sum(
            1 for material in materiais
            if material.quantidade <= 0
        )

        dados = {
            "total_materiais": total_materiais,
            "estoque_baixo": estoque_baixo,
            "estoque_zerado": estoque_zerado
        }

        return resposta_sucesso(
            "Resumo do estoque carregado com sucesso.",
            dados
        )

    except Exception as erro:
        return resposta_erro(
            "Erro ao carregar resumo do estoque.",
            500,
            str(erro)
        )

