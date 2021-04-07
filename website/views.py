from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Ticket, Ticket_Status, Priority, ticket_ticket_status

views = Blueprint('views', __name__)

@views.route('/')
def front_page():
    if current_user.get_id():
        return redirect(url_for('views.dashboard'))
    return render_template('front_page.html')

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# @views.route('/new_ticket')
# @login_required
# def new_ticket():
#     return render_template('new_ticket.html')


@views.route('/new_ticket', methods=['GET', 'POST'])
@login_required
def new_ticket():
    if request.method == 'POST':
        ticket_name = request.form.get('ticket_name')
        ticket_desc = request.form.get('ticket_desc')
        spec_requirements = request.form.get('spec_requirements')
        req_priority = request.form.get('req_priority')

        status = Ticket_Status.query.filter_by(id='1').first()
        
        new_ticket = Ticket(title=ticket_name, overview=ticket_desc, spec_requirements=spec_requirements, req_priority=req_priority, owner_id=current_user.id )

        new_ticket.ticket_statuses.append(status)

        

        db.session.add(new_ticket)
        db.session.commit()
        flash('Request submitted!', category='success')

        # return str(new_ticket.title) + ' ' + str(new_ticket.overview) + ' ' + str(new_ticket.spec_requirements) + ' ' + str(new_ticket.req_priority) + ' ' + str(new_ticket.owner_id) + ' ' + str(user_id) + ' ' + str(status.id)
        # return str(status)
        return redirect(url_for('views.dashboard'))

    # If get
    return render_template('new_ticket.html')


@views.route('/tickets', methods=['GET','POST'])
@login_required
def tickets():
    
    # tickets = Ticket.query.select_from(Ticket).join(ticket_ticket_status).join(Ticket_Status).first()
    
    # tickets = Ticket.query.select_from(Ticket).join(Priority, Ticket.req_priority == Priority.id).first()
    # tickets = db.session.query(Ticket,Priority).filter_by(Ticket.req_priority == Priority.id).first()

    tickets = Ticket.query.join(Ticket_Status, Ticket.ticket_statuses).first()
    # tickets = Ticket.query.join(ticket_ticket_status, Ticket.id == ticket_ticket_status.c.ticket_id).join(Ticket_Status, ticket_ticket_status.c.ticket_status_id == Ticket_Status.id).first()

    
    # return render_template('tickets.html')
    # return str(tickets.id) + ' ' + str(tickets.title) + ' ' + str(tickets.created_date) + ' ' + str(tickets.overview) + ' ' + str(tickets.spec_requirements) + ' '  + str(tickets.req_priority) + ' ' + str(tickets.ticket_statuses.all()) 
    # + ' ' + str(tickets.owner_id) 

    # GETS TICKET STATUSES
    tickets = Ticket.query.join(Ticket_Status, Ticket.ticket_statuses).first()
    return str(tickets.id) + ' ' + str(tickets.title) + ' ' + str(tickets.ticket_statuses.first().name) + ' ' + str(tickets.title)

    # GIVES PRIORITY
    # tickets = Ticket.query.join(Priority, Ticket.req_priority==Priority.id).first()
    # return str(tickets.id) + ' ' + str(tickets.req_priority) + ' ' + str(tickets.priority.priority_decoded)
 

