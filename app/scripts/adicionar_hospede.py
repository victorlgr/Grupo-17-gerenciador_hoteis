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

                flash('Hospede cadastrado com sucesso!', 'success')
            else:
                flash('Hospede já existe...', 'danger')
        return redirect(url_for('adicionar_hospede_endpoint'))

    return render_template('add_hospede.html',
                           form=form,
                           titulo='Adicionar Hospede', form_reserva=form_reserva,
                           user=user
                           )
