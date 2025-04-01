from models.models_adega import Produto, Venda, Vendedor
from datetime import datetime
from models import db

def realizar_venda(data):
    print("Dados recebidos para venda:", data)  # Log para depuração
    produtos = data['produtos']
    vendedor = Vendedor.query.get(data['vendedor_id'])
    forma_pagamento = data['forma_pagamento']

    if not vendedor or not vendedor.ativo:
        return {'message': 'Vendedor não encontrado ou inativo'}, 404

    vendas = []
    for item in produtos:
        produto = Produto.query.get(item['produto_id'])
        quantidade = item['quantidade']

        if not produto:
            return {'message': f"Produto com ID {item['produto_id']} não encontrado"}, 404
        if produto.quantidade < quantidade:
            return {'message': f"Estoque insuficiente para o produto {produto.produto}"}, 400

        produto.quantidade -= quantidade
        total_venda = produto.preco_venda * quantidade
        lucro = (produto.preco_venda - produto.preco_custo) * quantidade

        venda = Venda(
            produto_id=produto.id,
            vendedor_id=vendedor.id,
            quantidade=quantidade,
            total_venda=total_venda,
            lucro=lucro,
            data=datetime.utcnow(),
            forma_pagamento=forma_pagamento
        )
        vendas.append(venda)
        db.session.add(venda)

    db.session.commit()
    print("Vendas realizadas com sucesso:", vendas)  # Log para depuração
    return {'message': 'Venda realizada com sucesso!'}

def relatorio():
    vendas = Venda.query.all()
    relatorio = []
    for v in vendas:
        relatorio.append({
            'id': v.id,
            'produto': v.produto.produto,
            'marca': v.produto.marca.nome,
            'vendedor': v.vendedor.nome,
            'quantidade': v.quantidade,
            'data': v.data.strftime('%d/%m/%Y %H:%M'),
            'total_venda': v.total_venda,
            'lucro': v.lucro,
            'forma_pagamento': v.forma_pagamento
        })
    
    total = sum(v['total_venda'] for v in relatorio)
    lucro_total = sum(v['lucro'] for v in relatorio)
    
    print("Relatório gerado:", relatorio)  # Log para depuração
    return {
        'total_vendas': total,
        'lucro_total': lucro_total,
        'vendas': relatorio
    }