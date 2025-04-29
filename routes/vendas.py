from flask import Blueprint, request, jsonify
from controllers.vendas_controller import realizar_venda, relatorio, vendas_diarias

vendas_bp = Blueprint('vendas', __name__)

@vendas_bp.route('/realizar', methods=['POST'])
def realizar():
    data = request.json
    result = realizar_venda(data)
    if isinstance(result, tuple):  # Caso de erro com status code
        return jsonify(result[0]), result[1]
    return jsonify(result)

@vendas_bp.route('/relatorio', methods=['GET'])
def gerar_relatorio():
    result = relatorio()
    return jsonify(result)

@vendas_bp.route('/diarias', methods=['GET'])
def vendas_diarias_route():
    result = vendas_diarias()
    return jsonify(result)