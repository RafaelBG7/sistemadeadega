from flask import Blueprint, request, jsonify, render_template
from models import db
from models.promocao import Promocao
from models.models_adega import Produto
from datetime import datetime

promocoes_bp = Blueprint('promocoes', __name__)

@promocoes_bp.route('/', methods=['GET'])
def listar_promocoes():
    promocoes = Promocao.query.all()
    return jsonify([{
        'id': p.id,
        'produto': p.produto.produto,
        'produto_id': p.produto_id,
        'preco_promocional': p.preco_promocional,
        'data_inicio': p.data_inicio.strftime('%Y-%m-%d'),
        'data_fim': p.data_fim.strftime('%Y-%m-%d')
    } for p in promocoes])

@promocoes_bp.route('/', methods=['POST'])
def adicionar_promocao():
    data = request.get_json()
    promocao = Promocao(
        produto_id=data['produto_id'],
        preco_promocional=data['preco_promocional'],
        data_inicio=datetime.strptime(data['data_inicio'], '%Y-%m-%d'),
        data_fim=datetime.strptime(data['data_fim'], '%Y-%m-%d')
    )
    db.session.add(promocao)
    db.session.commit()
    return jsonify({'message': 'Promoção adicionada com sucesso!'})

@promocoes_bp.route('/<int:id>', methods=['PUT'])
def editar_promocao(id):
    promocao = Promocao.query.get_or_404(id)
    data = request.get_json()
    promocao.preco_promocional = data['preco_promocional']
    promocao.data_inicio = datetime.strptime(data['data_inicio'], '%Y-%m-%d')
    promocao.data_fim = datetime.strptime(data['data_fim'], '%Y-%m-%d')
    db.session.commit()
    return jsonify({'message': 'Promoção atualizada com sucesso!'})

@promocoes_bp.route('/<int:id>', methods=['DELETE'])
def remover_promocao(id):
    promocao = Promocao.query.get_or_404(id)
    db.session.delete(promocao)
    db.session.commit()
    return jsonify({'message': 'Promoção removida com sucesso!'})

@promocoes_bp.route('/pagina')
def pagina_promocoes():
    produtos = Produto.query.all()
    return render_template('promocoes.html', produtos=produtos)