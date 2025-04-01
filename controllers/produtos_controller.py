from models.models_adega import Produto, db

def cadastrar_produto(data):
    # Validação dos dados recebidos
    if not data.get('produto') or not data.get('categoria_id') or not data.get('preco_custo') or not data.get('preco_venda'):
        return {'message': 'Todos os campos obrigatórios devem ser preenchidos!'}, 400

    try:
        produto = Produto(
            produto=data['produto'],
            categoria_id=data['categoria_id'],
            preco_custo=data['preco_custo'],
            preco_venda=data['preco_venda'],
            quantidade=data.get('quantidade', 0)
        )
        db.session.add(produto)
        db.session.commit()
        return {'message': 'Produto cadastrado com sucesso!'}, 201
    except Exception as e:
        db.session.rollback()
        return {'message': f'Erro ao cadastrar produto: {str(e)}'}, 500

def listar_produtos():
    produtos = Produto.query.all()
    return [
        {
            'id': p.id,
            'produto': p.produto,
            'categoria_id': p.categoria_id,
            'preco_custo': p.preco_custo,
            'preco_venda': p.preco_venda,
            'quantidade': p.quantidade
        } for p in produtos
    ]