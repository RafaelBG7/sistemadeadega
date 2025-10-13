from models.models_adega import Produto, Venda, Vendedor, Caixa, Cliente
from datetime import datetime, date
from models import db
from sqlalchemy.exc import NoResultFound
from sqlalchemy import func, and_

def realizar_venda(data):
    print("Dados recebidos para venda:", data)  # Log para depuração
    produtos = data['produtos']
    vendedor = Vendedor.query.get(data['vendedor_id'])
    forma_pagamento = data['forma_pagamento']
    cliente_id = data.get('cliente_id')
    cliente = Cliente.query.get(cliente_id) if cliente_id else None

    if not vendedor or not vendedor.ativo:
        return {'message': 'Vendedor não encontrado ou inativo'}, 404

    vendas = []
    desconto_aplicado = False
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

            # Fidelidade: aplicar desconto se houver
            desconto = 0.0
            if cliente and cliente.fidelidade_ativo and not desconto_aplicado:
                desconto = total_venda * 0.05
                total_venda -= desconto
                cliente.fidelidade_ativo = False  # Desativa o desconto após uso
                desconto_aplicado = True

            # Criar a venda
            venda = Venda(
                produto_id=produto.id,
                vendedor_id=vendedor.id,
                quantidade=quantidade,
                total_venda=total_venda,
                lucro=lucro,
                data=datetime.utcnow(),  # Aqui a data está sendo definida
                forma_pagamento=forma_pagamento,
                cliente_id=cliente_id  # <-- NOVO
            )
            vendas.append(venda)
            db.session.add(venda)

        db.session.flush()  # Garante que as vendas estão na sessão

        # Fidelidade: acumular crédito e ativar desconto se necessário
        if cliente:
            valor_gasto = sum(v.total_venda for v in vendas)
            cliente.fidelidade_credito += valor_gasto
            while cliente.fidelidade_credito >= 100:
                cliente.fidelidade_credito -= 100
                cliente.fidelidade_ativo = True  # Ativa desconto para próxima compra

        db.session.commit()
        print("Vendas realizadas com sucesso:", vendas)  # Log para depuração
        valor_total = sum(v.total_venda for v in vendas)
        return {
            'message': 'Venda realizada com sucesso!',
            'valor_total': valor_total
        }, 201
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

def relatorio_por_periodo(inicio, fim):
    try:
        # Log para depuração
        print(f"Gerando relatório para o período: {inicio} a {fim}")

        # Converter as datas de string para datetime
        inicio_date = datetime.strptime(inicio, '%Y-%m-%d')
        fim_date = datetime.strptime(fim, '%Y-%m-%d')

        # Ajustar o fim_date para incluir o final do dia
        fim_date = fim_date.replace(hour=23, minute=59, second=59)

        # Log para depuração
        print(f"Datas convertidas: início={inicio_date}, fim={fim_date}")

        # Filtrar vendas no intervalo de datas
        vendas = Venda.query.filter(Venda.data >= inicio_date, Venda.data <= fim_date).all()

        # Log para depuração
        print(f"Vendas encontradas: {len(vendas)}")

        # Calcular total de vendas e lucro
        total_vendas = sum(v.total_venda for v in vendas)
        lucro_total = sum(v.lucro for v in vendas)

        # Criar o relatório detalhado
        relatorio = [
            {
                'id': v.id,
                'produto': v.produto.produto,
                'vendedor': v.vendedor.nome,
                'quantidade': v.quantidade,
                'data': v.data.strftime('%d/%m/%Y %H:%M'),
                'total_venda': v.total_venda,
                'lucro': v.lucro,
                'forma_pagamento': v.forma_pagamento
            }
            for v in vendas
        ]

        return {
            'total_vendas': total_vendas,
            'lucro_total': lucro_total,
            'vendas': relatorio
        }
    except ValueError as ve:
        print(f"Erro de conversão de datas: {ve}")
        return {'error': 'Formato de data inválido. Use o formato YYYY-MM-DD.'}
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
        return {'error': str(e)}

