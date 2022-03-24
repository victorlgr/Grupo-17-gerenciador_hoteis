from flask import url_for, redirect, render_template, flash, g, session
from flask_login import login_user, logout_user, current_user, login_required
from app import app, login_manager
from app.forms import CreateUserForm, LoginForm
from app.models import User
from app import db, bcrypt
from app.scripts.adicionar_hotel import adicionar_hotel, listar_hoteis, editar_hotel
from app.scripts.ocupacao_quartos import adicionar_quarto, ocupacao_quartos, editar_quarto


@app.route('/')
def pagina_inicial():
    return render_template('index.html')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# @app.route('/list/')
# def posts():
# 	return render_template('list.html')


@app.route('/new/')
@login_required
def new():
	form = CreateUserForm()
	return render_template('new.html', form=form)


@app.route('/save/', methods = ['GET','POST'])
@login_required
def save():
    form = CreateUserForm()
    if form.validate_on_submit():
         name = form.name.data
         email = form.email.data
         pwd = bcrypt.generate_password_hash(form.password.data)
         admin = User(name=name, password=pwd, profile='admin', email=email, password_confirmation=pwd)
         db.session.add(admin)
         db.session.commit()
    return render_template('new.html', form=form)


# @app.route('/view/<id>/')
# def view(id):
# 	return render_template('view.html')

# # === User login methods ===

@app.before_request
def before_request():
    g.user = current_user

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('new'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for("new"))

    return render_template('login.html', 
        title = 'Sign In',
        form = form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/adicionar-hotel/', methods=['GET', 'POST'])
def adicionar_hotel_endpoint():
    return adicionar_hotel()


@app.route('/lista-hotel/')
def lista_hotel():
    return listar_hoteis()


@app.route('/editar-hotel/<int:id>', methods=['GET', 'POST'])
def editar_hotel_endpoint(id):
    return editar_hotel(id)


@app.route('/adicionar-quarto/', methods=['GET', 'POST'])
def adicionar_quarto_endpoint():
    return adicionar_quarto()


@app.route('/ocupacao-quartos/<int:id>')
def ocupacao_quartos_endpoint(id):
    return ocupacao_quartos(id)


@app.route('/editar-quarto/<int:id>', methods=['GET', 'POST'])
def editar_quarto_endpoint(id):
    return editar_quarto(id)
