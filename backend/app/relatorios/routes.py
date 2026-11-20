from flask import Blueprint

from database import db

from app.common.permissions import verificar_permissao
from app.common.responses import resposta_sucesso, resposta_erro
from app.clientes.models import Cliente
from app.orcamentos.models import Orcamento
from app.pedidos.models import Pedido
from app.estoque.models import Material
from app.agenda.models import Agenda
from app.instalacoes.models import Instalacao
from app.financeiro.models import LancamentoFinanceiro
from app.producao.models import MaterialProducao, Producao


relatorios_bp = Blueprint("relatorios", __name__, url_prefix="/relatorios")


@relatorios_bp.route("/resumo", methods=["GET"])
@verificar_permissao("relatorios", "visualizar")
def relatorio_resumo():
    try:
        total_clientes = Cliente.query.count()
        total_orcamentos = Orcamento.query.count()
        total_pedidos = Pedido.query.count()
        total_materiais = Material.query.count()
        total_agenda = Agenda.query.count()
        total_instalacoes = Instalacao.query.count()
        total_financeiro = LancamentoFinanceiro.query.count()

        dados = {
            "clientes": total_clientes,
            "orcamentos": total_orcamentos,
            "pedidos": total_pedidos,
            "materiais": total_materiais,
            "agenda": total_agenda,
            "instalacoes": total_instalacoes,
            "financeiro": total_financeiro
        }

        return resposta_sucesso(
            "Resumo geral gerado com sucesso.",
            dados
        )

    except Exception as e:
        db.session.rollback()

        return resposta_erro(
            f"Erro ao gerar relatório: {str(e)}"
        ), 500


@relatorios_bp.route("/clientes", methods=["GET"])
@verificar_permissao("relatorios", "visualizar")
def relatorio_clientes():
    try:
        clientes = Cliente.query.order_by(Cliente.nome.asc()).all()

        dados = []

        for cliente in clientes:
            dados.append({
                "id": cliente.id,
                "nome": cliente.nome,
                "telefone": cliente.telefone,
                "email": cliente.email,
                "cidade": cliente.cidade,
                "estado": cliente.estado
            })

        return resposta_sucesso(
            "Relatório de clientes gerado com sucesso.",
            {
                "total": len(dados),
                "clientes": dados
            }
        )

    except Exception as e:
        db.session.rollback()

        return resposta_erro(
            f"Erro ao gerar relatório de clientes: {str(e)}"
        ), 500


@relatorios_bp.route("/orcamentos", methods=["GET"])
@verificar_permissao("relatorios", "visualizar")
def relatorio_orcamentos():
    try:
        orcamentos = Orcamento.query.order_by(
            Orcamento.data.desc()
        ).all()

        dados = []

        total_subtotal = 0
        total_desconto = 0
        total_valor = 0

        for orcamento in orcamentos:
            subtotal = orcamento.subtotal or 0
            desconto = orcamento.desconto or 0
            valor_total = orcamento.valor_total or 0

            total_subtotal += subtotal
            total_desconto += desconto
            total_valor += valor_total

            dados.append({
                "id": orcamento.id,
                "cliente": {
                    "id": orcamento.cliente.id,
                    "nome": orcamento.cliente.nome
                } if orcamento.cliente else None,
                "usuario": {
                    "id": orcamento.usuario.id,
                    "nome": orcamento.usuario.nome
                } if orcamento.usuario else None,
                "data": orcamento.data.isoformat() if orcamento.data else None,
                "validade": orcamento.validade.isoformat() if orcamento.validade else None,
                "status": orcamento.status,
                "subtotal": subtotal,
                "desconto": desconto,
                "valor_total": valor_total,
                "observacoes": orcamento.observacoes,
                "quantidade_itens": len(orcamento.itens)
            })

        return resposta_sucesso(
            "Relatório de orçamentos gerado com sucesso.",
            {
                "total": len(dados),
                "resumo": {
                    "subtotal": total_subtotal,
                    "desconto": total_desconto,
                    "valor_total": total_valor
                },
                "orcamentos": dados
            }
        )

    except Exception as e:
        db.session.rollback()

        return resposta_erro(
            f"Erro ao gerar relatório de orçamentos: {str(e)}"
        ), 500


