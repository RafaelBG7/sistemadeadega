from flask import Blueprint, request, jsonify
from controllers.produtos_controller import cadastrar_produto, listar_produtos

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.json
    result = cadastrar_produto(data)
    return jsonify(result)

@produtos_bp.route('/listar', methods=['GET'])
def listar():
    result = listar_produtos()
    return jsonify(result)