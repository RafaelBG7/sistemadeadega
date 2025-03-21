from flask import Blueprint, request, jsonify
from controllers.vendedores_controller import cadastrar_vendedor, listar_vendedores

vendedores_bp = Blueprint('vendedores', __name__)

@vendedores_bp.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.json
    result = cadastrar_vendedor(data)
    return jsonify(result)

@vendedores_bp.route('/listar', methods=['GET'])
def listar():
    result = listar_vendedores()
    return jsonify(result)
