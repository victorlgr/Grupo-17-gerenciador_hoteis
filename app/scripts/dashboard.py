# Quartos disponíveis
# Hóspedes ativos
# Pagamentos recebidos no mês
# Pagamentos esperados no mês
# Reservas canceladas no mês
# Receita de reservas canceladas no mês

from flask import render_template, request, redirect, url_for, flash
from datetime import datetime as dt
from app.models import Rooms, Hotels, User, Reservation, Status, Guest, Account
from app import db


def dashboard(hotel_id):
    hotel = Hotels.query.get_or_404(hotel_id)
    quartos = Rooms.query.filter_by(hotel_id=hotel_id).order_by(Rooms.id)
    hospedes = Guest.query.filter_by(hotel_id=hotel_id).order_by(Guest.name)
    reservas = Reservation.query.order_by(Reservation.id)
    contas = Account.query.filter_by(hotel_id=hotel_id).order_by(Account.id)
    hoje = dt.strptime(dt.today().strftime('%Y-%m-%d'), '%Y-%m-%d')
    status_reservas = [(r.room_id, (r.check_in <= hoje <= r.check_out)) for r in reservas if r.status == Status.ATIVO]
    # status_reservas = [status for status in status_reservas if status[1] is True]
    contador_quartos = 0
    contador_hospedes = 0
    contas_receber_mes = 0
    contas_pagar_mes = 0
    for i in status_reservas:
        if i[1]:
            contador_quartos += 1
    for r in reservas:
        if r.status == Status.ATIVO and (r.check_in <= hoje <= r.check_out):
            contador_hospedes += r.total_guests
    for c in contas:
        print(c.data_pgto)
        if c.tipo == 'Contas a receber' and c.data_pgto is not None:
            if c.data_pgto.month == dt.today().month:
                contas_receber_mes += c.valor
        elif c.tipo == 'Contas a pagar' and c.data_pgto is not None:
            if c.data_pgto.month == dt.today().month:
                contas_pagar_mes += c.valor
    status_reservas = dict(set(status_reservas))
    return render_template('dashboard.html',
                           status_reservas=status_reservas,
                           contador_quartos=contador_quartos,
                           contador_hospedes=contador_hospedes,
                           contas_receber_mes=contas_receber_mes,
                           contas_pagar_mes=contas_pagar_mes,
                           len=len
                           )
