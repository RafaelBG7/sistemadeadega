from flask import Blueprint, request, jsonify
from controllers.produtos_controller import cadastrar_produto, listar_produtos

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.json
    if not data:
        return jsonify({'message': 'Dados não fornecidos!'}), 400

    # Chamar a função do controlador e desempacotar os valores retornados
    result, status_code = cadastrar_produto(data)
    return jsonify(result), status_code

@produtos_bp.route('/listar', methods=['GET'])
def listar():
    result = listar_produtos()
    return jsonify(result)

@produtos_bp.route('/buscar', methods=['GET'])
def buscar_por_nome():
    nome = request.args.get('nome', '')
    if not nome:
        return jsonify([]), 200

    produtos = Produto.query.filter(Produto.produto.ilike(f'%{nome}%')).all()
    produtos_list = [{'id': p.id, 'nome': p.produto} for p in produtos]
    return jsonify(produtos_list), 200