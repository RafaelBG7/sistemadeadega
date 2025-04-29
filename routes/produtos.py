from flask import Blueprint, request, jsonify
from models.models_adega import db, Produto

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/cadastrar', methods=['POST'])
def cadastrar_produto():
    try:
        data = request.json
        print("Dados recebidos no backend:", data)  # Log para depuração

        # Validação dos campos obrigatórios
        if not data.get('produto') or not data.get('categoria_id') or not data.get('preco_custo') or not data.get('preco_venda'):
            return jsonify({'message': 'Todos os campos obrigatórios devem ser preenchidos!'}), 400

        # Criar o produto
        novo_produto = Produto(
            produto=data['produto'],
            categoria_id=data['categoria_id'],
            preco_custo=data['preco_custo'],
            preco_venda=data['preco_venda'],
            quantidade=data.get('quantidade', 0)
        )
        db.session.add(novo_produto)
        db.session.commit()

        return jsonify({'message': 'Produto cadastrado com sucesso!'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao cadastrar produto: {str(e)}")  # Log de erro
        return jsonify({'message': f'Erro ao cadastrar produto: {str(e)}'}), 500

@produtos_bp.route('/listar', methods=['GET'])
def listar_produtos():
    try:
        produtos = Produto.query.all()
        produtos_list = [
            {
                'id': p.id,
                'produto': p.produto,
                'categoria_id': p.categoria_id,
                'preco_custo': p.preco_custo,
                'preco_venda': p.preco_venda,
                'quantidade': p.quantidade
            }
            for p in produtos
        ]
        return jsonify(produtos_list), 200
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