from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Ticket, Ticket_Status, Priority, ticket_ticket_status
from sqlalchemy import text

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
    # If 'POST' request
    if request.method == 'POST':
        ticket_name = request.form.get('ticket_name')
        ticket_desc = request.form.get('ticket_desc')
        spec_requirements = request.form.get('spec_requirements')
        requested_priority = request.form.get('req_priority')

        status = Ticket_Status.query.filter_by(id='1').first()
        
        new_ticket = Ticket(title=ticket_name, overview=ticket_desc, spec_requirements=spec_requirements, requested_priority=requested_priority, owner_id=current_user.id )

        new_ticket.ticket_statuses.append(status)

        

        db.session.add(new_ticket)
        db.session.commit()
        flash('Request submitted!', category='success')

        # return str(new_ticket.title) + ' ' + str(new_ticket.overview) + ' ' + str(new_ticket.spec_requirements) + ' ' + str(new_ticket.req_priority) + ' ' + str(new_ticket.owner_id) + ' ' + str(user_id) + ' ' + str(status.id)
        # return str(status)
        return redirect(url_for('views.dashboard'))

    # If 'GET' request
    return render_template('new_ticket.html')


@views.route('/tickets', methods=['GET','POST'])
@login_required
def tickets():
    

    tickets = Ticket.query.all()

    
    return render_template('tickets.html', tickets=tickets)
    

    
    # GETS TICKET STATUSES
    # tickets = Ticket.query.join(Ticket_Status, Ticket.ticket_statuses).first()
    # return str(tickets.id) + ' ' + str(tickets.title) + ' ' + str(tickets.ticket_status.first().name) + ' ' + str(tickets.title)

    # GIVES PRIORITY
    # tickets = Ticket.query.join(Priority, Ticket.req_priority==Priority.id).first()
    # return str(tickets.id) + ' ' + str(tickets.req_priority) + ' ' + str(tickets.priority.priority_decoded)
 

@views.route('/ticket-<ticket_id>', methods=['GET','POST'])
@login_required
def ticket_number(ticket_id):


    ticket = Ticket.query.filter_by(id=ticket_id).first()
    
    if not ticket:
        return redirect(url_for('views.tickets'))

    status_dict = {ticket.ticket_statuses.all()[i].id:ticket.ticket_statuses.all()[i].name for i in range(len(ticket.ticket_statuses.all()))}
    
    statuses = db.session.query(ticket_ticket_status).filter(text('ticket_id='+str(ticket_id))).order_by(ticket_ticket_status.c.time_stamp).all()

    ticket_status = []
    for i in range(len(statuses)):
        ticket_status.append([   status_dict[statuses[i][1]]       , statuses[i][2]])
    
    return render_template('single_ticket_info.html', ticket=ticket, ticket_status=ticket_status[::-1], count_status=len(statuses))
    




@views.route('/update_ticket', methods=['POST'])
@login_required
def update_ticket():
    if request.method == 'POST':
        ticket_id = request.form.get('ticket_id')
        # ticket_name = request.form.get('ticket_name')
        # ticket_desc = request.form.get('ticket_desc')
        # spec_requirements = request.form.get('spec_requirements')
        updated_status = request.form.get('update_status')

        return str(ticket_id) + ' ' + str(updated_status)

        