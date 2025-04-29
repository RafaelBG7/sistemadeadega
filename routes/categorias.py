from flask import Blueprint, request, jsonify, make_response
from models.models_adega import db, Categoria

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/cadastrar', methods=['POST'])
def cadastrar_categoria():
    try:
        data = request.json
        if not data.get('nome'):
            return jsonify({'message': 'O nome da categoria é obrigatório!'}), 400

        nova_categoria = Categoria(nome=data['nome'])
        db.session.add(nova_categoria)
        db.session.commit()

        response = make_response(jsonify({'message': 'Categoria cadastrada com sucesso!'}), 201)
        response.headers['Cache-Control'] = 'no-store'
        return response
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao cadastrar categoria: {str(e)}'}), 500

@categorias_bp.route('/listar', methods=['GET'])
def listar_categorias():
    try:
        categorias = Categoria.query.all()
        categorias_list = [{'id': c.id, 'nome': c.nome} for c in categorias]
        response = make_response(jsonify(categorias_list), 200)
        response.headers['Cache-Control'] = 'no-store'
        return response
    except Exception as e:
        return jsonify({'message': f'Erro ao listar categorias: {str(e)}'}), 500