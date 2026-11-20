from database import db


class LancamentoFinanceiro(db.Model):
    __tablename__ = "lancamentos_financeiros"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    tipo = db.Column(
        db.String(20),
        nullable=False
    )

    categoria = db.Column(
        db.String(50),
        nullable=False
    )

    descricao = db.Column(
        db.String(200),
        nullable=False
    )

    valor = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    pedido_id = db.Column(
        db.Integer,
        db.ForeignKey("pedidos.id"),
        nullable=True
    )

    fornecedor_id = db.Column(
        db.Integer,
        db.ForeignKey("fornecedores.id"),
        nullable=True
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="pendente"
    )

    data_lancamento = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now()
    )

    data_vencimento = db.Column(
        db.Date,
        nullable=True
    )

    data_pagamento = db.Column(
        db.DateTime,
        nullable=True
    )

    forma_pagamento = db.Column(
        db.String(30),
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

    fornecedor = db.relationship(
        "Fornecedor",
        foreign_keys=[fornecedor_id]
    )

    usuario = db.relationship(
        "Usuario",
        foreign_keys=[usuario_id]
    )