def relatorio_por_vendedor(vendedor_id):
    try:
        vendas = Venda.query.filter_by(vendedor_id=vendedor_id).all()
        total_vendas = sum(v.total_venda for v in vendas)
        lucro_total = sum(v.lucro for v in vendas)

        relatorio = [
            {
                'id': v.id,
                'produto': v.produto.produto,
                'quantidade': v.quantidade,
                'data': v.data.strftime('%d/%m/%Y %H:%M'),
                'total_venda': v.total_venda,
                'lucro': v.lucro,
                'forma_pagamento': v.forma_pagamento
            }
            for v in vendas
        ]

        return {
            'total_vendas': total_vendas,
            'lucro_total': lucro_total,
            'vendas': relatorio
        }
    except Exception as e:
        return {'error': str(e)}

def relatorio_por_produto():
    try:
        produtos = Produto.query.all()
        relatorio = []

        for produto in produtos:
            vendas = Venda.query.filter_by(produto_id=produto.id).all()
            total_vendas = sum(v.total_venda for v in vendas)
            lucro_total = sum(v.lucro for v in vendas)

            relatorio.append({
                'produto': produto.produto,
                'total_vendas': total_vendas,
                'lucro_total': lucro_total
            })

        return relatorio
    except Exception as e:
        return {'error': str(e)}

def relatorio_por_cliente(cliente_id):
    try:
        vendas = Venda.query.filter_by(cliente_id=cliente_id).all()
        total_vendas = sum(v.total_venda for v in vendas)
        lucro_total = sum(v.lucro for v in vendas)

        relatorio = [
            {
                'id': v.id,
                'produto': v.produto.produto,
                'quantidade': v.quantidade,
                'data': v.data.strftime('%d/%m/%Y %H:%M'),
                'total_venda': v.total_venda,
                'lucro': v.lucro,
                'forma_pagamento': v.forma_pagamento
            }
            for v in vendas
        ]

        return {
            'total_vendas': total_vendas,
            'lucro_total': lucro_total,
            'vendas': relatorio
        }
    except Exception as e:
        return {'error': str(e)}


def ranking_vendedores_por_mes(year=None, month=None):
    """Retorna ranking de vendedores por quantidade vendida no mês especificado.
    Se year ou month não forem fornecidos, usa o mês atual.
    Retorna dict com 'ranking' (lista de vendedores ordenada) e 'vendedor_do_mes' (o topo, ou None).
    """
    try:
        hoje = datetime.utcnow()
        if year is None or month is None:
            year = hoje.year
            month = hoje.month

        inicio = datetime(year, month, 1)
        # calcular fim do mês: próximo mês menos 1 segundo
        if month == 12:
            fim = datetime(year + 1, 1, 1)
        else:
            fim = datetime(year, month + 1, 1)

        # Usar outer join para incluir vendedores sem vendas (quantidade 0)
        query = db.session.query(
            Vendedor.id.label('vendedor_id'),
            Vendedor.nome.label('vendedor_nome'),
            func.coalesce(func.sum(Venda.quantidade), 0).label('quantidade_total'),
            func.coalesce(func.sum(Venda.total_venda), 0.0).label('valor_total')
        ).outerjoin(Venda, and_(Venda.vendedor_id == Vendedor.id, Venda.data >= inicio, Venda.data < fim))

        query = query.group_by(Vendedor.id).order_by(func.coalesce(func.sum(Venda.quantidade), 0).desc())

        results = query.all()

        ranking = []
        for row in results:
            ranking.append({
                'vendedor_id': row.vendedor_id,
                'vendedor_nome': row.vendedor_nome,
                'quantidade_total': int(row.quantidade_total),
                'valor_total': float(row.valor_total)
            })

        vendedor_do_mes = ranking[0] if ranking and ranking[0]['quantidade_total'] > 0 else None

        return {
            'year': year,
            'month': month,
            'ranking': ranking,
            'vendedor_do_mes': vendedor_do_mes
        }
    except Exception as e:
        print(f"Erro ao calcular ranking de vendedores: {e}")
        return {'error': str(e)}