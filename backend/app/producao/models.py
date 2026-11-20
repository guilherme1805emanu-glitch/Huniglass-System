from database import db


class Producao(db.Model):
    __tablename__ = "producoes"

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

    status = db.Column(
        db.String(30),
        nullable=False,
        default="aguardando"
    )

    data_inicio = db.Column(
        db.DateTime,
        nullable=True
    )

    data_previsao = db.Column(
        db.DateTime,
        nullable=True
    )

    data_conclusao = db.Column(
        db.DateTime,
        nullable=True
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

    itens = db.relationship(
        "ItemProducao",
        back_populates="producao",
        cascade="all, delete-orphan"
    )


class ItemProducao(db.Model):
    __tablename__ = "itens_producao"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    producao_id = db.Column(
        db.Integer,
        db.ForeignKey("producoes.id"),
        nullable=False
    )

    item_pedido_id = db.Column(
        db.Integer,
        db.ForeignKey("itens_pedido.id"),
        nullable=False
    )

    quantidade = db.Column(
        db.Float,
        nullable=False,
        default=1
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="aguardando"
    )

    observacoes = db.Column(
        db.Text,
        nullable=True
    )

    producao = db.relationship(
        "Producao",
        back_populates="itens"
    )

    item_pedido = db.relationship(
        "ItemPedido",
        foreign_keys=[item_pedido_id]
    )


class MaterialProducao(db.Model):
    __tablename__ = "materiais_producao"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    producao_id = db.Column(
        db.Integer,
        db.ForeignKey("producoes.id"),
        nullable=False
    )

    material_id = db.Column(
        db.Integer,
        db.ForeignKey("materiais.id"),
        nullable=False
    )

    quantidade = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    consumido = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    data_consumo = db.Column(
        db.DateTime,
        nullable=True
    )

    observacoes = db.Column(
        db.Text,
        nullable=True
    )

    producao = db.relationship(
        "Producao",
        foreign_keys=[producao_id]
    )

    material = db.relationship(
        "Material",
        foreign_keys=[material_id]
    )