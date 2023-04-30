from meusboletos import db


class Boletos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    valor = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)
    data_pagamento = db.Column(db.Date, nullable=True)
    situacao = db.Column(db.String(20), nullable=False)
    codigo_boleto = db.Column(db.String(48), nullable=True)

    def __repr__(self):
        return '<Name %r>' % self.name