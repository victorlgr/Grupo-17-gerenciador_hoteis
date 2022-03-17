from flask import render_template, request, redirect, url_for, flash
from app.forms import AdicionarQuarto
from app.models import Rooms
from app import db


def adicionar_quarto():
    form = AdicionarQuarto()

    if request.method == 'POST':
        if form.validate_on_submit():
            room = Rooms.query.filter_by(number=form.number.data).first()
            if room is None:
                room = Rooms(number=form.number.data,
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
                           form=form
                           )


def ocupacao_quartos():
    quartos = Rooms.query.order_by(Rooms.created_at)
    return render_template('ocupacao_quartos.html',
                           quartos=quartos
                           )


def editar_quarto(quarto):
    form = AdicionarQuarto()

    if form.validate_on_submit():
        if request.method == 'POST':
            to_update = Rooms.query.get_or_404(quarto)
            to_update.number = request.form['number']
            to_update.kind = request.form['kind']
            to_update.phone_extension = request.form['phone_extension']
            to_update.price = request.form['price']
            to_update.guest_limit = request.form['guest_limit']
            to_update.status = request.form['status']
            db.session.commit()
        return redirect('/ocupacao-quartos')

    room = Rooms.query.filter_by(id=quarto).first()

    form.number.data = room.number
    form.kind.data = room.kind
    form.phone_extension.data = room.phone_extension
    form.price.data = room.price
    form.guest_limit.data = room.guest_limit
    form.status.data = room.status

    return render_template('editar_quarto.html',
                           form=form
                           )