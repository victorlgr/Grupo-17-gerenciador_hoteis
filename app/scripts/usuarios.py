from flask import render_template, redirect, flash, request, url_for
from app import db
from app.models import Hotels, User
from app.forms import EditarUsuario, VerificarDisponibilidade


def listar_usuarios(user_id):
    form_reserva = VerificarDisponibilidade()
    user = User.query.filter_by(id=user_id).first()
    hoteis = Hotels.query.filter_by(id=user.hotel_id).order_by(Hotels.created_at)
    if user.hotel_id is None:
        hoteis = Hotels.query.filter_by(user_id=user_id).order_by(Hotels.created_at)
    if user_id not in [hotel.user_id for hotel in hoteis]\
            and user.hotel_id not in [hotel.id for hotel in hoteis] or user.profile not in ['admin']:
        return '<h1>Erro! Você não pode acessar este conteúdo!</h1>'
    ids_hoteis = [i.id for i in hoteis]
    hotel_choices = dict([(hotel.id, hotel.name) for hotel in hoteis])
    usuarios = User.query.filter(User.hotel_id.in_(ids_hoteis)).order_by(User.id)
    print(hotel_choices)

    return render_template('lista_usuarios.html',
                           usuarios=usuarios,
                           hotel_choices=hotel_choices,
                           zip=zip,
                           form_reserva=form_reserva
                           )


def deletar_usuario(id_usuario, user_id):
    user = User.query.get_or_404(id_usuario)
    user_deleting = User.query.get_or_404(user_id)
    hoteis = Hotels.query.filter_by(id=user.hotel_id).order_by(Hotels.created_at)
    if user_id not in [hotel.user_id for hotel in hoteis]\
            and user.hotel_id not in [hotel.id for hotel in hoteis] or user_deleting.profile not in ['admin']:
        return '<h1>Erro! Você não pode acessar este conteúdo!</h1>'
    db.session.delete(user)
    db.session.commit()
    flash('Usuário deletado com sucesso!', 'success')
    return redirect(url_for('lista_usuarios_endpoint'))


def editar_usuario(id_usuario, user_id):
    form = EditarUsuario()
    user = User.query.filter_by(id=id_usuario).first()

    hoteis = Hotels.query.order_by(Hotels.created_at)
    form.hotel_id.choices = [(hotel.id, hotel.name) for hotel in hoteis if hotel.user_id == user_id]

    """if user_id not in [hotel.user_id for hotel in hoteis]\
            and user.hotel_id not in [hotel.id for hotel in hoteis] or user.profile not in ['admin']:
        return '<h1>Erro! Você não pode acessar este conteúdo!</h1>'
"""
    if form.validate_on_submit():
        if request.method == 'POST':
            to_update = User.query.get_or_404(id_usuario)
            to_update.hotel_id = request.form['hotel_id']
            to_update.name = request.form['name']
            to_update.email = request.form['email']
            to_update.profile = request.form['profile']
            db.session.commit()
            flash('Usuário editado com sucesso!', 'success')
        return redirect(url_for('lista_usuarios_endpoint'))

    form.hotel_id.default = user.hotel_id
    form.process()
    form.name.data = user.name
    form.email.data = user.email
    form.profile.data = user.profile

    return render_template('editar_usuario.html',
                           form=form,
                           user=user,
                           titulo='Editar usuario'
                           )