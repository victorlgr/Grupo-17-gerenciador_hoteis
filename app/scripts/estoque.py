from flask import render_template, request, redirect, url_for, flash
from app.forms import Estoque
from app.models import Hotels, User, Inventory
from app import db


def adicionar_estoque(user_id):
    form = Estoque()
    user = User.query.filter_by(id=user_id).first()
    hoteis = Hotels.query.filter_by(id=user.hotel_id).order_by(Hotels.created_at)
    if user.hotel_id is None:
        hoteis = Hotels.query.filter_by(user_id=user_id).order_by(Hotels.created_at)

    form.hotel_id.choices = [(hotel.id, hotel.name) for hotel in hoteis]

    if request.method == 'POST':
        print(form.data)
        if form.validate_on_submit():
            estoque = Inventory(hotel_id=form.hotel_id.data,
                                categoria=form.categoria.data,
                                nome=form.nome.data,
                                detalhes=form.detalhes.data)
            db.session.add(estoque)
            db.session.commit()

            flash('Estoque cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_estoque_endpoint'))

    return render_template('add_estoque.html',
                           form=form,
                           titulo='Adicionar estoque'
                           )


def listar_estoque(user_id):
    user = User.query.filter_by(id=user_id).first()
    hoteis = Hotels.query.filter_by(id=user.hotel_id).order_by(Hotels.created_at)
    if user.hotel_id is None:
        hoteis = Hotels.query.filter_by(user_id=user_id).order_by(Hotels.created_at)
    hoteis_id = [hotel.id for hotel in hoteis]

    hotel_choices = dict([(hotel.id, hotel.name) for hotel in hoteis])
    estoques = Inventory.query.filter(Inventory.hotel_id.in_(hoteis_id)).order_by(Inventory.id)
    return render_template('lista_estoque.html',
                           estoques=estoques,
                           hotel_choices=hotel_choices
                           )


def editar_estoque(estoque_id, user_id):
    form = Estoque()
    user = User.query.filter_by(id=user_id).first()
    hoteis = Hotels.query.filter_by(id=user.hotel_id).order_by(Hotels.created_at)
    if user.hotel_id is None:
        hoteis = Hotels.query.filter_by(user_id=user_id).order_by(Hotels.created_at)
    hoteis_id = [hotel.id for hotel in hoteis]

    form.hotel_id.choices = [(hotel.id, hotel.name) for hotel in hoteis]

    estoque = Inventory.query.filter_by(id=estoque_id).first()

    if request.method == 'POST':
        if form.validate_on_submit():
            to_update_estoque = Inventory.query.get_or_404(estoque_id)
            to_update_estoque.hotel_id = form.hotel_id.data
            to_update_estoque.categoria = form.categoria.data
            to_update_estoque.nome = form.nome.data
            to_update_estoque.detales = form.detalhes.data
            db.session.commit()

            flash('Estoque editado com sucesso!', 'success')
        return redirect(url_for('listar_estoque_endpoint'))

    form.hotel_id.data = estoque.hotel_id
    form.categoria.data = estoque.categoria
    form.nome.data = estoque.nome
    form.detalhes.data = estoque.detalhes

    return render_template('add_estoque.html',
                           form=form,
                           titulo='Editar estoque'
                           )


def deletar_estoque(id, user_id):
    estoque = Inventory.query.get_or_404(id)
    db.session.delete(estoque)
    db.session.commit()
    flash('Estoque deletado com sucesso!', 'success')
    return redirect(url_for('listar_estoque_endpoint'))
