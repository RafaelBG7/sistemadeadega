from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='templates', template_folder='templates')
    
    # Configuração básica
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
    
    # Habilitar CORS (para integrar com frontend futuramente)
    CORS(app)

    # Inicializa o banco de dados
    db.init_app(app)

    # Importando e registrando as rotas (blueprints)
    from routes.produtos import produtos_bp
    from routes.vendas import vendas_bp
    from routes.vendedores import vendedores_bp

    app.register_blueprint(produtos_bp, url_prefix='/produtos')
    app.register_blueprint(vendas_bp, url_prefix='/vendas')
    app.register_blueprint(vendedores_bp, url_prefix='/vendedores')

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()

    # Criar as tabelas do banco na primeira execução
    with app.app_context():
        from models import models_adega  # importante para registrar os models antes do create_all
        db.create_all()

    app.run(debug=True)