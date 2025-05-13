from flask import Blueprint, request, jsonify
from controllers.produtos_controller import cadastrar_produto, listar_produtos
from models.models_adega import Produto, Categoria, db

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

@produtos_bp.route('/estoque-baixo', methods=['GET'])
def estoque_baixo():
    limite = request.args.get('limite', 10, type=int)  # Limite padrão: 10 unidades
    produtos = Produto.query.filter(Produto.quantidade < limite).all()
    produtos_list = [
        {
            'id': p.id,
            'produto': p.produto,
            'quantidade': p.quantidade,
            'categoria': p.categoria.nome
        }
        for p in produtos
    ]
    return jsonify(produtos_list), 200

@produtos_bp.route('/editar/<int:produto_id>', methods=['PUT'])
def editar_produto(produto_id):
    try:
        data = request.json
        produto = Produto.query.get(produto_id)

        if not produto:
            return jsonify({'message': 'Produto não encontrado!'}), 404

        # Atualizar os campos do produto
        produto.produto = data.get('produto', produto.produto)
        produto.preco_custo = data.get('preco_custo', produto.preco_custo)
        produto.preco_venda = data.get('preco_venda', produto.preco_venda)
        produto.quantidade = data.get('quantidade', produto.quantidade)

        # Atualizar a categoria, se fornecida
        categoria_id = data.get('categoria_id')
        if categoria_id:
            categoria = Categoria.query.get(categoria_id)
            if not categoria:
                return jsonify({'message': 'Categoria não encontrada!'}), 404
            produto.categoria_id = categoria_id

        db.session.commit()

        return jsonify({'message': 'Produto atualizado com sucesso!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao editar produto: {str(e)}'}), 500