from flask import Blueprint, request, jsonify
from models.models_adega import db, Categoria

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/cadastrar', methods=['POST'])
def cadastrar_categoria():
    data = request.json
    nova_categoria = Categoria(nome=data['nome'])
    db.session.add(nova_categoria)
    db.session.commit()
    return jsonify({'message': 'Categoria cadastrada com sucesso!'}), 201

@categorias_bp.route('/listar', methods=['GET'])
def listar_categorias():
    categorias = Categoria.query.all()
    categorias_list = [{'id': c.id, 'nome': c.nome} for c in categorias]
    return jsonify(categorias_list)

@categorias_bp.route('/buscar', methods=['GET'])
def buscar_por_nome():
    nome = request.args.get('nome', '')
    if not nome:
        return jsonify([]), 200

    categorias = Categoria.query.filter(Categoria.nome.ilike(f'%{nome}%')).all()
    categorias_list = [{'id': c.id, 'nome': c.nome} for c in categorias]
    return jsonify(categorias_list), 200