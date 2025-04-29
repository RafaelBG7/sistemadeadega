from flask import Blueprint, request, jsonify
from controllers.produtos_controller import cadastrar_produto, listar_produtos
from models.models_adega import Produto, db

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.json
    if not data:
        return jsonify({'message': 'Dados não fornecidos!'}), 400

    result, status_code = cadastrar_produto(data)
    return jsonify(result), status_code

@produtos_bp.route('/listar', methods=['GET'])
def listar():
    result = listar_produtos()
    return jsonify(result)

@produtos_bp.route('/<int:produto_id>', methods=['DELETE'])
def remover(produto_id):
    produto = Produto.query.get(produto_id)
    if not produto:
        return jsonify({'message': 'Produto não encontrado!'}), 404

    try:
        db.session.delete(produto)
        db.session.commit()
        return jsonify({'message': 'Produto removido com sucesso!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao remover produto: {str(e)}'}), 500