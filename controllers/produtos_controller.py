from models.models_adega import Produto, db

def cadastrar_produto(data):
    produto = Produto(
        produto=data['produto'],
        categoria_id=data['categoria_id'],
        preco_custo=data['preco_custo'],
        preco_venda=data['preco_venda'],
        quantidade=data.get('quantidade', 0)
    )
    db.session.add(produto)
    db.session.commit()
    return {'message': 'Produto cadastrado com sucesso!'}

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