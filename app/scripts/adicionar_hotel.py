from flask import render_template, request, redirect, url_for, flash
from app.forms import AdicionarHotel
from app.models import Hotels, Addresses
from app import db


def adicionar_hotel():
    form = AdicionarHotel()

    if request.method == 'POST':
        if form.validate_on_submit():
            hotel = Hotels.query.filter_by(name=form.name.data).first()
            if hotel is None:
                address = Addresses(street=form.endereco.data,
                                    neighborhood=form.bairro.data,
                                    city=form.cidade.data,
                                    state=form.estado.data,
                                    country=form.pais.data,
                                    zip_code=form.cep.data,
                                    complement=form.complemento.data)

                db.session.add(address)
                db.session.flush()

                hotel = Hotels(name=form.name.data,
                               phone=form.phone.data,
                               address_id=address.id)

                db.session.add(hotel)
                db.session.commit()

                flash('Hotel cadastrado com sucesso!')
            else:
                flash('Hotel já existe...')
        return redirect('/adicionar-hotel')

    return render_template('formulario_hotel.html',
                           form=form
                           )


def listar_hoteis():
    hoteis = Hotels.query.order_by(Hotels.created_at)
    return render_template('lista_hoteis_cadastrados.html',
                           hoteis=hoteis
                           )
