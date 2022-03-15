from flask import render_template, request, redirect, url_for, flash
from app.forms import AdicionarHotel


def adicionar_hotel():
    form = AdicionarHotel()

    if request.method == 'POST':
        return redirect('/adicionar-hotel')

    if form.validate_on_submit():
        flash('Hotel cadastrado com sucesso!')

    return render_template('formulario_hotel.html',
                           form=form
                           )
