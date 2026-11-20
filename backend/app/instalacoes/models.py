from database import db


class Instalacao(db.Model):
    __tablename__ = "instalacoes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    pedido_id = db.Column(
        db.Integer,
        db.ForeignKey("pedidos.id"),
        nullable=False,
        unique=True
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    instalador_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    data_agendada = db.Column(
        db.DateTime,
        nullable=True
    )

    data_inicio = db.Column(
        db.DateTime,
        nullable=True
    )

    data_conclusao = db.Column(
        db.DateTime,
        nullable=True
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="agendada"
    )

    endereco = db.Column(
        db.String(200),
        nullable=False
    )

    observacoes = db.Column(
        db.Text,
        nullable=True
    )

    pedido = db.relationship(
        "Pedido",
        foreign_keys=[pedido_id]
    )

    usuario = db.relationship(
        "Usuario",
        foreign_keys=[usuario_id]
    )

    instalador = db.relationship(
        "Usuario",
        foreign_keys=[instalador_id]
    )