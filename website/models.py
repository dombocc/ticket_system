from flask_login import UserMixin 
from . import db
from sqlalchemy.sql import func

# User Table
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))

# Many to Many Ticket and Status
ticket_ticket_status = db.Table('ticket_ticket_status', 
        db.Column('ticket_id', db.Integer, db.ForeignKey('ticket.id')),
        db.Column('ticket_status_id', db.Integer, db.ForeignKey('ticket_status.id')))

class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id')) # user owns a ticket
    
class Ticket_Status(db.Model): 
    __tablename__ = 'ticket_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    ticket_ticket_status = db.relationship('Ticket', secondary=ticket_ticket_status, backref=db.backref('statuses', lazy=True))

