# from turtle import title

from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from BusPay2000 import app, bcrypt, db, qrcode
from BusPay2000.models import User, Ticket, users_tickets
from BusPay2000.forms import RegistrationForm, LoginForm, BuyForm, TravelcardForm



@app.route('/', methods=['GET'])
def main_page():
    title = 'BusPay2000 - Главная страница'
    if current_user.is_authenticated:
        tickets = current_user.tickets
        return render_template('main.html', title=title, tickets=tickets)
    return render_template('main.html', title=title)




@app.route('/account', methods=['GET'])
def account_page():
    title = 'BusPay2000 - Личный кабинет'
    if current_user.is_authenticated:
        travels = current_user.travels
        return render_template('account.html', title=title, travels=travels)
    return redirect(url_for('main_page'))


@app.route('/schedule', methods=['GET'])
def schedule_page():
    title = 'BusPay2000 - Расписание'
    if current_user.is_authenticated:
        return render_template('schedule.html', title=title)
    return redirect(url_for('main_page'))

@app.route('/buy', methods=['GET', 'POST'])
def buy_page():
    title = 'BusPay2000 - Купить'
    if current_user.is_authenticated:
        form = BuyForm()
        if form.validate_on_submit():
            ticket =  Ticket()
            db.session.add(ticket)
            current_user.tickets.append(ticket)
            db.session.commit()
            flash('Билет куплен', 'success')
            return redirect(url_for('main_page'))
        return render_template('buy.html', title=title, messages=True, form=form)
    return redirect(url_for('main_page'))

@app.route('/travelcard', methods=['GET', 'POST'])
def travelcard_page():
    title = 'BusPay2000 - Купить проездной'
    if current_user.is_authenticated:
        form = TravelcardForm()

        if form.validate_on_submit():
            print(form.travelcard_uses.data)
            ticket = Ticket(uses=form.travelcard_uses.data)
            db.session.add(ticket)
            current_user.tickets.append(ticket)
            db.session.commit()
            flash(f'Куплен проездной на {ticket.uses} поездок', 'success')
            return redirect(url_for('main_page'))
        return render_template('travelcard.html', title=title, form=form, travelcard_uses=form.travelcard_uses)
    return redirect(url_for('main_page'))


# @app.route('/history', methods=['GET'])
# def history_page():
#     title = 'BusPay2000 - История поездок'
#     tickets = current_user.tickets
#     print(tickets)
#     return render_template('history.html', title=title, tickets=tickets)


@app.route('/contacts', methods=['GET'])
def contacts_page():
    title = 'BusPay2000 - Контакты'
    if current_user.is_authenticated:
        return render_template('contacts.html', title=title)
    return redirect(url_for('main_page'))


@app.route('/registration', methods=['GET', 'POST'])
def reg_page():
    title = 'BusPay2000 - Регистрация'
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phone=form.phone.data).first()
        if user:
            flash('Пользователь существует', 'danger')
        else:
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
    if current_user.is_authenticated:
        flash('Вы успешно вышли из учётной записи', 'info')
        logout_user()
        return redirect(url_for('main_page'))
    return redirect(url_for('main_page'))


@app.route('/flush', methods=['GET'])
def reset_db():
    flash('Database has been resetted', 'info')
    logout_user()
    db.drop_all()
    db.create_all()
    return redirect(url_for('main_page'))


@app.route("/approve_ticket/<int:ticket>", methods=['GET', 'POST'])
def approve(ticket):
    if current_user.is_authenticated:
        if current_user.is_conductor == True:
            t = Ticket.query.filter_by(id=ticket).first_or_404()
            u = User.query.filter_by(id=db.session.query(users_tickets).filter_by(ticket_id=1).first()[0]).first_or_404()
            if t.uses > 0:
                t.uses -=  1
                u.travels += 1
                db.session.commit()
                flash('Билет успшено оплачен', 'info')
                return redirect(url_for('main_page'))
            elif t.uses == 0:
                flash('Билет уже использован', 'danger')
                return redirect(url_for('main_page'))
            else:
                return redirect(url_for('main_page'))
        else:
            flash('Нет прав для просмотра страницы >:V','danger')
            return redirect(url_for('main_page'))
    return redirect(url_for('main_page'))
    

@app.errorhandler(404)
def not_found(e):
    title = "BusPay2000 - 404 страница не найдена"
    return render_template('404.html', title=title)