@relatorios_bp.route("/pedidos", methods=["GET"])
@verificar_permissao("relatorios", "visualizar")
def relatorio_pedidos():
    try:
        pedidos = Pedido.query.order_by(
            Pedido.data.desc()
        ).all()

        dados = []

        total_valor = 0
        total_entrada = 0
        total_restante = 0

        for pedido in pedidos:
            valor_total = pedido.valor_total or 0
            entrada = pedido.entrada or 0
            restante = pedido.restante or 0

            total_valor += valor_total
            total_entrada += entrada
            total_restante += restante

            dados.append({
                "id": pedido.id,

                "cliente": {
                    "id": pedido.cliente.id,
                    "nome": pedido.cliente.nome
                } if pedido.cliente else None,

                "orcamento": {
                    "id": pedido.orcamento.id
                } if pedido.orcamento else None,

                "usuario": {
                    "id": pedido.usuario.id,
                    "nome": pedido.usuario.nome
                } if pedido.usuario else None,

                "data": pedido.data.isoformat() if pedido.data else None,
                "status": pedido.status,
                "valor_total": valor_total,
                "entrada": entrada,
                "restante": restante,
                "observacoes": pedido.observacoes,
                "quantidade_itens": len(pedido.itens)
            })

        return resposta_sucesso(
            "Relatório de pedidos gerado com sucesso.",
            {
                "total": len(dados),

                "resumo": {
                    "valor_total": total_valor,
                    "entrada": total_entrada,
                    "restante": total_restante
                },

                "pedidos": dados
            }
        )

    except Exception as e:
        db.session.rollback()

        return resposta_erro(
            f"Erro ao gerar relatório de pedidos: {str(e)}"
        ), 500


@relatorios_bp.route("/producao", methods=["GET"])
@verificar_permissao("relatorios", "visualizar")
def relatorio_producao():
    try:
        producoes = Producao.query.order_by(
            Producao.id.desc()
        ).all()

        dados = []

        total_producoes = len(producoes)
        total_itens = 0
        total_materiais = 0
        materiais_consumidos = 0

        for producao in producoes:
            quantidade_itens = len(producao.itens)

            materiais = MaterialProducao.query.filter_by(
                producao_id=producao.id
            ).all()

            quantidade_materiais = len(materiais)
            quantidade_consumidos = sum(
                1 for material in materiais
                if material.consumido
            )

            total_itens += quantidade_itens
            total_materiais += quantidade_materiais
            materiais_consumidos += quantidade_consumidos

            dados.append({
                "id": producao.id,
                "pedido": {
                    "id": producao.pedido.id
                } if producao.pedido else None,
                "usuario": {
                    "id": producao.usuario.id,
                    "nome": producao.usuario.nome
                } if producao.usuario else None,
                "status": producao.status,
                "data_inicio": (
                    producao.data_inicio.isoformat()
                    if producao.data_inicio
                    else None
                ),
                "data_previsao": (
                    producao.data_previsao.isoformat()
                    if producao.data_previsao
                    else None
                ),
                "data_conclusao": (
                    producao.data_conclusao.isoformat()
                    if producao.data_conclusao
                    else None
                ),
                "observacoes": producao.observacoes,
                "quantidade_itens": quantidade_itens,
                "quantidade_materiais": quantidade_materiais,
                "materiais_consumidos": quantidade_consumidos
            })

        return resposta_sucesso(
            "Relatório de produção gerado com sucesso.",
            {
                "total": total_producoes,
                "resumo": {
                    "total_itens": total_itens,
                    "total_materiais": total_materiais,
                    "materiais_consumidos": materiais_consumidos
                },
                "producoes": dados
            }
        )

    except Exception as e:
        db.session.rollback()

        return resposta_erro(
            f"Erro ao gerar relatório de produção: {str(e)}"
        ), 500


