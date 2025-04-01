from models.models_adega import Produto, Venda, Vendedor
from datetime import datetime
from models import db
from sqlalchemy.exc import NoResultFound

def realizar_venda(data):
    print("Dados recebidos para venda:", data)  # Log para depuração
    produtos = data['produtos']
    vendedor = Vendedor.query.get(data['vendedor_id'])
    forma_pagamento = data['forma_pagamento']

    if not vendedor or not vendedor.ativo:
        return {'message': 'Vendedor não encontrado ou inativo'}, 404

    vendas = []
    try:
        for item in produtos:
            produto_nome = item.get('produto_nome')
            quantidade = item.get('quantidade')

            print(f"Processando produto: {produto_nome}, Quantidade: {quantidade}")  # Log para depuração

            # Buscar o produto pelo nome
            produto = Produto.query.filter(Produto.produto.ilike(f'%{produto_nome}%')).first()
            if not produto:
                print(f"Produto com nome '{produto_nome}' não encontrado!")  # Log de erro
                return {'message': f"Produto com nome '{produto_nome}' não encontrado"}, 404

            if produto.quantidade < quantidade:
                print(f"Estoque insuficiente para o produto {produto.produto}")  # Log de erro
                return {'message': f"Estoque insuficiente para o produto {produto.produto}"}, 400

            # Atualizar estoque
            produto.quantidade -= quantidade

            # Calcular total da venda e lucro
            total_venda = produto.preco_venda * quantidade
            lucro = (produto.preco_venda - produto.preco_custo) * quantidade

            # Criar a venda
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
        return {'message': 'Venda realizada com sucesso!'}, 201
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao realizar venda: {str(e)}")  # Log de erro
        return {'message': f"Erro ao realizar venda: {str(e)}"}, 500

def relatorio():
    vendas = Venda.query.all()
    relatorio = []
    for v in vendas:
        relatorio.append({
            'id': v.id,
            'produto': v.produto.produto,  # Nome do produto
            'vendedor': v.vendedor.nome,  # Nome do vendedor
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