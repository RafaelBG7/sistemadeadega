from . import db

class Promocao(db.Model):
    __tablename__ = 'promocao'
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    preco_promocional = db.Column(db.Float, nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)

    produto = db.relationship('Produto', backref='promocoes')