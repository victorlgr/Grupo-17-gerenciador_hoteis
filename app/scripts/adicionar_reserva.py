from tabnanny import check
from flask import render_template, request, redirect, url_for, flash
from app.forms import AdicionarReserva, VerificarDisponibilidade
from app.models import Hotels, Status, User, Reservation, Rooms, Guest
from datetime import datetime
from app import db


def adicionar_reserva(user_id):
    form_reserva = VerificarDisponibilidade()
    form = AdicionarReserva()
    user = User.query.filter_by(id=user_id).first()
    hotel = Hotels.query.filter_by(id=user.hotel_id).first()
    rooms = Rooms.query.filter_by(hotel_id=hotel.id).order_by(Rooms.number)
    guests = Guest.query.filter_by(hotel_id=hotel.id).order_by(Guest.name)

    form.room_id.choices = [(room.id, room.number) for room in rooms]
    form.guest_id.choices = [(guest.id, guest.name) for guest in guests]

    if request.method == 'POST':
      if form.validate_on_submit():
          reservation = Reservation.query.filter((Reservation.room_id == form.room_id.data) & (Reservation.check_in.between(form.check_in.data,  form.check_out.data) | Reservation.check_out.between(form.check_in.data,  form.check_out.data)), Reservation.status == Status.ATIVO).all()
          if not reservation:

            total_guests = form.total_guests.data
            room_id = form.room_id.data
            room = Rooms.query.filter_by(id=room_id).first()

            if total_guests > room.guest_limit:
              flash('Esse quarto não tem capacidade para esse número de hóspedes', 'danger')
            else:
              r = Reservation(total_guests=form.total_guests.data,
                              payment_type=form.payment_type.data,
                              check_in=form.check_in.data,
                              check_out=form.check_out.data,
                              room_id=form.room_id.data,
                              guest_id=form.guest_id.data,
                              user_id=user_id)
                              
              db.session.add(r)
              db.session.commit()

              flash('Reserva cadastrada com sucesso!', 'success')
          else:
              flash('Esse quarto já possui uma reserva para essa data.', 'danger')

    if request.method == 'GET':
      form.room_id.data = request.args.get('quarto_id') if 'quarto_id' in request.args else ''
      form.check_in.data = datetime.strptime(request.args.get('check_in'), "%Y-%m-%d") if 'check_in' in request.args else ''
      form.check_out.data = datetime.strptime(request.args.get('check_out'), "%Y-%m-%d") if 'check_out' in request.args else ''
      form.total_guests.data = request.args.get('total_guests') if 'total_guests' in request.args else ''
    
    return render_template('add_reserva.html',
                           form=form,
                           titulo='Adicionar Reserva', form_reserva=form_reserva
                           )

def listar_reservas(user_id):
  form_reserva = VerificarDisponibilidade()
  user = User.query.filter_by(id=user_id).first()
  hotel = Hotels.query.filter_by(id=user.hotel_id).first()

  if user.profile not in ['admin', 'gerente', 'recepcionista']:
    return '<h1>Erro! Você não pode acessar este conteúdo!</h1>'

  reservas = db.session.query(Reservation, Guest, Rooms)\
    .join(Guest)\
    .join(Rooms)\
    .filter(Rooms.hotel_id == hotel.id, Reservation.status == Status.ATIVO)\
    .order_by(Reservation.check_in).all()

  return render_template('lista_reservas.html', reservas=reservas, form_reserva=form_reserva)

def quartos_disponiveis(user_id):
  form_reserva = VerificarDisponibilidade()
  user = User.query.filter_by(id=user_id).first()

  if user.profile not in ['admin', 'gerente', 'recepcionista']:
    return '<h1>Erro! Você não pode acessar este conteúdo!</h1>'

  return render_template('lista_reservas.html', quartos=[], form_reserva=form_reserva)

def verificar_disponibilidade(user_id):
  form_reserva = VerificarDisponibilidade()
  user = User.query.filter_by(id=user_id).first()

  if user.profile not in ['admin', 'gerente', 'recepcionista']:
    return '<h1>Erro! Você não pode acessar este conteúdo!</h1>'

  if request.method == 'POST':
      if form_reserva.validate_on_submit():

        check_in = form_reserva.check_in.data
        check_out = form_reserva.check_out.data
        total_guests = form_reserva.total_guests.data

        rooms_ids = db.session.query(Reservation.room_id).join(Rooms).filter(Rooms.hotel_id == user.hotel_id, (Reservation.check_in.between(check_in, check_out) | Reservation.check_out.between(check_in, check_out)), Reservation.status == Status.ATIVO)
        rooms = Rooms.query.filter(Rooms.hotel_id == user.hotel_id, Rooms.guest_limit >= total_guests, Rooms.id.not_in(rooms_ids))
        
        if rooms.count() == 0:
          flash('Não foi possível encontrar nenhum quarto para a data escolhida.', 'warning')

        return render_template('quartos_disponiveis.html', quartos=rooms, form_reserva=form_reserva)

  return redirect('/lista-reservas')

##TODO Faz sentido alterar reserva? talvez deva sempre cancelar e criar uma nova
def alterar_reserva(id, user_id):
  form_reserva = VerificarDisponibilidade()
  user = User.query.filter_by(id=user_id).first()

  form = AdicionarReserva()
  hotel = Hotels.query.filter_by(id=user.hotel_id).first()
  rooms = Rooms.query.filter_by(hotel_id=hotel.id).order_by(Rooms.number)
  guests = Guest.query.filter_by(hotel_id=hotel.id).order_by(Guest.name)

  form.room_id.choices = [(room.id, room.number) for room in rooms]
  form.guest_id.choices = [(guest.id, guest.name) for guest in guests]

  if user.profile not in ['admin', 'gerente', 'recepcionista']:
    return '<h1>Erro! Você não pode acessar este conteúdo!</h1>'

  if request.method == 'POST':
      if form.validate_on_submit():
        reservation = Reservation.query.filter_by(id=id)
        reservation.total_guests = request.form['total_guests']
        reservation.check_in = request.form['check_in']
        reservation.check_out = request.form['check_out']
        reservation.payment_type = request.form['payment_type']
        reservation.status = request.form['status']
        db.session.commit()
        return redirect(f"/ocupacao-quartos/{request.form['hotel_id']}")

  return redirect('/lista-reservas')

def cancelar_reserva(reservation_id, user_id):
  form_reserva = VerificarDisponibilidade()
  user = User.query.filter_by(id=user_id).first()
  
  if user.profile not in ['admin', 'gerente', 'recepcionista']:
    return '<h1>Erro! Você não pode acessar este conteúdo!</h1>'

  reservation = Reservation.query.join(Rooms).filter(Rooms.hotel_id == user.hotel_id, Reservation.id==reservation_id).first()

  if reservation is not None:
    reservation.status = Status.CANCELADO
    db.session.commit()

  return redirect('/lista-reservas')