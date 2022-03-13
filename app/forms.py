from flask_wtf import FlaskForm
from wtforms  import StringField, TextAreaField, DateTimeField, PasswordField
from wtforms.validators import InputRequired

class ExampleForm(FlaskForm):
	title = StringField(u'Título', validators = [InputRequired()])
	content = TextAreaField(u'Conteúdo')
	date = DateTimeField(u'Data', format='%d/%m/%Y %H:%M')
	#recaptcha = RecaptchaField(u'Recaptcha')

class LoginForm(FlaskForm):
	user = StringField(u'Usuário', validators = [InputRequired()])
	password = PasswordField(u'Senha', validators = [InputRequired()])
