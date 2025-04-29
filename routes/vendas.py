from flask import Blueprint, request, jsonify
from controllers.vendas_controller import realizar_venda, relatorio, vendas_diarias

vendas_bp = Blueprint('vendas', __name__)

@vendas_bp.route('/realizar', methods=['POST'])
def realizar():
    try:
        data = request.json
        result = realizar_venda(data)
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'message': f'Erro ao realizar venda: {str(e)}'}), 500

@vendas_bp.route('/relatorio', methods=['GET'])
def gerar_relatorio():
    try:
        result = relatorio()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': f'Erro ao gerar relatório: {str(e)}'}), 500

@vendas_bp.route('/diarias', methods=['GET'])
def vendas_diarias_route():
    try:
        result = vendas_diarias()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': f'Erro ao obter vendas diárias: {str(e)}'}), 500