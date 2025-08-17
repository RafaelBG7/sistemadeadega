from flask import Blueprint, request, jsonify
from models import db
from models.fornecedor import Fornecedor

fornecedores_bp = Blueprint('fornecedores', __name__)

@fornecedores_bp.route('/', methods=['GET'])
def listar_fornecedores():
    fornecedores = Fornecedor.query.all()
    return jsonify([{'id': f.id, 'nome': f.nome, 'cnpj': f.cnpj, 'telefone': f.telefone, 'email': f.email, 'endereco': f.endereco} for f in fornecedores])

@fornecedores_bp.route('/', methods=['POST'])
def adicionar_fornecedor():
    data = request.json
    fornecedor = Fornecedor(
        nome=data.get('nome'),
        cnpj=data.get('cnpj'),
        telefone=data.get('telefone'),
        email=data.get('email'),
        endereco=data.get('endereco')
    )
    db.session.add(fornecedor)
    db.session.commit()
    return jsonify({'message': 'Fornecedor adicionado com sucesso!'}), 201

@fornecedores_bp.route('/<int:id>', methods=['PUT'])
def editar_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    data = request.json
    fornecedor.nome = data.get('nome', fornecedor.nome)
    fornecedor.cnpj = data.get('cnpj', fornecedor.cnpj)
    fornecedor.telefone = data.get('telefone', fornecedor.telefone)
    fornecedor.email = data.get('email', fornecedor.email)
    fornecedor.endereco = data.get('endereco', fornecedor.endereco)
    db.session.commit()
    return jsonify({'message': 'Fornecedor atualizado com sucesso!'})

@fornecedores_bp.route('/<int:id>', methods=['DELETE'])
def deletar_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    db.session.delete(fornecedor)
    db.session.commit()
    return jsonify({'message': 'Fornecedor removido com sucesso!'})
