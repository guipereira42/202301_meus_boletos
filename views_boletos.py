from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from sqlalchemy import func

from meusboletos import app, db
from models import Boletos
from helpers import FormularioBoleto, BuscaBoleto
import time


@app.route('/')
def index():

    form = BuscaBoleto(request.form)
    if form is None:
        form = BuscaBoleto()

    lista = Boletos.query.order_by(Boletos.id)
    return render_template('lista.html', titulo='Meus Boletos', boletos=lista, proxima='index', form=form)


@app.route('/novo')
def novo():
    form = FormularioBoleto()
    return render_template('novo.html', titulo='Novo Boleto', form=form)


@app.route('/criar', methods=['POST',])
def criar():

    form = FormularioBoleto(request.form)

    if not form.validate_on_submit():
        flash('Erro na validação!')
        return redirect(url_for('novo'))

    descricao = form.descricao.data
    categoria = form.categoria.data
    valor = form.valor.data
    data_vencimento = form.data_vencimento.data
    data_pagamento = form.data_pagamento.data
    situacao = form.situacao.data
    codigo_boleto = form.codigo_boleto.data

    boleto = Boletos.query.filter_by(codigo_boleto=codigo_boleto).first()

    if boleto:
        flash('Boleto já existente!')
        return redirect(url_for('index'))

    novo_boleto = Boletos(descricao=descricao, categoria=categoria, valor=valor, data_vencimento=data_vencimento,
                          data_pagamento=data_pagamento, situacao=situacao, codigo_boleto=codigo_boleto)
    db.session.add(novo_boleto)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):

    proxima = request.args.get('proxima')
    data_vencimento_inicio = request.args.get('data_vencimento_inicio')
    data_vencimento_final = request.args.get('data_vencimento_final')
    boleto = Boletos.query.filter_by(id=id).first()

    form = FormularioBoleto()

    form.descricao.data = boleto.descricao
    form.categoria.data = boleto.categoria
    form.valor.data = boleto.valor
    form.data_vencimento.data = boleto.data_vencimento
    form.data_pagamento.data = boleto.data_pagamento
    form.situacao.data = boleto.situacao
    form.codigo_boleto.data = boleto.codigo_boleto

    return render_template('editar.html', titulo='Editando Boleto', id=id, form=form, proxima=proxima,
                           data_vencimento_inicio=data_vencimento_inicio, data_vencimento_final=data_vencimento_final)


@app.route('/atualizar', methods=['POST',])
def atualizar():

    proxima = request.args.get('proxima')
    data_vencimento_inicio = request.args.get('data_vencimento_inicio')
    data_vencimento_final = request.args.get('data_vencimento_final')
    form = FormularioBoleto(request.form)

    if form.validate_on_submit():
        boleto = Boletos.query.filter_by(id=request.form['id']).first()
        boleto.descricao = form.descricao.data
        boleto.categoria = form.categoria.data
        boleto.valor = form.valor.data
        boleto.data_vencimento = form.data_vencimento.data
        boleto.data_pagamento = form.data_pagamento.data
        boleto.situacao = form.situacao.data
        boleto.codigo_boleto = form.codigo_boleto.data

        db.session.add(boleto)
        db.session.commit()

    return redirect(url_for(proxima, data_vencimento_inicio=data_vencimento_inicio, data_vencimento_final=data_vencimento_final))


@app.route('/deletar/<int:id>')
def deletar(id):
    data_vencimento_inicio = request.args.get('data_vencimento_inicio')
    data_vencimento_final = request.args.get('data_vencimento_final')
    proxima = request.args.get('proxima')
    Boletos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Boleto deletado com sucesso.')
    return redirect(url_for(proxima, data_vencimento_inicio=data_vencimento_inicio, data_vencimento_final=data_vencimento_final))


@app.route('/busca', methods=['GET', 'POST'])
def busca():

    form = BuscaBoleto()
    data_vencimento_inicio = next(data for data in [form.data_vencimento_inicio.data,
                                                    request.args.get('data_vencimento_inicio'),
                                                    db.session.query(func.min(Boletos.data_vencimento)).scalar()] if data is not None)
    data_vencimento_final = next(data for data in [form.data_vencimento_final.data,
                                                   request.args.get('data_vencimento_final'),
                                                   db.session.query(func.max(Boletos.data_vencimento)).scalar()] if data is not None)

    lista = Boletos.query.filter(Boletos.data_vencimento.between(data_vencimento_inicio, data_vencimento_final)) \
        .order_by(Boletos.data_vencimento).all()

    return render_template('lista.html', titulo='Busca de Boletos', boletos=lista, proxima='busca', form=form,
                           data_vencimento_inicio=data_vencimento_inicio, data_vencimento_final=data_vencimento_final)

