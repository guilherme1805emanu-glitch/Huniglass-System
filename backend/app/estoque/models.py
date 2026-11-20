from database import db


class Material(db.Model):
    __tablename__ = "materiais"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(150),
        nullable=False
    )

    categoria = db.Column(
        db.String(100),
        nullable=False
    )

    unidade = db.Column(
        db.String(30),
        nullable=False
    )

    quantidade = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    estoque_minimo = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    fornecedor_id = db.Column(
        db.Integer,
        db.ForeignKey("fornecedores.id"),
        nullable=True
    )

    ativo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    observacoes = db.Column(
        db.Text,
        nullable=True
    )

    fornecedor = db.relationship(
        "Fornecedor",
        back_populates="materiais"
    )

    movimentacoes = db.relationship(
        "MovimentacaoEstoque",
        back_populates="material",
        cascade="all, delete-orphan"
    )

class Fornecedor(db.Model):
    __tablename__ = "fornecedores"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(150),
        nullable=False
    )

    telefone = db.Column(
        db.String(20),
        nullable=True
    )

    email = db.Column(
        db.String(150),
        nullable=True
    )

    cpf_cnpj = db.Column(
        db.String(20),
        nullable=True
    )

    endereco = db.Column(
        db.String(200),
        nullable=True
    )

    cidade = db.Column(
        db.String(100),
        nullable=True
    )

    estado = db.Column(
        db.String(2),
        nullable=True
    )

    observacoes = db.Column(
        db.Text,
        nullable=True
    )

    ativo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    materiais = db.relationship(
        "Material",
        back_populates="fornecedor"
    )

class MovimentacaoEstoque(db.Model):
    __tablename__ = "movimentacoes_estoque"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    material_id = db.Column(
        db.Integer,
        db.ForeignKey("materiais.id"),
        nullable=False
    )

    tipo = db.Column(
        db.String(20),
        nullable=False
    )

    quantidade = db.Column(
        db.Float,
        nullable=False
    )

    data = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now()
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    observacao = db.Column(
        db.Text,
        nullable=True
    )

    material = db.relationship(
        "Material",
        back_populates="movimentacoes"
    )

    usuario = db.relationship(
        "Usuario",
        foreign_keys=[usuario_id]
    )