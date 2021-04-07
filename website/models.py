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
    owned_tickets = db.relationship('Ticket', backref=db.backref('owner', lazy=True), foreign_keys='Ticket.owner_id')
    assigned_tickets = db.relationship('Ticket', backref=db.backref('assigned', lazy=True), foreign_keys='Ticket.assigned_id')
    

class Priority(db.Model):
    __tablename__ = 'priority'
    id = db.Column(db.Integer, primary_key=True)
    priority_decoded = db.Column(db.String(30))
    ticket_id = db.relationship('Ticket', backref='priority', lazy=True)


# Many to Many Ticket and Status
ticket_ticket_status = db.Table('ticket_ticket_status', 
        db.Column('ticket_id', db.Integer, db.ForeignKey('ticket.id')),
        db.Column('ticket_status_id', db.Integer, db.ForeignKey('ticket_status.id')),
        db.Column('time_stamp', db.DateTime(timezone=True), default=func.now()),
        db.PrimaryKeyConstraint('ticket_id','ticket_status_id'))

class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    overview = db.Column(db.String(200))
    spec_requirements = db.Column(db.String(200))

    req_priority = db.Column(db.Integer, db.ForeignKey('priority.id'))

    ticket_statuses = db.relationship('Ticket_Status', secondary='ticket_ticket_status', lazy='dynamic', backref=db.backref('tickets', lazy='dynamic'))

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id')) # user owns a ticket
    # owner = db.relationship('User', foreign_keys='Ticket.owner_id') #Dont need
    assigned_id = db.Column(db.Integer, db.ForeignKey('user.id')) # user assigned to ticket
    # assigned = db.relationship('User', foreign_keys='Ticket.assigned_id') #Dont need
    
class Ticket_Status(db.Model): 
    __tablename__ = 'ticket_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    ticket_ticket_status = db.relationship('Ticket', secondary='ticket_ticket_status', backref=db.backref('ticket_status', lazy='dynamic'))

