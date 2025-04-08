from datetime import datetime
from . import db

class Produto(db.Model):
    __tablename__ = 'produto'

    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    produto = db.Column(db.String(100), nullable=False)
    preco_custo = db.Column(db.Float, nullable=False)
    preco_venda = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, default=0)

    # Relação com vendas
    vendas = db.relationship('Venda', backref='produto', lazy=True)

class Vendedor(db.Model):
    __tablename__ = 'vendedor'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    ativo = db.Column(db.Boolean, default=True)

    # Relação com vendas
    vendas = db.relationship('Venda', backref='vendedor', lazy=True)

class Venda(db.Model):
    __tablename__ = 'venda'

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('vendedor.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    total_venda = db.Column(db.Float, nullable=False)
    lucro = db.Column(db.Float, nullable=False)
    forma_pagamento = db.Column(db.String(20), nullable=False)  # Novo campo para forma de pagamento

class Categoria(db.Model):
    __tablename__ = 'categoria'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    # Relação com produtos
    produtos = db.relationship('Produto', backref='categoria', lazy=True)

class Caixa(db.Model):
    __tablename__ = 'caixa'

    id = db.Column(db.Integer, primary_key=True)
    data_abertura = db.Column(db.DateTime, nullable=False)
    data_fechamento = db.Column(db.DateTime, nullable=True)