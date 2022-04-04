from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from BusPay2000.models import User
from BusPay2000 import db


class RegistrationForm(FlaskForm):
    phone = IntegerField('Номер телефона', validators=[
                           DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтверждение пароля', validators=[
                                     DataRequired(), EqualTo('password')])
    usr_type = BooleanField('Кондуктор?')
    submit = SubmitField('Регистрация')

    def validate_username(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('Имя пользователя уже занято')


class LoginForm(FlaskForm):
    phone = IntegerField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Оставаться в системе')
    submit = SubmitField('Вход')
