from database import db


class Orcamento(db.Model):
    __tablename__ = "orcamentos"

    id = db.Column(db.Integer, primary_key=True)

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id"),
        nullable=False
    )

    medicao_id = db.Column(
        db.Integer,
        db.ForeignKey("medicoes.id"),
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

    validade = db.Column(
        db.Date,
        nullable=True
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="rascunho"
    )

    subtotal = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    desconto = db.Column(
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

    cliente = db.relationship(
        "Cliente",
        foreign_keys=[cliente_id]
    )

    medicao = db.relationship(
        "Medicao",
        foreign_keys=[medicao_id]
    )

    usuario = db.relationship(
        "Usuario",
        foreign_keys=[usuario_id]
    )

    itens = db.relationship(
        "ItemOrcamento",
        back_populates="orcamento",
        cascade="all, delete-orphan"
    )


class ItemOrcamento(db.Model):
    __tablename__ = "itens_orcamento"

    id = db.Column(db.Integer, primary_key=True)

    orcamento_id = db.Column(
        db.Integer,
        db.ForeignKey("orcamentos.id"),
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

    orcamento = db.relationship(
        "Orcamento",
        back_populates="itens"
    )