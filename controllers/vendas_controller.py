from models.models_adega import Produto, Venda, Vendedor, Caixa
from datetime import datetime, date
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

def vendas_diarias():
    hoje = date.today()
    vendas = Venda.query.filter(Venda.data >= datetime(hoje.year, hoje.month, hoje.day)).all()

    total_vendas = sum(v.total_venda for v in vendas)
    lucro_total = sum(v.lucro for v in vendas)

    formas_pagamento = {}
    for v in vendas:
        formas_pagamento[v.forma_pagamento] = formas_pagamento.get(v.forma_pagamento, 0) + v.total_venda

    return {
        'total_vendas': total_vendas,
        'lucro_total': lucro_total,
        'formas_pagamento': formas_pagamento
    }

def abrir_caixa():
    caixa_aberto = Caixa.query.filter_by(data_fechamento=None).first()
    if caixa_aberto:
        return {'message': 'Já existe um caixa aberto!'}, 400

    try:
        novo_caixa = Caixa(data_abertura=datetime.utcnow())
        db.session.add(novo_caixa)
        db.session.commit()
        print("Caixa aberto com sucesso!")  # Log para depuração
        return {'message': 'Caixa aberto com sucesso!'}
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao abrir caixa: {str(e)}")  # Log de erro
        return {'message': f"Erro ao abrir caixa: {str(e)}"}, 500

def fechar_caixa():
    caixa_aberto = Caixa.query.filter_by(data_fechamento=None).first()
    if not caixa_aberto:
        return {'message': 'Nenhum caixa aberto encontrado!'}, 400

    try:
        caixa_aberto.data_fechamento = datetime.utcnow()
        db.session.commit()
        print("Caixa fechado com sucesso!")  # Log para depuração
        return {'message': 'Caixa fechado com sucesso!'}
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao fechar caixa: {str(e)}")  # Log de erro
        return {'message': f"Erro ao fechar caixa: {str(e)}"}, 500

def status_caixa():
    caixa_aberto = Caixa.query.filter_by(data_fechamento=None).first()
    if caixa_aberto:
        return {
            'status': 'Aberto',
            'data_abertura': caixa_aberto.data_abertura.strftime('%d/%m/%Y %H:%M'),
            'id': caixa_aberto.id
        }
    return {'status': 'Fechado'}