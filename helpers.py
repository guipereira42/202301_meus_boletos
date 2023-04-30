from meusboletos import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, DateField, DecimalField


class FormularioBoleto(FlaskForm):
    descricao = StringField('Descrição', [validators.data_required(), validators.Length(min=1, max=50)])
    categoria = StringField('Categoria', [validators.data_required(), validators.Length(min=1, max=40)])
    valor = DecimalField('Valor', [validators.data_required()])
    data_vencimento = DateField('Data de Vencimento', [validators.data_required()])
    data_pagamento = DateField('Data de Pagamento', [validators.Optional()])
    situacao = StringField('Situação', [validators.data_required(), validators.Length(min=1, max=20)])
    codigo_boleto = StringField('Código', [validators.data_required(), validators.Length(min=0, max=48)])
    salvar = SubmitField('Salvar')




