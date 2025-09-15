from flask import Blueprint, request, jsonify, render_template
from models import db
from models.conta_pagar import ContaPagar
from datetime import datetime

contas_pagar_bp = Blueprint('contas_pagar', __name__)

@contas_pagar_bp.route('/', methods=['GET'])
def listar_contas():
    contas = ContaPagar.query.all()
    return jsonify([{
        'id': c.id,
        'descricao': c.descricao,
        'valor': c.valor,
        'vencimento': c.vencimento.strftime('%Y-%m-%d'),
        'status': c.status
    } for c in contas])

@contas_pagar_bp.route('/', methods=['POST'])
def adicionar_conta():
    data = request.get_json()
    conta = ContaPagar(
        descricao=data['descricao'],
        valor=data['valor'],
        vencimento=datetime.strptime(data['vencimento'], '%Y-%m-%d'),
        status=data.get('status', 'Pendente')
    )
    db.session.add(conta)
    db.session.commit()
    return jsonify({'message': 'Conta adicionada com sucesso!'})

@contas_pagar_bp.route('/<int:id>', methods=['PUT'])
def editar_conta(id):
    conta = ContaPagar.query.get_or_404(id)
    data = request.get_json()
    conta.descricao = data['descricao']
    conta.valor = data['valor']
    conta.vencimento = datetime.strptime(data['vencimento'], '%Y-%m-%d')
    conta.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Conta atualizada com sucesso!'})

@contas_pagar_bp.route('/<int:id>', methods=['DELETE'])
def remover_conta(id):
    conta = ContaPagar.query.get_or_404(id)
    db.session.delete(conta)
    db.session.commit()
    return jsonify({'message': 'Conta removida com sucesso!'})

@contas_pagar_bp.route('/pagina')
def pagina_contas():
    return render_template('contas_pagar.html')