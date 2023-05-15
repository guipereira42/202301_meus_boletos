from meusboletos import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, DateField, DecimalField, SelectField


class BuscaBoleto(FlaskForm):
    data_vencimento_inicio = DateField('Data Início de Vencimento', [validators.Optional()])
    data_vencimento_final = DateField('Data Final de Vencimento', [validators.Optional()])
    buscar = SubmitField('Buscar')


class FormularioBoleto(FlaskForm):
    descricao = StringField('Descrição', [validators.data_required(), validators.Length(min=1, max=50)])
    categoria = StringField('Categoria', [validators.data_required(), validators.Length(min=1, max=40)])
    valor = DecimalField('Valor', [validators.data_required()])
    data_vencimento = DateField('Data de Vencimento', [validators.data_required()])
    data_pagamento = DateField('Data de Pagamento', [validators.Optional()])
    situacao = SelectField('Situação', choices=['Pendente', 'Pago'])
    codigo_boleto = StringField('Código', [validators.data_required(), validators.Length(min=0, max=48)])
    salvar = SubmitField('Salvar')




