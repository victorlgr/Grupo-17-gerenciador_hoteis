from flask import render_template, request, redirect, url_for, flash
from app.forms import Contas
from app.models import Hotels, User, Guest, Account
from app import db


def adicionar_conta(user_id):
    form = Contas()
    user = User.query.filter_by(id=user_id).first()
    hospedes = Guest.query.order_by(Guest.id)
    hoteis = Hotels.query.filter_by(id=user.hotel_id).order_by(Hotels.created_at)
    if user.hotel_id is None:
        hoteis = Hotels.query.filter_by(user_id=user_id).order_by(Hotels.created_at)
    hoteis_id = [hotel.id for hotel in hoteis]

    form.hotel_id.choices = [(hotel.id, hotel.name) for hotel in hoteis]
    form.guest_id.choices = [(hospede.id, hospede.name) for hospede in hospedes if hospede.hotel_id in hoteis_id]

    if request.method == 'POST':
        if form.validate_on_submit():
            conta = Account(tipo=form.tipo.data,
                            hotel_id=form.hotel_id.data,
                            guest_id=form.guest_id.data,
                            descricao=form.descricao.data,
                            valor=form.valor.data,
                            data_pgto=form.data_pagamento.data)
            db.session.add(conta)
            db.session.commit()

            flash('Conta cadastrada com sucesso!')
        return redirect('/adicionar-conta')

    return render_template('add_conta.html',
                           form=form,
                           titulo='Adicionar conta'
                           )


def listar_contas(user_id):
    user = User.query.filter_by(id=user_id).first()
    hospedes = Guest.query.order_by(Guest.id)
    hoteis = Hotels.query.filter_by(id=user.hotel_id).order_by(Hotels.created_at)
    if user.hotel_id is None:
        hoteis = Hotels.query.filter_by(user_id=user_id).order_by(Hotels.created_at)
    hoteis_id = [hotel.id for hotel in hoteis]

    hotel_choices = dict([(hotel.id, hotel.name) for hotel in hoteis])
    guest_choices = dict([(hospede.id, hospede.name) for hospede in hospedes if hospede.hotel_id in hoteis_id])
    contas = Account.query.filter(Account.hotel_id.in_(hoteis_id)).order_by(Account.id)
    return render_template('lista_contas.html',
                           contas=contas,
                           hotel_choices=hotel_choices,
                           guest_choices=guest_choices,
                           )


def editar_conta(conta_id, user_id):
    form = Contas()
    user = User.query.filter_by(id=user_id).first()
    hospedes = Guest.query.order_by(Guest.id)
    hoteis = Hotels.query.filter_by(id=user.hotel_id).order_by(Hotels.created_at)
    if user.hotel_id is None:
        hoteis = Hotels.query.filter_by(user_id=user_id).order_by(Hotels.created_at)
    hoteis_id = [hotel.id for hotel in hoteis]

    form.hotel_id.choices = [(hotel.id, hotel.name) for hotel in hoteis]
    form.guest_id.choices = [(hospede.id, hospede.name) for hospede in hospedes if hospede.hotel_id in hoteis_id]

    conta = Account.query.filter_by(id=conta_id).first()

    if request.method == 'POST':
        if form.validate_on_submit():
            to_update_conta = Account.query.get_or_404(conta_id)
            to_update_conta.tipo = form.tipo.data
            to_update_conta.hotel_id = form.hotel_id.data
            to_update_conta.guest_id = form.guest_id.data
            to_update_conta.descricao = form.descricao.data
            to_update_conta.valor = form.valor.data
            to_update_conta.data_pgto = form.data_pagamento.data
            db.session.commit()

            flash('Conta editada com sucesso!')
        return redirect('/listar-contas')

    form.tipo.data = conta.tipo
    form.hotel_id.data = conta.hotel_id
    form.guest_id.data = conta.guest_id
    form.descricao.data = conta.descricao
    form.valor.data = conta.valor
    form.data_pagamento.data = conta.data_pgto

    return render_template('add_conta.html',
                           form=form,
                           titulo='Editar conta'
                           )


def deletar_conta(id, user_id):
    conta = Account.query.get_or_404(id)
    db.session.delete(conta)
    db.session.commit()
    flash('Conta deletada com sucesso!', 'success')
    return redirect('/listar-contas')
