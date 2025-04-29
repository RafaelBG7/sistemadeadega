from flask import Blueprint, request, jsonify
from controllers.produtos_controller import cadastrar_produto, listar_produtos

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/cadastrar', methods=['POST'])
def cadastrar():
    try:
        data = request.json
        result, status_code = cadastrar_produto(data)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'message': f'Erro ao cadastrar produto: {str(e)}'}), 500

@produtos_bp.route('/listar', methods=['GET'])
def listar():
    try:
        result = listar_produtos()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': f'Erro ao listar produtos: {str(e)}'}), 500

@produtos_bp.route('/buscar', methods=['GET'])
def buscar_por_nome():
    nome = request.args.get('nome', '')
    if not nome:
        return jsonify([]), 200

    produtos = Produto.query.filter(Produto.produto.ilike(f'%{nome}%')).all()
    produtos_list = [{'id': p.id, 'nome': p.produto} for p in produtos]
    return jsonify(produtos_list), 200