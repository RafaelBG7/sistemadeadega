from models import Vendedor
from app import db

def cadastrar_vendedor(data):
    vendedor = Vendedor(
        nome=data['nome'],
        email=data['email'],
        telefone=data.get('telefone', ''),
        ativo=True
    )
    db.session.add(vendedor)
    db.session.commit()
    return {'message': 'Vendedor cadastrado com sucesso!'}

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
