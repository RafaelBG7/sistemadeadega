from models.models_adega import Produto
from models.models_adega import db

def cadastrar_produto(data):
    produto = Produto(
        marca=data['marca'],
        produto=data['produto'],
        categoria=data['categoria'],
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
            'marca': p.marca,
            'produto': p.produto,
            'categoria': p.categoria,
            'preco_custo': p.preco_custo,
            'preco_venda': p.preco_venda,
            'quantidade': p.quantidade
        } for p in produtos
    ]
