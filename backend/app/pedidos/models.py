from database import db


class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id"),
        nullable=False
    )

    orcamento_id = db.Column(
        db.Integer,
        db.ForeignKey("orcamentos.id"),
        nullable=False
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    data = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now()
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="aguardando_producao"
    )

    valor_total = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    entrada = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    restante = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    observacoes = db.Column(
        db.Text,
        nullable=True
    )

    cliente = db.relationship(
        "Cliente",
        foreign_keys=[cliente_id]
    )

    orcamento = db.relationship(
        "Orcamento",
        foreign_keys=[orcamento_id]
    )

    usuario = db.relationship(
        "Usuario",
        foreign_keys=[usuario_id]
    )

    itens = db.relationship(
        "ItemPedido",
        back_populates="pedido",
        cascade="all, delete-orphan"
    )


class ItemPedido(db.Model):
    __tablename__ = "itens_pedido"

    id = db.Column(db.Integer, primary_key=True)

    pedido_id = db.Column(
        db.Integer,
        db.ForeignKey("pedidos.id"),
        nullable=False
    )

    descricao = db.Column(
        db.String(150),
        nullable=False
    )

    quantidade = db.Column(
        db.Float,
        nullable=False,
        default=1
    )

    valor_unitario = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    valor_total = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    observacoes = db.Column(
        db.Text,
        nullable=True
    )

    pedido = db.relationship(
        "Pedido",
        back_populates="itens"
    )


