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
        return redirect('/adicionar-quarto')

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
