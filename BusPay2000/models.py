from datetime import datetime
from flask_login import UserMixin
from BusPay2000 import db
from BusPay2000 import login_manager



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


users_tickets = db.Table('users_tickets',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True ),
    db.Column('ticket_id', db.Integer, db.ForeignKey('ticket.id'), primary_key=True)
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_conductor = db.Column(db.Boolean, default=False)

    tickets = db.relationship('Ticket', secondary=users_tickets, lazy='subquery',
                           backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f"User '{self.username}', Phone number '{self.phone}'"
   


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    used = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Date '{self.date}', Is used? '{self.used}'"
