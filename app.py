from flask import Flask, render_template
from flask_cors import CORS
from models import db
from models.models_adega import Produto, Venda, Vendedor, Categoria  # Removido Marca
from routes.produtos import produtos_bp
from routes.vendas import vendas_bp
from routes.vendedores import vendedores_bp
from routes.categorias import categorias_bp
from routes.caixa import caixa_bp
from routes.home import home_bp
from routes.relatorios import relatorios_bp

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    
    # Configuração básica
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
    
    # Habilitar CORS
    CORS(app)

    # Inicializa o banco de dados
    db.init_app(app)

    # Registrar blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(produtos_bp, url_prefix='/produtos')
    app.register_blueprint(vendas_bp, url_prefix='/vendas')
    app.register_blueprint(vendedores_bp, url_prefix='/vendedores')
    app.register_blueprint(categorias_bp, url_prefix='/categorias')
    app.register_blueprint(caixa_bp, url_prefix='/caixa')
    app.register_blueprint(relatorios_bp, url_prefix='/relatorios')

    @app.route('/categoria')
    def categoria():
        return render_template('categoria.html')

    @app.route('/produto')
    def produto():
        return render_template('produto.html')

    @app.route('/venda')
    def venda():
        return render_template('venda.html')

    @app.route('/vendas-diarias')
    def vendas_diarias():
        return render_template('vendas_diarias.html')

    @app.route('/caixa')
    def caixa():
        return render_template('caixa.html')

    @app.route('/vendedor')
    def vendedor():
        return render_template('vendedor.html')
    
    @app.route('/relatorios')
    def relatorios():
        return render_template('relatorios.html')


    return app

if __name__ == '__main__':
    app = create_app()

    # Criar as tabelas do banco na primeira execução
    with app.app_context():
        db.create_all()

    app.run(debug=True)