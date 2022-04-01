# from turtle import title
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from BusPay2000 import app, bcrypt, db
from BusPay2000.models import User
from BusPay2000.forms import RegistrationForm, LoginForm



@app.route('/', methods=['GET'])
def main_page():
    title = 'BusPay2000 - Главная страница'
    return render_template('main.html', title=title)


@app.route('/account', methods=['GET'])
def account_page():
    title = 'BusPay2000 - Личный кабинет'
    return render_template('account.html', title=title)


@app.route('/schedule', methods=['GET'])
def schedule_page():
    title = 'BusPay2000 - Расписание'
    return render_template('schedule.html', title=title)


@app.route('/buy', methods=['GET'])
def buy_page():
    title = 'BusPay2000 - Купить'
    return render_template('buy.html', title=title)


@app.route('/registration', methods=['GET', 'POST'])
def reg_page():
    title = 'BusPay2000 - Регистрация'
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(phone=form.phone.data, password=hashed_password,
                    is_conductor=form.usr_type.data)
        db.session.add(user)
        db.session.commit()
        flash('Аккаунт создан', 'success')
        return redirect(url_for('login_page'))
    return render_template('registration.html', title=title, messages=True, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    title = 'BusPay2000 - Вход'
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phone=form.phone.data).first()
        if not user:
            flash('Пользователь несуществует', 'danger')
        else:
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main_page'))
            else:
                flash('Неправильный логин или пароль', 'danger')
    return render_template('login.html', title=title, messages=True, form=form)


@app.route('/logout')
def logout_page():
    flash('Вы успешно вышли из учётной записи', 'info')
    logout_user()
    return redirect(url_for('main_page'))


@app.route('/flush', methods=['GET'])
def reset_db():
    flash('Database has been resetted', 'info')
    logout_user()
    db.drop_all()
    db.create_all()
    return redirect(url_for('main_page'))
