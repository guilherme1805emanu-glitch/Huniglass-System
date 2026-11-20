from database import db


class Medicao(db.Model):
    __tablename__ = "medicoes"

    id = db.Column(db.Integer, primary_key=True)

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id"),
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

    local_instalacao = db.Column(
        db.String(200),
        nullable=False
    )

    descricao = db.Column(
        db.Text,
        nullable=True
    )

    observacoes = db.Column(
        db.Text,
        nullable=True
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="pendente"
    )

    cliente = db.relationship(
        "Cliente",
        foreign_keys=[cliente_id]
    )

    usuario = db.relationship(
        "Usuario",
        foreign_keys=[usuario_id]
    )

    itens = db.relationship(
        "ItemMedicao",
        back_populates="medicao",
        cascade="all, delete-orphan"
    )


class ItemMedicao(db.Model):
    __tablename__ = "itens_medicao"

    id = db.Column(db.Integer, primary_key=True)

    medicao_id = db.Column(
        db.Integer,
        db.ForeignKey("medicoes.id"),
        nullable=False
    )

    descricao = db.Column(
        db.String(150),
        nullable=False
    )

    largura = db.Column(
        db.Float,
        nullable=False
    )

    altura = db.Column(
        db.Float,
        nullable=False
    )

    quantidade = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    observacoes = db.Column(
        db.Text,
        nullable=True
    )

    medicao = db.relationship(
        "Medicao",
        back_populates="itens"
    )