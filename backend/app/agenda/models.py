from database import db


class Agenda(db.Model):
    __tablename__ = "agenda"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    tipo = db.Column(
        db.String(30),
        nullable=False
    )

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id"),
        nullable=True
    )

    pedido_id = db.Column(
        db.Integer,
        db.ForeignKey("pedidos.id"),
        nullable=True
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    data_inicio = db.Column(
        db.DateTime,
        nullable=False
    )

    data_fim = db.Column(
        db.DateTime,
        nullable=True
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="agendado"
    )

    endereco = db.Column(
        db.String(200),
        nullable=True
    )

    descricao = db.Column(
        db.String(200),
        nullable=True
    )

    observacoes = db.Column(
        db.Text,
        nullable=True
    )

    cliente = db.relationship(
        "Cliente",
        foreign_keys=[cliente_id]
    )

    pedido = db.relationship(
        "Pedido",
        foreign_keys=[pedido_id]
    )

    usuario = db.relationship(
        "Usuario",
        foreign_keys=[usuario_id]
    )