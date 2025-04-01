from models.models_adega import Vendedor, db

def cadastrar_vendedor(data):
    if not data.get('nome') or not data.get('email'):
        return {'message': 'Nome e email são obrigatórios!'}, 400

    # Verificar se o email já está cadastrado
    vendedor_existente = Vendedor.query.filter_by(email=data['email']).first()
    if vendedor_existente:
        return {'message': 'Email já cadastrado!'}, 400

    try:
        vendedor = Vendedor(
            nome=data['nome'],
            email=data['email'],
            telefone=data.get('telefone'),
            ativo=data.get('ativo', True)
        )
        db.session.add(vendedor)
        db.session.commit()
        return {'message': 'Vendedor cadastrado com sucesso!'}, 201
    except Exception as e:
        db.session.rollback()
        return {'message': f'Erro ao cadastrar vendedor: {str(e)}'}, 500

def listar_vendedores():
    vendedores = Vendedor.query.all()
    return [
        {
            'id': v.id,
            'nome': v.nome,
            'email': v.email,
            'telefone': v.telefone,
            'ativo': v.ativo
        } for v in vendedores
    ]

def atualizar_vendedor(vendedor_id, data):
    vendedor = Vendedor.query.get(vendedor_id)
    if not vendedor:
        return {'message': 'Vendedor não encontrado!'}, 404

    try:
        vendedor.nome = data.get('nome', vendedor.nome)
        vendedor.email = data.get('email', vendedor.email)
        vendedor.telefone = data.get('telefone', vendedor.telefone)
        vendedor.ativo = data.get('ativo', vendedor.ativo)
        db.session.commit()
        return {'message': 'Vendedor atualizado com sucesso!'}, 200
    except Exception as e:
        db.session.rollback()
        return {'message': f'Erro ao atualizar vendedor: {str(e)}'}, 500

def deletar_vendedor(vendedor_id):
    vendedor = Vendedor.query.get(vendedor_id)
    if not vendedor:
        return {'message': 'Vendedor não encontrado!'}, 404

    try:
        db.session.delete(vendedor)
        db.session.commit()
        return {'message': 'Vendedor deletado com sucesso!'}, 200
    except Exception as e:
        db.session.rollback()
        return {'message': f'Erro ao deletar vendedor: {str(e)}'}, 500
