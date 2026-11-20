from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from database import db
from app.clientes.models import Cliente
from app.clientes.routes import clientes_bp

from app.auth.models import Usuario
from app.auth.routes import auth_bp

from app.estoque.models import Material, Fornecedor, MovimentacaoEstoque
from app.estoque.routes import estoque_bp

from app.orcamentos.models import Orcamento, ItemOrcamento
from app.orcamentos.routes import orcamentos_bp

from app.medicoes.routes import medicoes_bp

from app.pedidos.models import Pedido, ItemPedido
from app.pedidos.routes import pedidos_bp

from app.producao.models import Producao,ItemProducao, MaterialProducao
from app.producao.routes import producao_bp

from app.instalacoes.models import Instalacao
from app.instalacoes.routes import instalacao_bp

from app.financeiro.models import LancamentoFinanceiro
from app.financeiro.routes import financeiro_bp

from app.dashboard.routes import dashboard_bp

from app.agenda.routes import agenda_bp

from app.relatorios.routes import relatorios_bp

from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["JWT_SECRET_KEY"] = "chave-super-secreta-huniglass"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///huniglass.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    migrate = Migrate(app, db)

    jwt = JWTManager(app)
    
    app.register_blueprint(clientes_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(estoque_bp)
    app.register_blueprint(medicoes_bp)
    app.register_blueprint(orcamentos_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(producao_bp)
    app.register_blueprint(instalacao_bp)
    app.register_blueprint(financeiro_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(agenda_bp)
    app.register_blueprint(relatorios_bp)


    with app.app_context():
        db.create_all()

    return app