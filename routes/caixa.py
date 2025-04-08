from flask import Blueprint, jsonify
from controllers.vendas_controller import abrir_caixa, fechar_caixa, status_caixa

caixa_bp = Blueprint('caixa', __name__)

@caixa_bp.route('/abrir', methods=['POST'])
def abrir():
    result = abrir_caixa()
    if isinstance(result, tuple):  # Verifica se há um status code
        return jsonify(result[0]), result[1]
    return jsonify(result)

@caixa_bp.route('/fechar', methods=['POST'])
def fechar():
    result = fechar_caixa()
    if isinstance(result, tuple):  # Verifica se há um status code
        return jsonify(result[0]), result[1]
    return jsonify(result)

@caixa_bp.route('/status', methods=['GET'])
def status():
    result = status_caixa()
    return jsonify(result)