@relatorios_bp.route("/instalacoes", methods=["GET"])
@verificar_permissao("relatorios", "visualizar")
def relatorio_instalacoes():
    try:
        instalacoes = Instalacao.query.order_by(
            Instalacao.data_agendada.desc()
        ).all()

        dados = []

        total_instalacoes = len(instalacoes)
        total_agendadas = 0
        total_em_andamento = 0
        total_concluidas = 0
        total_canceladas = 0

        for instalacao in instalacoes:
            if instalacao.status == "agendada":
                total_agendadas += 1
            elif instalacao.status == "em_andamento":
                total_em_andamento += 1
            elif instalacao.status == "concluida":
                total_concluidas += 1
            elif instalacao.status == "cancelada":
                total_canceladas += 1

            dados.append({
                "id": instalacao.id,
                "pedido": {
                    "id": instalacao.pedido.id
                } if instalacao.pedido else None,
                "usuario": {
                    "id": instalacao.usuario.id,
                    "nome": instalacao.usuario.nome
                } if instalacao.usuario else None,
                "instalador": {
                    "id": instalacao.instalador.id,
                    "nome": instalacao.instalador.nome
                } if instalacao.instalador else None,
                "data_agendada": (
                    instalacao.data_agendada.isoformat()
                    if instalacao.data_agendada
                    else None
                ),
                "data_inicio": (
                    instalacao.data_inicio.isoformat()
                    if instalacao.data_inicio
                    else None
                ),
                "data_conclusao": (
                    instalacao.data_conclusao.isoformat()
                    if instalacao.data_conclusao
                    else None
                ),
                "status": instalacao.status,
                "endereco": instalacao.endereco,
                "observacoes": instalacao.observacoes
            })

        return resposta_sucesso(
            "Relatório de instalações gerado com sucesso.",
            {
                "total": total_instalacoes,
                "resumo": {
                    "agendadas": total_agendadas,
                    "em_andamento": total_em_andamento,
                    "concluidas": total_concluidas,
                    "canceladas": total_canceladas
                },
                "instalacoes": dados
            }
        )

    except Exception as e:
        db.session.rollback()

        return resposta_erro(
            f"Erro ao gerar relatório de instalações: {str(e)}"
        ), 500


@relatorios_bp.route("/financeiro", methods=["GET"])
@verificar_permissao("relatorios", "visualizar")
def relatorio_financeiro():
    try:
        lancamentos = LancamentoFinanceiro.query.order_by(
            LancamentoFinanceiro.data_lancamento.desc()
        ).all()

        dados = []

        total_receitas = 0
        total_despesas = 0
        total_pendente = 0
        total_pago = 0
        total_cancelado = 0

        for lancamento in lancamentos:
            valor = lancamento.valor or 0

            if lancamento.tipo == "receita":
                total_receitas += valor
            elif lancamento.tipo == "despesa":
                total_despesas += valor

            if lancamento.status == "pendente":
                total_pendente += valor
            elif lancamento.status == "pago":
                total_pago += valor
            elif lancamento.status == "cancelado":
                total_cancelado += valor

            dados.append({
                "id": lancamento.id,
                "tipo": lancamento.tipo,
                "categoria": lancamento.categoria,
                "descricao": lancamento.descricao,
                "valor": valor,
                "pedido": {
                    "id": lancamento.pedido.id
                } if lancamento.pedido else None,
                "fornecedor": {
                    "id": lancamento.fornecedor.id,
                    "nome": lancamento.fornecedor.nome
                } if lancamento.fornecedor else None,
                "usuario": {
                    "id": lancamento.usuario.id,
                    "nome": lancamento.usuario.nome
                } if lancamento.usuario else None,
                "status": lancamento.status,
                "data_lancamento": (
                    lancamento.data_lancamento.isoformat()
                    if lancamento.data_lancamento
                    else None
                ),
                "data_vencimento": (
                    lancamento.data_vencimento.isoformat()
                    if lancamento.data_vencimento
                    else None
                ),
                "data_pagamento": (
                    lancamento.data_pagamento.isoformat()
                    if lancamento.data_pagamento
                    else None
                ),
                "forma_pagamento": lancamento.forma_pagamento,
                "observacoes": lancamento.observacoes
            })

        saldo = total_receitas - total_despesas

        return resposta_sucesso(
            "Relatório financeiro gerado com sucesso.",
            {
                "total": len(dados),
                "resumo": {
                    "receitas": total_receitas,
                    "despesas": total_despesas,
                    "saldo": saldo,
                    "pendente": total_pendente,
                    "pago": total_pago,
                    "cancelado": total_cancelado
                },
                "lancamentos": dados
            }
        )

    except Exception as e:
        db.session.rollback()

        return resposta_erro(
            f"Erro ao gerar relatório financeiro: {str(e)}"
        ), 500