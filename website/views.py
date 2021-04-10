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
        special_requirements = request.form.get('special_requirements')
        requested_priority = request.form.get('req_priority')

        status = Ticket_Status.query.filter_by(id='1').first()
        
        new_ticket = Ticket(title=ticket_name, overview=ticket_desc, special_requirements=special_requirements, requested_priority=requested_priority, owner_id=current_user.id )

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

    # Status dictonary to get status names
    status_dict = {ticket.ticket_statuses.all()[i].id:ticket.ticket_statuses.all()[i].name for i in range(len(ticket.ticket_statuses.all()))}
    
    # Statuses for the ticket
    statuses = db.session.query(ticket_ticket_status).filter(text('ticket_id='+str(ticket_id))).order_by(ticket_ticket_status.c.time_stamp).all()

    current_ticket_status = statuses[-1][1]
    

    # Get status list in order from oldest to newest
    ticket_status = []
    for i in range(len(statuses)):
        ticket_status.append([  status_dict[statuses[i][1]]  , statuses[i][2]])
    
    # Get List of developers
    developers = User.query.filter_by(user_type=1).order_by(User.id).all()

    #Get List of statuses for updates
    ticket_statuses = Ticket_Status.query.order_by(Ticket_Status.id).all()

    priorities = Priority.query.all()
    
    
    return render_template('single_ticket_info.html', ticket=ticket, ticket_status=ticket_status[::-1], count_status=len(statuses), 
                developers=developers, developer_length = len(developers), ticket_statuses=ticket_statuses, current_ticket_status=current_ticket_status,
                priorities = priorities)
    




@views.route('/update_ticket', methods=['POST'])
@login_required
def update_ticket():
    if request.method == 'POST':
        ticket_id = int(request.form.get('ticket_id'))
        ticket_title = request.form.get('ticket_title')
        ticket_overview = request.form.get('ticket_overview')
        special_requirements = request.form.get('special_requirements')
        assigned_user_id = int(request.form.get('assigned_user'))
        updated_status = int(request.form.get('update_status'))
        assigned_priority = int(request.form.get('assigned_priority'))

        # Get current ticket entitiy
        ticket = Ticket.query.filter_by(id=ticket_id).first()

        # update ticket title
        if ticket.title != ticket_title:
            ticket.title = ticket_title
            return 'title ' + str(ticket_title)
        
        # update ticket overview
        if ticket.overview != ticket_overview:
            ticket.overview = ticket_overview
            return 'overview ' + str(ticket_overview)
        
        # update ticket special_requirements
        if ticket.special_requirements != special_requirements:
            ticket.special_requirements = special_requirements
            return 'spec_req ' + str(special_requirements)
        
        # update ticket assigned_user
        if ticket.assigned_user.id != assigned_user_id:
            ticket.assigned_user.id = assigned_user_id
            return 'assigned ' + str(assigned_user_id)+ str(ticket.assigned_user.id)

        # assign a priority
        ###########
        
        
        # update ticket status
        if ticket.ticket_statuses.all()[-1].id != updated_status:
            new_status = Ticket_Status.query.filter_by(id=updated_status).first()
            ticket.ticket_statuses.append(new_status)
            return 'status ' + str(new_status.id) + str(ticket.ticket_statuses.all()[-1].id)

        # Commit Updates
        # db.session.commit() 

        # return str(ticket_id) + ' ' + str(ticket_title) + ' ' + str(ticket_overview) + ' ' + str(special_requirements) + ' ' + str(updated_status) + ' ' + str(assigned_user_id)
        return str(ticket.id) + ' ' + str(ticket.title) + ' ' + str(ticket.overview) + ' ' + str(ticket.special_requirements)
        # return redirect(url_for('views.tickets'))

        