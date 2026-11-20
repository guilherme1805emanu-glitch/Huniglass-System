from datetime import datetime, timedelta

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity

from database import db

from app.agenda.models import Agenda
from app.agenda.validators import validar_agenda, validar_edicao_agenda, STATUS_AGENDA, CARGOS_POR_TIPO, validar_conflito_agenda
from app.common.permissions import verificar_permissao, verificar_responsavel_agenda
from app.common.responses import resposta_sucesso, resposta_erro
from app.auth.models import Usuario
from app.clientes.models import Cliente
from app.pedidos.models import Pedido

agenda_bp = Blueprint(
    "agenda",
    __name__,
    url_prefix="/agenda"
)


# ============================================================
# CRIAR ATIVIDADE
# ============================================================

@agenda_bp.route("", methods=["POST"])
@verificar_permissao("agenda", "criar")
def criar_agenda():

    dados = request.get_json()

    if not dados:
        return resposta_erro(
            "Nenhum dado foi enviado.",
            400
        )

    erros = validar_agenda(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    try:
        # ----------------------------------------------------
        # VERIFICAR RESPONSÁVEL
        # ----------------------------------------------------

        usuario = db.session.get(
            Usuario,
            dados["usuario_id"]
        )

        if not usuario:
            return resposta_erro(
                "Usuário responsável não encontrado.",
                404
            )

        if not usuario.ativo:
            return resposta_erro(
                "O usuário responsável está inativo.",
                400
            )

        # ----------------------------------------------------
        # VERIFICAR CARGO DO RESPONSÁVEL
        # ----------------------------------------------------

        cargos_permitidos = CARGOS_POR_TIPO.get(
            dados["tipo"],
            []
        )

        if usuario.cargo not in cargos_permitidos:
            return resposta_erro(
                f"O cargo '{usuario.cargo}' não pode ser responsável por uma atividade do tipo '{dados['tipo']}'.",
                400
            )

        # ----------------------------------------------------
        # VERIFICAR CLIENTE
        # ----------------------------------------------------

        cliente_id = dados.get("cliente_id")

        if cliente_id is not None:

            cliente = db.session.get(
                Cliente,
                cliente_id
            )

            if not cliente:
                return resposta_erro(
                    "Cliente não encontrado.",
                    404
                )

        # ----------------------------------------------------
        # VERIFICAR PEDIDO
        # ----------------------------------------------------

        pedido_id = dados.get("pedido_id")

        if pedido_id is not None:

            pedido = db.session.get(
                Pedido,
                pedido_id
            )

            if not pedido:
                return resposta_erro(
                    "Pedido não encontrado.",
                    404
                )

        # ----------------------------------------------------
        # DATAS
        # ----------------------------------------------------

        data_inicio = datetime.fromisoformat(
            dados["data_inicio"]
        )

        data_fim = None

        if dados.get("data_fim"):
            data_fim = datetime.fromisoformat(
                dados["data_fim"]
            )

        if data_fim and data_fim < data_inicio:
            return resposta_erro(
                "A data de fim não pode ser anterior à data de início.",
                400
            )

        # ----------------------------------------------------
        # VERIFICAR CONFLITO DE HORÁRIO
        # ----------------------------------------------------

        if validar_conflito_agenda(
            dados["usuario_id"],
            data_inicio,
            data_fim
        ):
            return resposta_erro(
                "O responsável já possui uma atividade agendada nesse horário.",
                400
            )

        # ----------------------------------------------------
        # CRIAR AGENDA
        # ----------------------------------------------------

        agenda = Agenda(
            tipo=dados["tipo"],
            cliente_id=cliente_id,
            pedido_id=pedido_id,
            usuario_id=dados["usuario_id"],
            data_inicio=data_inicio,
            data_fim=data_fim,
            status=dados.get(
                "status",
                "agendado"
            ),
            endereco=dados.get("endereco"),
            descricao=dados.get("descricao"),
            observacoes=dados.get("observacoes")
        )

        db.session.add(agenda)
        db.session.commit()

        return resposta_sucesso(
            "Atividade agendada com sucesso.",
            {
                "id": agenda.id,
                "tipo": agenda.tipo,
                "cliente_id": agenda.cliente_id,
                "pedido_id": agenda.pedido_id,
                "usuario_id": agenda.usuario_id,
                "data_inicio": agenda.data_inicio,
                "data_fim": agenda.data_fim,
                "status": agenda.status,
                "endereco": agenda.endereco,
                "descricao": agenda.descricao,
                "observacoes": agenda.observacoes
            },
            201
        )

    except Exception as e:

        db.session.rollback()

        return resposta_erro(
            f"Erro ao criar atividade na agenda: {str(e)}",
            500
        )


@agenda_bp.route("", methods=["GET"])
@verificar_permissao("agenda", "visualizar")
def listar_agenda():

    try:
        atividades = Agenda.query.order_by(
            Agenda.data_inicio.asc()
        ).all()

        dados = []

        for atividade in atividades:
            dados.append({
                "id": atividade.id,
                "tipo": atividade.tipo,
                "cliente_id": atividade.cliente_id,
                "pedido_id": atividade.pedido_id,
                "usuario_id": atividade.usuario_id,
                "data_inicio": atividade.data_inicio,
                "data_fim": atividade.data_fim,
                "status": atividade.status,
                "endereco": atividade.endereco,
                "descricao": atividade.descricao,
                "observacoes": atividade.observacoes
            })

        return resposta_sucesso(
            "Agenda carregada com sucesso.",
            dados
        )

    except Exception as e:

        return resposta_erro(
            f"Erro ao carregar agenda: {str(e)}",
            500
        )


@agenda_bp.route("/<int:id>", methods=["GET"])
@verificar_permissao("agenda", "visualizar")
def buscar_agenda(id):

    atividade = db.session.get(Agenda, id)

    if not atividade:
        return resposta_erro(
            "Atividade da agenda não encontrada.",
            404
        )

    return resposta_sucesso(
        "Atividade carregada com sucesso.",
        {
            "id": atividade.id,
            "tipo": atividade.tipo,
            "cliente_id": atividade.cliente_id,
            "pedido_id": atividade.pedido_id,
            "usuario_id": atividade.usuario_id,
            "data_inicio": atividade.data_inicio,
            "data_fim": atividade.data_fim,
            "status": atividade.status,
            "endereco": atividade.endereco,
            "descricao": atividade.descricao,
            "observacoes": atividade.observacoes
        }
    )


@agenda_bp.route("/<int:id>", methods=["PUT"])
@verificar_permissao("agenda", "editar")
def editar_agenda(id):

    atividade = db.session.get(Agenda, id)

    if not atividade:
        return resposta_erro(
            "Atividade da agenda não encontrada.",
            404
        )

    dados = request.get_json()

    if not dados:
        return resposta_erro(
            "Nenhum dado foi enviado.",
            400
        )

    # Verifica se o usuário logado pode alterar esta atividade
    pode_alterar, mensagem = verificar_responsavel_agenda(atividade)

    if not pode_alterar:
        return resposta_erro(mensagem, 403)

    erros = validar_edicao_agenda(dados)

    if erros:
        return resposta_erro(
            "Dados inválidos.",
            400,
            erros
        )

    try:
        # ----------------------------------------------------
        # VERIFICAR RESPONSÁVEL E CARGO
        # ----------------------------------------------------

        usuario = db.session.get(
            Usuario,
            dados.get("usuario_id", atividade.usuario_id)
        )

        if not usuario:
            return resposta_erro(
                "Usuário responsável não encontrado.",
                404
            )

        if not usuario.ativo:
            return resposta_erro(
                "O usuário responsável está inativo.",
                400
            )

        tipo_final = dados.get(
            "tipo",
            atividade.tipo
        )

        cargos_permitidos = CARGOS_POR_TIPO.get(
            tipo_final,
            []
        )

        if usuario.cargo not in cargos_permitidos:
            return resposta_erro(
                f"O cargo '{usuario.cargo}' não pode ser responsável por uma atividade do tipo '{tipo_final}'.",
                400
            )

        if "usuario_id" in dados:
            usuario_logado_id = int(get_jwt_identity())

            usuario_logado = db.session.get(
                Usuario,
                usuario_logado_id
            )

            if usuario_logado.cargo not in [
                "socio",
                "administrativo"
            ]:
                return resposta_erro(
                    "Você não tem permissão para alterar o responsável pela atividade.",
                    403
                )

            atividade.usuario_id = dados["usuario_id"]

        if "cliente_id" in dados:
            cliente_id = dados["cliente_id"]

            if cliente_id is not None:
                cliente = db.session.get(
                    Cliente,
                    cliente_id
                )

                if not cliente:
                    return resposta_erro(
                        "Cliente não encontrado.",
                        404
                    )

            atividade.cliente_id = cliente_id

        if "pedido_id" in dados:
            pedido_id = dados["pedido_id"]

            if pedido_id is not None:
                pedido = db.session.get(
                    Pedido,
                    pedido_id
                )

                if not pedido:
                    return resposta_erro(
                        "Pedido não encontrado.",
                        404
                    )

            atividade.pedido_id = pedido_id

        if "tipo" in dados:
            atividade.tipo = dados["tipo"]

        if "data_inicio" in dados:
            atividade.data_inicio = datetime.fromisoformat(
                dados["data_inicio"]
            )

        if "data_fim" in dados:
            atividade.data_fim = (
                datetime.fromisoformat(dados["data_fim"])
                if dados["data_fim"]
                else None
            )

        if atividade.data_fim and atividade.data_fim < atividade.data_inicio:
            return resposta_erro(
                "A data de fim não pode ser anterior à data de início.",
                400
            )

        # ----------------------------------------------------
        # VERIFICAR CONFLITO DE HORÁRIO
        # ----------------------------------------------------

        if validar_conflito_agenda(
            atividade.usuario_id,
            atividade.data_inicio,
            atividade.data_fim,
            atividade.id
        ):
            return resposta_erro(
                "O responsável já possui uma atividade agendada nesse horário.",
                400
            )

        if "status" in dados:
            atividade.status = dados["status"]

        if "endereco" in dados:
            atividade.endereco = dados["endereco"]

        if "descricao" in dados:
            atividade.descricao = dados["descricao"]

        if "observacoes" in dados:
            atividade.observacoes = dados["observacoes"]

        db.session.commit()

        return resposta_sucesso(
            "Atividade atualizada com sucesso.",
            {
                "id": atividade.id,
                "tipo": atividade.tipo,
                "cliente_id": atividade.cliente_id,
                "pedido_id": atividade.pedido_id,
                "usuario_id": atividade.usuario_id,
                "data_inicio": atividade.data_inicio,
                "data_fim": atividade.data_fim,
                "status": atividade.status,
                "endereco": atividade.endereco,
                "descricao": atividade.descricao,
                "observacoes": atividade.observacoes
            }
        )

    except Exception as e:

        db.session.rollback()

        return resposta_erro(
            f"Erro ao editar atividade da agenda: {str(e)}",
            500
        )



@agenda_bp.route("/<int:id>", methods=["DELETE"])
@verificar_permissao("agenda", "excluir")
def excluir_agenda(id):

    atividade = db.session.get(Agenda, id)

    if not atividade:
        return resposta_erro(
            "Atividade da agenda não encontrada.",
            404
        )

    try:
        db.session.delete(atividade)
        db.session.commit()

        return resposta_sucesso(
            "Atividade excluída com sucesso."
        )

    except Exception as e:

        db.session.rollback()

        return resposta_erro(
            f"Erro ao excluir atividade da agenda: {str(e)}",
            500
        )


@agenda_bp.route("/dia", methods=["GET"])
@verificar_permissao("agenda", "visualizar")
def agenda_dia():

    data = request.args.get("data")

    if not data:
        return resposta_erro(
            "O parâmetro data é obrigatório. Use o formato YYYY-MM-DD.",
            400
        )

    try:
        data_inicio = datetime.strptime(
            data,
            "%Y-%m-%d"
        )

        data_fim = data_inicio + timedelta(days=1)

        atividades = Agenda.query.filter(
            Agenda.data_inicio >= data_inicio,
            Agenda.data_inicio < data_fim
        ).order_by(
            Agenda.data_inicio.asc()
        ).all()

        dados = []

        for atividade in atividades:
            dados.append({
                "id": atividade.id,
                "tipo": atividade.tipo,
                "cliente_id": atividade.cliente_id,
                "pedido_id": atividade.pedido_id,
                "usuario_id": atividade.usuario_id,
                "data_inicio": atividade.data_inicio,
                "data_fim": atividade.data_fim,
                "status": atividade.status,
                "endereco": atividade.endereco,
                "descricao": atividade.descricao,
                "observacoes": atividade.observacoes
            })

        return resposta_sucesso(
            "Agenda do dia carregada com sucesso.",
            dados
        )

    except ValueError:

        return resposta_erro(
            "A data deve estar no formato YYYY-MM-DD.",
            400
        )

    except Exception as e:

        return resposta_erro(
            f"Erro ao carregar agenda do dia: {str(e)}",
            500
        )


@agenda_bp.route("/semana", methods=["GET"])
@verificar_permissao("agenda", "visualizar")
def agenda_semana():

    data = request.args.get("data")

    if not data:
        return resposta_erro(
            "O parâmetro data é obrigatório. Use o formato YYYY-MM-DD.",
            400
        )

    try:
        data_referencia = datetime.strptime(
            data,
            "%Y-%m-%d"
        )

        # Segunda-feira da semana
        data_inicio = data_referencia - timedelta(
            days=data_referencia.weekday()
        )

        # Segunda-feira da próxima semana
        data_fim = data_inicio + timedelta(days=7)

        atividades = Agenda.query.filter(
            Agenda.data_inicio >= data_inicio,
            Agenda.data_inicio < data_fim
        ).order_by(
            Agenda.data_inicio.asc()
        ).all()

        dados = []

        for atividade in atividades:
            dados.append({
                "id": atividade.id,
                "tipo": atividade.tipo,
                "cliente_id": atividade.cliente_id,
                "pedido_id": atividade.pedido_id,
                "usuario_id": atividade.usuario_id,
                "data_inicio": atividade.data_inicio,
                "data_fim": atividade.data_fim,
                "status": atividade.status,
                "endereco": atividade.endereco,
                "descricao": atividade.descricao,
                "observacoes": atividade.observacoes
            })

        return resposta_sucesso(
            "Agenda da semana carregada com sucesso.",
            dados
        )

    except ValueError:

        return resposta_erro(
            "A data deve estar no formato YYYY-MM-DD.",
            400
        )

    except Exception as e:

        return resposta_erro(
            f"Erro ao carregar agenda da semana: {str(e)}",
            500
        )


@agenda_bp.route("/mes", methods=["GET"])
@verificar_permissao("agenda", "visualizar")
def agenda_mes():

    data = request.args.get("data")

    if not data:
        return resposta_erro(
            "O parâmetro data é obrigatório. Use o formato YYYY-MM-DD.",
            400
        )

    try:
        data_referencia = datetime.strptime(
            data,
            "%Y-%m-%d"
        )

        # Primeiro dia do mês
        data_inicio = data_referencia.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        # Primeiro dia do próximo mês
        if data_inicio.month == 12:
            data_fim = data_inicio.replace(
                year=data_inicio.year + 1,
                month=1
            )
        else:
            data_fim = data_inicio.replace(
                month=data_inicio.month + 1
            )

        atividades = Agenda.query.filter(
            Agenda.data_inicio >= data_inicio,
            Agenda.data_inicio < data_fim
        ).order_by(
            Agenda.data_inicio.asc()
        ).all()

        dados = []

        for atividade in atividades:
            dados.append({
                "id": atividade.id,
                "tipo": atividade.tipo,
                "cliente_id": atividade.cliente_id,
                "pedido_id": atividade.pedido_id,
                "usuario_id": atividade.usuario_id,
                "data_inicio": atividade.data_inicio,
                "data_fim": atividade.data_fim,
                "status": atividade.status,
                "endereco": atividade.endereco,
                "descricao": atividade.descricao,
                "observacoes": atividade.observacoes
            })

        return resposta_sucesso(
            "Agenda do mês carregada com sucesso.",
            dados
        )

    except ValueError:

        return resposta_erro(
            "A data deve estar no formato YYYY-MM-DD.",
            400
        )

    except Exception as e:

        return resposta_erro(
            f"Erro ao carregar agenda do mês: {str(e)}",
            500
        )


@agenda_bp.route("/responsavel/<int:usuario_id>", methods=["GET"])
@verificar_permissao("agenda", "visualizar")
def agenda_responsavel(usuario_id):

    usuario_logado_id = int(get_jwt_identity())

    usuario_logado = db.session.get(
        Usuario,
        usuario_logado_id
    )

    if not usuario_logado:
        return resposta_erro(
            "Usuário logado não encontrado.",
            404
        )

    usuario = db.session.get(
        Usuario,
        usuario_id
    )

    if not usuario:
        return resposta_erro(
            "Usuário não encontrado.",
            404
        )

    cargos_admin = [
        "socio",
        "administrativo"
    ]

    if usuario_logado.cargo not in cargos_admin:
        if usuario_logado_id != usuario_id:
            return resposta_erro(
                "Você só pode consultar sua própria agenda.",
                403
            )

    query = Agenda.query.filter(
        Agenda.usuario_id == usuario_id
    )

    data = request.args.get("data")
    status = request.args.get("status")

    if status and status not in STATUS_AGENDA:
        return resposta_erro(
            "Status inválido. Use: agendado, em_andamento, concluido ou cancelado.",
            400
        )

    if data:
        try:
            data_inicio = datetime.strptime(
                data,
                "%Y-%m-%d"
            )

            data_fim = data_inicio + timedelta(days=1)

            query = query.filter(
                Agenda.data_inicio >= data_inicio,
                Agenda.data_inicio < data_fim
            )

        except ValueError:
            return resposta_erro(
                "A data deve estar no formato YYYY-MM-DD.",
                400
            )

    if status:
        query = query.filter(
            Agenda.status == status
        )

    atividades = query.order_by(
        Agenda.data_inicio.asc()
    ).all()

    dados = []

    for atividade in atividades:
        dados.append({
            "id": atividade.id,
            "tipo": atividade.tipo,
            "cliente_id": atividade.cliente_id,
            "pedido_id": atividade.pedido_id,
            "usuario_id": atividade.usuario_id,
            "data_inicio": atividade.data_inicio,
            "data_fim": atividade.data_fim,
            "status": atividade.status,
            "endereco": atividade.endereco,
            "descricao": atividade.descricao,
            "observacoes": atividade.observacoes
        })

    return resposta_sucesso(
        "Agenda do responsável carregada com sucesso.",
        dados
    )