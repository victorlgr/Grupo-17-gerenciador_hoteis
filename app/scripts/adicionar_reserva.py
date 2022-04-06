from flask import render_template, request, redirect, url_for, flash
from app.forms import AdicionarReserva
from app.models import Hotels, Addresses, Rooms, Guest
from app import db


def adicionar_reserva(user_id):
    form = AdicionarReserva()
    hotel = Hotels.query.order_by(Hotels.created_at).first()
    rooms = Rooms.query.filter_by(hotel_id=hotel.id).order_by(Rooms.number)
    guests = Guest.query.filter_by(hotel_id=hotel.id).order_by(Guest.name)
    form.room_id.choices = [(room.id, room.number) for room in rooms]
    # form.guest_id.choices = [(guest.id, guest.name) for guest in guests]

    if request.method == 'POST':
        if form.validate_on_submit():
            hotel = Hotels.query.filter_by(name=form.cnpj.data).first()
            if hotel is None:
                address = Addresses(street=form.endereco.data,
                                    neighborhood=form.bairro.data,
                                    city=form.cidade.data,
                                    state=form.estado.data,
                                    country=form.pais.data,
                                    zip_code=form.cep.data,
                                    number=form.numero.data,
                                    complement=form.complemento.data)

                db.session.add(address)
                db.session.flush()

                hotel = Hotels(name=form.name.data,
                               phone=form.phone.data,
                               email=form.email.data,
                               cnpj=form.cnpj.data,
                               address_id=address.id,
                               user_id=user_id)

                db.session.add(hotel)
                db.session.commit()

                flash('Hotel cadastrado com sucesso!')
            else:
                flash('Hotel já existe...')
        return redirect('/adicionar-hotel')

    return render_template('add_reserva.html',
                           form=form,
                           titulo='Adicionar Reserva'
                           )