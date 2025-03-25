from flask import Blueprint, request, jsonify
from models.models_adega import db, Marca

marcas_bp = Blueprint('marcas', __name__)

@marcas_bp.route('/cadastrar', methods=['POST'])
def cadastrar_marca():
    data = request.json
    nova_marca = Marca(nome=data['nome'])
    db.session.add(nova_marca)
    db.session.commit()
    return jsonify({'message': 'Marca cadastrada com sucesso!'}), 201

@marcas_bp.route('/listar', methods=['GET'])
def listar_marcas():
    marcas = Marca.query.all()
    marcas_list = [{'id': m.id, 'nome': m.nome} for m in marcas]
    return jsonify(marcas_list)