from flask import Blueprint, request, jsonify, Response
from controllers.vendas_controller import relatorio_por_periodo, relatorio_por_vendedor, relatorio_por_produto, relatorio_por_cliente
import csv
import io

relatorios_bp = Blueprint('relatorios', __name__)

@relatorios_bp.route('/periodo', methods=['GET'])
def periodo():
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')
    result = relatorio_por_periodo(inicio, fim)
    return jsonify(result)


@relatorios_bp.route('/periodo/export', methods=['GET'])
def periodo_export():
    """Gera e retorna um CSV com o relatório de vendas no período informado.
    Parâmetros esperados: `inicio` e `fim` no formato YYYY-MM-DD.
    Exemplo: /relatorios/periodo/export?inicio=2025-01-01&fim=2025-01-31
    """
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')

    if not inicio or not fim:
        return jsonify({'error': 'Parâmetros "inicio" e "fim" são obrigatórios (YYYY-MM-DD).'}), 400

    result = relatorio_por_periodo(inicio, fim)
    if isinstance(result, dict) and result.get('error'):
        return jsonify(result), 400

    # Gerar CSV
    output = io.StringIO()
    writer = csv.writer(output)

    # Cabeçalho
    writer.writerow(['id', 'produto', 'vendedor', 'quantidade', 'data', 'total_venda', 'lucro', 'forma_pagamento'])

    for v in result.get('vendas', []):
        writer.writerow([
            v.get('id'),
            v.get('produto'),
            v.get('vendedor'),
            v.get('quantidade'),
            v.get('data'),
            v.get('total_venda'),
            v.get('lucro'),
            v.get('forma_pagamento')
        ])

    csv_data = output.getvalue()
    output.close()

    filename = f"relatorio_vendas_{inicio}_a_{fim}.csv"
    resp = Response(csv_data, mimetype='text/csv')
    resp.headers['Content-Disposition'] = f'attachment; filename={filename}'
    return resp

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