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
    # assigned_tickets = db.relationship('Ticket')

class Priority(db.Model):
    __tablename__ = 'priority'
    id = db.Column(db.Integer, primary_key=True)
    priority_decoded = db.Column(db.String(30))

# Many to Many Ticket and Status
ticket_ticket_status = db.Table('ticket_ticket_status', 
        db.Column('ticket_id', db.Integer, db.ForeignKey('ticket.id')),
        db.Column('ticket_status_id', db.Integer, db.ForeignKey('ticket_status.id')))

class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    overview = db.Column(db.String(200))
    spec_requirements = db.Column(db.String(200))
    req_priority = db.Column(db.String(2), db.ForeignKey('priority.id'))

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id')) # user owns a ticket
    # owner = db.relationship('User', foreign_keys='Ticket.owner_id') #Dont need
    assigned_id = db.Column(db.Integer, db.ForeignKey('user.id')) # user assigned to ticket
    # assigned = db.relationship('User', foreign_keys='Ticket.assigned_id') #Dont need
    
class Ticket_Status(db.Model): 
    __tablename__ = 'ticket_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    ticket_ticket_status = db.relationship('Ticket', secondary=ticket_ticket_status, backref=db.backref('statuses', lazy=True))


# def add_status():
#     ticket_status_low = Ticket_Status(id=1, name='low')
#     ticket_status_medium = Ticket_Status(id=2, name='meidum')
#     ticket_status_high = Ticket_Status(id=3, name='high')
#     ticket_status_critial = Ticket_Status(id=4, name='critical')
#     db.session.add(ticket_status_low)
#     db.session.add(ticket_status_medium)
#     db.session.add(ticket_status_high)
#     db.session.add(ticket_status_critial)
#     db.session.commit()
# add_status()

# priority_low = Ticket_Status(id=1, name='low')
# priority_medium = Ticket_Status(id=2, name='meidum')
# priority_high = Ticket_Status(id=3, name='high')
# priority_critial = Ticket_Status(id=4, name='critical')
# db.session.add(priority_low)
# db.session.add(priority_medium)
# db.session.add(priority_high)
# db.session.add(priority_critial)
# db.session.commit()

# priorities = ['low','medium','high','critical']
# for i in priorities:
#     print(i)