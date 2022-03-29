from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, DataRequired, EqualTo


class CreateUserForm(FlaskForm):
	name = StringField(u'Nome', validators = [InputRequired()])
	email = StringField(u'E-mail', validators = [InputRequired()])
	password = PasswordField(u'Senha', validators = [InputRequired()])
	password_confirmation = PasswordField(u'Confirmação de Senha', validators = [InputRequired(), DataRequired(), EqualTo('password')])
	hotel_id = SelectField('Hotel', validators=[DataRequired()])
	# date = DateTimeField(u'Data', format='%d/%m/%Y %H:%M')
	#recaptcha = RecaptchaField(u'Recaptcha')


class LoginForm(FlaskForm):
	email = StringField(u'Email', validators = [InputRequired()])
	password = PasswordField(u'Senha', validators = [InputRequired()])


class AdicionarHotel(FlaskForm):
	name = StringField('Nome', validators=[DataRequired()])
	phone = StringField('Telefone', validators=[DataRequired()])
	email = StringField('E-mail', validators=[DataRequired()])
	cnpj = StringField('CNPJ', validators=[DataRequired()])
	endereco = StringField('Endereço', validators=[DataRequired()])
	numero = StringField('Número', validators=[DataRequired()])
	complemento = StringField('Complemento', validators=[DataRequired()])
	bairro = StringField('Bairro', validators=[DataRequired()])
	cidade = StringField('Cidade', validators=[DataRequired()])
	estado = StringField('Estado', validators=[DataRequired()])
	pais = StringField('Pais', validators=[DataRequired()])
	cep = StringField('CEP', validators=[DataRequired()])

	submeter = SubmitField('Submeter')


class AdicionarQuarto(FlaskForm):
	hotel_id = SelectField('Hotel', validators=[DataRequired()])
	number = StringField('Número', validators=[DataRequired()])
	kind = StringField('Tipo', validators=[DataRequired()])
	phone_extension = StringField('Extensão telefone', validators=[DataRequired()])
	price = StringField('Preço', validators=[DataRequired()])
	guest_limit = StringField('Número de hóspedes', validators=[DataRequired()])
	status = StringField('Status', validators=[DataRequired()])

	submeter = SubmitField('Submeter')
