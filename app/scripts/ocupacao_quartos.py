from flask import render_template, request, redirect, url_for, flash
from app.forms import AdicionarQuarto
from app.models import Rooms, Hotels
from app import db


def adicionar_quarto(user_id):
    form = AdicionarQuarto()
    hoteis = Hotels.query.order_by(Hotels.created_at)
    form.hotel_id.choices = [(hotel.id, hotel.name) for hotel in hoteis if hotel.user_id == user_id]

    if request.method == 'POST':
        if form.validate_on_submit():
            room = Rooms.query.filter_by(hotel_id=form.hotel_id.data, number=form.number.data).first()
            if room is None:
                room = Rooms(number=form.number.data,
                             hotel_id=form.hotel_id.data,
                             kind=form.kind.data,
                             phone_extension=form.phone_extension.data,
                             price=form.price.data,
                             guest_limit=form.guest_limit.data,
                             status=form.status.data)
                db.session.add(room)
                db.session.commit()

                flash('Quarto cadastrado com sucesso!')
            else:
                flash('Quarto já existe...')
        return redirect('/adicionar-quarto')

    return render_template('adicionar_quartos.html',
                           form=form,
                           hoteis=hoteis,
                           titulo='Adicionar quarto'
                           )


def ocupacao_quartos(id):
    quartos = Rooms.query.filter_by(hotel_id=id).order_by(Rooms.number)
    return render_template('ocupacao_quartos.html',
                           quartos=quartos
                           )


def editar_quarto(quarto, user_id):

    user_id_room = Rooms\
        .query.filter_by(id=quarto)\
        .join(Hotels, Rooms.hotel_id == Hotels.id).add_columns(Hotels.user_id)
    if [i.user_id for i in user_id_room][0] != user_id:
        return '<h1>Erro! Você não pode acessar este conteúdo!</h1>'

    form = AdicionarQuarto()
    hoteis = Hotels.query.order_by(Hotels.created_at)
    form.hotel_id.choices = [(hotel.id, hotel.name) for hotel in hoteis if hotel.user_id == user_id]

    if form.validate_on_submit():
        if request.method == 'POST':
            to_update = Rooms.query.get_or_404(quarto)
            to_update.hotel_id = request.form['hotel_id']
            to_update.number = request.form['number']
            to_update.kind = request.form['kind']
            to_update.phone_extension = request.form['phone_extension']
            to_update.price = request.form['price']
            to_update.guest_limit = request.form['guest_limit']
            to_update.status = request.form['status']
            db.session.commit()
        return redirect(f"/ocupacao-quartos/{request.form['hotel_id']}")

    room = Rooms.query.filter_by(id=quarto).first()

    form.hotel_id.default = room.hotel_id
    form.process()
    form.number.data = room.number
    form.kind.data = room.kind
    form.phone_extension.data = room.phone_extension
    form.price.data = room.price
    form.guest_limit.data = room.guest_limit
    form.status.data = room.status

    return render_template('adicionar_quartos.html',
                           form=form,
                           titulo='Editar quarto'
                           )