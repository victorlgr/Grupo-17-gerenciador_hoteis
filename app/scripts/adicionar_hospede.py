from flask import render_template, request, redirect, url_for, flash
from app.forms import AdicionarHospede, VerificarDisponibilidade
from app.models import Hotels, Addresses, Guest, User
from datetime import datetime
from app import db


def adicionar_hospede(user_id):
    form_reserva = VerificarDisponibilidade()
    form = AdicionarHospede()
    user = User.query.filter_by(id=user_id).first()

    if user.hotel_id is None:
        hoteis = Hotels.query.order_by(Hotels.created_at)
        form.hotel_id.choices = [(hotel.id, hotel.name) for hotel in hoteis if hotel.user_id == user_id]
    else:
        hoteis = Hotels.query.filter_by(id=user.hotel_id).order_by(Hotels.created_at)
        form.hotel_id.choices = [(hotel.id, hotel.name) for hotel in hoteis]

    if request.method == 'POST':
        if form.validate_on_submit():
            guest = Guest.query.filter_by(cpf=form.cpf.data).first()
            if guest is None:
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

                birthday = datetime.strptime(form.birthday.data, "%d/%m/%Y")

                guest = Guest(name=form.name.data,
                              phone=form.phone.data,
                              email=form.email.data,
                              cpf=form.cpf.data,
                              birthday=birthday,
                              hotel_id=form.hotel_id.data,
                              address_id=address.id)

                db.session.add(guest)
                db.session.commit()

                flash('Hóspede cadastrado com sucesso!', 'success')
            else:
                flash('Hóspede já existe...', 'danger')
        return redirect(url_for('adicionar_hospede_endpoint'))

    return render_template('add_hospede.html',
                           form=form,
                           titulo='Adicionar Hospede', form_reserva=form_reserva,
                           user=user
                           )


def listar_hospedes(user_id):
    user = User.query.filter_by(id=user_id).first()
    hoteis = Hotels.query.filter_by(id=user.hotel_id).order_by(Hotels.created_at)
    if user.hotel_id is None:
        hoteis = Hotels.query.filter_by(user_id=user_id).order_by(Hotels.created_at)
    hoteis_id = [hotel.id for hotel in hoteis]
    hospedes = Guest.query.filter(Guest.hotel_id.in_(hoteis_id)).order_by(Guest.id)

    hotel_choices = dict([(hotel.id, hotel.name) for hotel in hoteis])
    return render_template('lista_hospedes.html',
                           hospedes=hospedes,
                           hotel_choices=hotel_choices
                           )


def editar_hospede(hospede_id, user_id):
    form = AdicionarHospede()
    user = User.query.filter_by(id=user_id).first()
    hospede = Guest.query.get_or_404(hospede_id)
    address_data = Addresses.query.filter_by(id=hospede.address_id).first()
    hoteis = Hotels.query.filter_by(id=user.hotel_id).order_by(Hotels.created_at)
    if user.hotel_id is None:
        hoteis = Hotels.query.filter_by(user_id=user_id).order_by(Hotels.created_at)

    form.hotel_id.choices = [(hotel.id, hotel.name) for hotel in hoteis]

    if request.method == 'POST':
        if form.validate_on_submit():
            to_update_hospede = Guest.query.get_or_404(hospede_id)
            to_update_address = Addresses.query.get_or_404(hospede.address_id)
            to_update_hospede.hotel_id = form.hotel_id.data
            to_update_hospede.name = form.name.data
            to_update_hospede.email = form.email.data
            to_update_hospede.phone = form.phone.data
            to_update_hospede.cpf = form.cpf.data
            to_update_hospede.birthday = datetime.strptime(form.birthday.data, '%d/%m/%Y')
            to_update_address.endereco = form.endereco.data
            to_update_address.numero = form.numero.data
            to_update_address.complemento = form.complemento.data
            to_update_address.bairro = form.bairro.data
            to_update_address.cidade = form.cidade.data
            to_update_address.estado = form.estado.data
            to_update_address.pais = form.pais.data
            to_update_address.cep = form.cep.data
            db.session.commit()

            flash('Hóspede editado com sucesso!', 'success')
        return redirect(url_for('lista_hospedes_endpoint'))

    form.hotel_id.data = hospede.hotel_id
    form.name.data = hospede.name
    form.email.data = hospede.email
    form.phone.data = hospede.phone
    form.cpf.data = hospede.cpf
    form.birthday.data = hospede.birthday.strftime('%d/%m/%Y')
    form.endereco.data = address_data.street
    form.numero.data = address_data.number
    form.complemento.data = address_data.complement
    form.bairro.data = address_data.neighborhood
    form.cidade.data = address_data.city
    form.estado.data = address_data.state
    form.pais.data = address_data.country
    form.cep.data = address_data.zip_code

    return render_template('add_hospede.html',
                           form=form,
                           titulo='Editar hóspede'
                           )


def deletar_hospede(id, user_id):
    hospede = Guest.query.get_or_404(id)
    db.session.delete(hospede)
    db.session.commit()
    flash('Hóspede deletado com sucesso!', 'success')
    return redirect(url_for('lista_hospedes_endpoint'))
