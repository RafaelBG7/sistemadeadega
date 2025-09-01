from flask import Blueprint, request, jsonify, render_template
from models import db
from models.lote import Lote
from models.models_adega import Produto
from datetime import datetime

lotes_bp = Blueprint('lotes', __name__)

@lotes_bp.route('/', methods=['GET'])
def listar_lotes():
    lotes = Lote.query.all()
    resultado = []
    for lote in lotes:
        resultado.append({
            'id': lote.id,
            'produto': lote.produto.produto,  # campo correto do modelo Produto
            'produto_id': lote.produto_id,
            'numero_lote': lote.numero_lote,
            'validade': lote.validade.strftime('%Y-%m-%d'),
            'quantidade': lote.quantidade
        })
    return jsonify(resultado)

@lotes_bp.route('/', methods=['POST'])
def adicionar_lote():
    data = request.get_json()
    lote = Lote(
        produto_id=data['produto_id'],
        numero_lote=data['numero_lote'],
        validade=datetime.strptime(data['validade'], '%Y-%m-%d'),
        quantidade=data['quantidade']
    )
    db.session.add(lote)
    db.session.commit()
    return jsonify({'message': 'Lote adicionado com sucesso!'})

@lotes_bp.route('/<int:id>', methods=['PUT'])
def editar_lote(id):
    lote = Lote.query.get_or_404(id)
    data = request.get_json()
    lote.numero_lote = data['numero_lote']
    lote.validade = datetime.strptime(data['validade'], '%Y-%m-%d')
    lote.quantidade = data['quantidade']
    db.session.commit()
    return jsonify({'message': 'Lote atualizado com sucesso!'})

@lotes_bp.route('/<int:id>', methods=['DELETE'])
def remover_lote(id):
    lote = Lote.query.get_or_404(id)
    db.session.delete(lote)
    db.session.commit()
    return jsonify({'message': 'Lote removido com sucesso!'})

@lotes_bp.route('', methods=['GET'])
def pagina_lotes():
    produtos = Produto.query.all()
    return render_template('lotes.html', produtos=produtos)