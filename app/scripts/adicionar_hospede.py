from flask import render_template, request, redirect, url_for, flash
from app.forms import AdicionarHospede, VerificarDisponibilidade
from app.models import Hotels, Addresses, Guest
from datetime import datetime
from app import db


def adicionar_hospede(user_id):
    form_reserva = VerificarDisponibilidade()
    form = AdicionarHospede()
    hotel = Hotels.query.order_by(Hotels.created_at).first() #TODO need refact to use the right hotel

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
                                hotel_id=hotel.id,
                                address_id=address.id)

                db.session.add(guest)
                db.session.commit()

                flash('Hospede cadastrado com sucesso!')
            else:
                flash('Hospede já existe...')
        flash('Validação falhou!')        
        return render_template('add_hospede.html', form=form, titulo='Adicionar Hospede', form_reserva=form_reserva)

    return render_template('add_hospede.html',
                           form=form,
                           titulo='Adicionar Hospede', form_reserva=form_reserva
                           )