from flask import render_template, request, redirect, url_for, flash
from app.forms import AdicionarHotel
from app.models import Hotels, Addresses, User
from app import db


def adicionar_hotel(user_id):
    form = AdicionarHotel()

    if request.method == 'POST':
        if form.validate_on_submit():
            hotel = Hotels.query.filter_by(cnpj=form.cnpj.data).first()
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

    return render_template('formulario_hotel.html',
                           form=form,
                           titulo='Adicionar hotel'
                           )


def listar_hoteis(user_id):
    user = User.query.filter_by(id=user_id).first()
    hoteis = Hotels.query.filter_by(id=user.hotel_id).order_by(Hotels.created_at)
    if user.hotel_id is None:
        hoteis = Hotels.query.filter_by(user_id=user_id).order_by(Hotels.created_at)
    return render_template('lista_hoteis_cadastrados.html',
                           hoteis=hoteis
                           )


def deletar_hotel(id, user_id):
    hotel = Hotels.query.get_or_404(id)
    if hotel.user_id != user_id:
        return '<h1>Erro! Você não pode acessar este conteúdo!</h1>'
    db.session.delete(hotel)
    db.session.commit()
    flash('Hotel deletado com sucesso!')
    return redirect('/lista-hotel')


def editar_hotel(hotel, user_id):
    user = User.query.filter_by(id=user_id).first()
    hotel_data = Hotels.query.filter_by(id=hotel).first()
    address_data = Addresses.query.filter_by(id=hotel_data.address_id).first()

    if hotel_data.user_id != user_id and user.hotel_id != user_id:
        return '<h1>Erro! Você não pode acessar este conteúdo!</h1>'

    form = AdicionarHotel()

    if form.validate_on_submit():
        if request.method == 'POST':
            to_update_hotel = Hotels.query.get_or_404(hotel)
            to_update_address = Addresses.query.get_or_404(hotel)
            to_update_hotel.name = form.name.data
            to_update_hotel.phone = form.phone.data
            to_update_hotel.email = form.email.data
            to_update_hotel.cnpj = form.cnpj.data
            to_update_address.street = form.endereco.data
            to_update_address.neighborhood = form.bairro.data
            to_update_address.city = form.cidade.data
            to_update_address.state = form.estado.data
            to_update_address.country = form.pais.data
            to_update_address.zip_code = form.cep.data
            to_update_address.number = form.numero.data
            to_update_address.complement = form.complemento.data
            db.session.commit()
        return redirect('/lista-hotel')

    form.name.data = hotel_data.name
    form.phone.data = hotel_data.phone
    form.email.data = hotel_data.email
    form.cnpj.data = hotel_data.cnpj
    form.endereco.data = address_data.street
    form.bairro.data = address_data.neighborhood
    form.cidade.data = address_data.city
    form.estado.data = address_data.state
    form.pais.data = address_data.country
    form.cep.data = address_data.zip_code
    form.numero.data = address_data.number
    form.complemento.data = address_data.complement

    return render_template('formulario_hotel.html',
                           form=form,
                           titulo='Editar hotel'
                           )
