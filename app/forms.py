from flask_wtf import FlaskForm
from wtforms  import StringField, TextAreaField, DateTimeField, PasswordField
from wtforms.validators import InputRequired

class CreateUserForm(FlaskForm):
	name = StringField(u'Nome', validators = [InputRequired()])
	email = StringField(u'E-mail', validators = [InputRequired()])
	password = PasswordField(u'Senha', validators = [InputRequired()])
	password_confirmation = PasswordField(u'Confirmação de Senha', validators = [InputRequired()])
	# date = DateTimeField(u'Data', format='%d/%m/%Y %H:%M')
	#recaptcha = RecaptchaField(u'Recaptcha')

class LoginForm(FlaskForm):
	email = StringField(u'Email', validators = [InputRequired()])
	password = PasswordField(u'Senha', validators = [InputRequired()])
