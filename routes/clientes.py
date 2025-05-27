from flask import Blueprint, request, jsonify
from controllers.clientes_controller import cadastrar_cliente
from models.models_adega import Cliente

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.json
    if not data:
        return jsonify({'message': 'Dados não fornecidos!'}), 400

    result, status_code = cadastrar_cliente(data)
    return jsonify(result), status_code

@clientes_bp.route('/listar', methods=['GET'])
def listar():
    clientes = Cliente.query.all()
    clientes_list = [
        {
            'id': c.id,
            'nome': c.nome,
            'cpf': c.cpf,
            'data_nascimento': c.data_nascimento.strftime('%Y-%m-%d'),
            'telefone': c.telefone,
            'email': c.email
        }
        for c in clientes
    ]
    return jsonify(clientes_list), 200