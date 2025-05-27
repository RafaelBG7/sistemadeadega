from flask import Blueprint, request, jsonify
from controllers.vendas_controller import relatorio_por_periodo, relatorio_por_vendedor, relatorio_por_produto, relatorio_por_cliente

relatorios_bp = Blueprint('relatorios', __name__)

@relatorios_bp.route('/periodo', methods=['GET'])
def periodo():
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')
    result = relatorio_por_periodo(inicio, fim)
    return jsonify(result)

@relatorios_bp.route('/vendedor', methods=['GET'])
def vendedor():
    vendedor_id = request.args.get('vendedor_id')
    result = relatorio_por_vendedor(vendedor_id)
    return jsonify(result)

@relatorios_bp.route('/produto', methods=['GET'])
def produto():
    result = relatorio_por_produto()
    return jsonify(result)

@relatorios_bp.route('/cliente', methods=['GET'])
def cliente():
    cliente_id = request.args.get('cliente_id')
    result = relatorio_por_cliente(cliente_id)
    return jsonify(result)