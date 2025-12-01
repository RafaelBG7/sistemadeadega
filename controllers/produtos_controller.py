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


def estoque_total(limite=10):
    """Retorna o total de unidades em estoque e quantos produtos estão abaixo do `limite`.

    Args:
        limite (int): limite para considerar estoque baixo (padrão 10).

    Returns:
        dict: {'total_estoque': int, 'produtos_abaixo_limite': int}
    """
    produtos = Produto.query.all()
    total_estoque = sum(p.quantidade for p in produtos)
    produtos_abaixo = sum(1 for p in produtos if p.quantidade < limite)

    return {
        'total_estoque': int(total_estoque),
        'produtos_abaixo_limite': int(produtos_abaixo),
        'limite': int(limite)
    }


def valor_total_estoque():
    """Calcula o valor total do estoque com base no preço de custo e no preço de venda.

    Retorna um dicionário com:
      - total_unidades: número total de unidades em estoque
      - valor_custo: valor total pelo preço de custo
      - valor_venda: valor total pelo preço de venda
      - produtos_count: número de produtos distintos
      - margem_media: (valor_venda - valor_custo) / valor_custo (ou None se custo for 0)
    """
    produtos = Produto.query.all()
    total_unidades = sum((p.quantidade or 0) for p in produtos)
    valor_custo = sum(((p.preco_custo or 0.0) * (p.quantidade or 0)) for p in produtos)
    valor_venda = sum(((p.preco_venda or 0.0) * (p.quantidade or 0)) for p in produtos)
    produtos_count = len(produtos)

    margem_media = None
    if valor_custo > 0:
        margem_media = (valor_venda - valor_custo) / valor_custo

    return {
        'total_unidades': int(total_unidades),
        'valor_custo': float(valor_custo),
        'valor_venda': float(valor_venda),
        'produtos_count': int(produtos_count),
        'margem_media': float(margem_media) if margem_media is not None else None
    }