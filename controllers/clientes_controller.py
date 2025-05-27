from models.models_adega import Cliente, db
from datetime import datetime

def cadastrar_cliente(data):
    if not data.get('nome') or not data.get('cpf') or not data.get('data_nascimento') or not data.get('email'):
        return {'message': 'Nome, CPF, data de nascimento e email são obrigatórios!'}, 400

    # Verificar se o CPF ou email já está cadastrado
    if Cliente.query.filter_by(cpf=data['cpf']).first():
        return {'message': 'CPF já cadastrado!'}, 400
    if Cliente.query.filter_by(email=data['email']).first():
        return {'message': 'Email já cadastrado!'}, 400

    try:
        cliente = Cliente(
            nome=data['nome'],
            cpf=data['cpf'],
            data_nascimento=datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date(),
            telefone=data.get('telefone'),
            email=data['email']
        )
        db.session.add(cliente)
        db.session.commit()
        return {'message': 'Cliente cadastrado com sucesso!'}, 201
    except Exception as e:
        db.session.rollback()
        return {'message': f'Erro ao cadastrar cliente: {str(e)}'}, 500