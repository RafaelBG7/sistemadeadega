from flask import Blueprint, jsonify, request
from controllers.vendas_controller import abrir_caixa, fechar_caixa, status_caixa

caixa_bp = Blueprint('caixa', __name__)

@caixa_bp.route('/abrir', methods=['POST'])
def abrir():
    try:
        result = abrir_caixa()
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
        return jsonify({'message': 'Caixa aberto com sucesso!', 'status': 'Aberto'}), 200
    except Exception as e:
        return jsonify({'message': f'Erro ao abrir o caixa: {str(e)}'}), 500

@caixa_bp.route('/fechar', methods=['POST'])
def fechar():
    try:
        result = fechar_caixa()
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
        return jsonify({'message': 'Caixa fechado com sucesso!', 'status': 'Fechado'}), 200
    except Exception as e:
        return jsonify({'message': f'Erro ao fechar o caixa: {str(e)}'}), 500

@caixa_bp.route('/status', methods=['GET'])
def status():
    try:
        result = status_caixa()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': f'Erro ao obter o status do caixa: {str(e)}'}), 500