from flask import render_template, redirect, flash, request
from app import db
from app.models import Hotels, User
from app.forms import EditarUsuario


def listar_usuarios(user_id):
    user = User.query.filter_by(id=user_id).first()
    hoteis = Hotels.query.filter_by(id=user.hotel_id).order_by(Hotels.created_at)
    if user.hotel_id is None:
        hoteis = Hotels.query.filter_by(user_id=user_id).order_by(Hotels.created_at)
    ids_hoteis = [i.id for i in hoteis]
    nomes_hoteis = [i.name for i in hoteis]
    usuarios = User.query.filter(User.hotel_id.in_(ids_hoteis)).order_by(User.id)

    return render_template('lista_usuarios.html',
                           usuarios=usuarios,
                           nomes_hoteis=nomes_hoteis,
                           zip=zip
                           )


def deletar_usuario(id_usuario):
    user = User.query.get_or_404(id_usuario)
    db.session.delete(user)
    db.session.commit()
    flash('Usuario deletado com sucesso!')
    return redirect('/lista-usuarios/')


def editar_usuario(id_usuario, user_id):
    form = EditarUsuario()
    user = User.query.filter_by(id=id_usuario).first()

    hoteis = Hotels.query.order_by(Hotels.created_at)
    form.hotel_id.choices = [(hotel.id, hotel.name) for hotel in hoteis if hotel.user_id == user_id]

    if form.validate_on_submit():
        if request.method == 'POST':
            to_update = User.query.get_or_404(id_usuario)
            to_update.hotel_id = request.form['hotel_id']
            to_update.name = request.form['name']
            to_update.email = request.form['email']
            to_update.profile = request.form['profile']
            db.session.commit()
        return redirect("/lista-usuarios")

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