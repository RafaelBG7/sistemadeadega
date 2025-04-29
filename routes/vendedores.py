from flask import Blueprint, request, jsonify
from controllers.vendedores_controller import (
    cadastrar_vendedor,
    listar_vendedores,
    atualizar_vendedor,
    deletar_vendedor
)

vendedores_bp = Blueprint('vendedores', __name__)

@vendedores_bp.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.json
    if not data:
        return jsonify({'message': 'Dados não fornecidos!'}), 400

    result, status_code = cadastrar_vendedor(data)
    return jsonify(result), status_code

@vendedores_bp.route('/listar', methods=['GET'])
def listar():
    result = listar_vendedores()
    return jsonify(result)

@vendedores_bp.route('/<int:vendedor_id>', methods=['PUT'])
def atualizar(vendedor_id):
    data = request.json
    if not data:
        return jsonify({'message': 'Dados não fornecidos!'}), 400

    result, status_code = atualizar_vendedor(vendedor_id, data)
    return jsonify(result), status_code

@vendedores_bp.route('/<int:vendedor_id>', methods=['DELETE'])
def deletar(vendedor_id):
    result, status_code = deletar_vendedor(vendedor_id)
    return jsonify(result), status_code