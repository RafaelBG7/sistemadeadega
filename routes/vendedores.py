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
    try:
        data = request.json
        result, status_code = cadastrar_vendedor(data)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'message': f'Erro ao cadastrar vendedor: {str(e)}'}), 500

@vendedores_bp.route('/listar', methods=['GET'])
def listar():
    try:
        result = listar_vendedores()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': f'Erro ao listar vendedores: {str(e)}'}), 500

@vendedores_bp.route('/<int:vendedor_id>', methods=['PUT'])
def atualizar(vendedor_id):
    try:
        data = request.json
        result, status_code = atualizar_vendedor(vendedor_id, data)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'message': f'Erro ao atualizar vendedor: {str(e)}'}), 500

@vendedores_bp.route('/<int:vendedor_id>', methods=['DELETE'])
def deletar(vendedor_id):
    try:
        result, status_code = deletar_vendedor(vendedor_id)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'message': f'Erro ao deletar vendedor: {str(e)}'}), 500