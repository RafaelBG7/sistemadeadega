from models.models_adega import Produto, Venda, Vendedor
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 

def realizar_venda(data):
    produto = Produto.query.get(data['produto_id'])
    vendedor = Vendedor.query.get(data['vendedor_id'])
    quantidade = data['quantidade']

    if not produto:
        return {'message': 'Produto não encontrado'}, 404
    if not vendedor or not vendedor.ativo:
        return {'message': 'Vendedor não encontrado ou inativo'}, 404
    if produto.quantidade < quantidade:
        return {'message': 'Estoque insuficiente'}, 400

    produto.quantidade -= quantidade
    total_venda = produto.preco_venda * quantidade
    lucro = (produto.preco_venda - produto.preco_custo) * quantidade

    venda = Venda(
        produto_id=produto.id,
        vendedor_id=vendedor.id,
        quantidade=quantidade,
        total_venda=total_venda,
        lucro=lucro,
        data=datetime.utcnow()
    )

    db.session.add(venda)
    db.session.commit()
    return {'message': 'Venda realizada com sucesso!'}

def relatorio():
    vendas = Venda.query.all()
    relatorio = []
    for v in vendas:
        relatorio.append({
            'id': v.id,
            'produto': v.produto.produto,
            'marca': v.produto.marca,
            'vendedor': v.vendedor.nome,
            'quantidade': v.quantidade,
            'data': v.data.strftime('%d/%m/%Y %H:%M'),
            'total_venda': v.total_venda,
            'lucro': v.lucro
        })
    
    total = sum(v['total_venda'] for v in relatorio)
    lucro_total = sum(v['lucro'] for v in relatorio)
    
    return {
        'total_vendas': total,
        'lucro_total': lucro_total,
        'vendas': relatorio
    }
