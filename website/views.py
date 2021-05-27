from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Ticket, Ticket_Status, Priority, ticket_ticket_status, User_Type
from sqlalchemy import text

views = Blueprint('views', __name__)

@views.route('/')
def front_page():
    if current_user.get_id():
        return redirect(url_for('views.view_all_tickets'))
    return render_template('front_page.html')

@views.route('/dashboard')
@login_required
def dashboard():

    return render_template('dashboard.html')


@views.route('/new_ticket', methods=['GET', 'POST'])
@login_required
def create_new_ticket():
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
        return redirect(url_for('views.view_all_tickets'))

    # If 'GET' request
    return render_template('new_ticket.html')


@views.route('/tickets', methods=['GET','POST'])
@login_required
def view_all_tickets():

    if request.method == 'POST':
        filter_ticket_id = request.form.getlist('filter_ticket_id')
        filter_ticket_status = request.form.getlist('filter_ticket_status')
        filter_ticket_owner = request.form.getlist('filter_ticket_owner')
        filter_ticket_developer = request.form.getlist('filter_ticket_developer')
        cur_user = User.query.filter_by(id=current_user.id).first()
        all_ticket_statuses = Ticket_Status.query.all()
        all_users = User.query.all()

        # Initialize bool for 'select all's
        filter_ticket_id_all_bool = False
        filter_ticket_status_all_bool = False
        filter_ticket_owner_all_bool = False
        filter_ticket_developer_all_bool = False

        if cur_user.user_type == 1 or cur_user.admin == 1:
            all_tickets = Ticket.query.filter_by().all()
        else:
            all_tickets = Ticket.query.filter_by(owner_id=cur_user.id).all()
        

        # add filter capabilities
        # filter by ticket id
        # filter_1
        filter_1 = []
        if len(filter_ticket_id) == 1 and filter_ticket_id[0] == "":
            filter_ticket_id_all_bool = True
            filter_1 = all_tickets
        else:
            for ticket in all_tickets:
                if str(ticket.id) in filter_ticket_id:
                    filter_1.append(ticket)
        
        # filter by ticket status
        # filter_2
        filter_2 = []
        if len(filter_ticket_status) == 1 and filter_ticket_status[0] == "":
            filter_ticket_status_all_bool = True
            filter_2 = filter_1
        else:
            for ticket in filter_1:
                if str(ticket.ticket_statuses[-1].id) in filter_ticket_status:
                    filter_2.append(ticket)
    
        # filter by owner
        # filter 3
        filter_3 = []
        if len(filter_ticket_owner) == 1 and filter_ticket_owner[0] == "":
            filter_ticket_owner_all_bool = True
            filter_3 = filter_2
        else:
            for ticket in filter_2:
                if str(ticket.owner_id) in filter_ticket_owner:
                    filter_3.append(ticket)

        # filter by developer  
        # filter 4
        filter_4 = []
        if len(filter_ticket_developer) == 1 and filter_ticket_developer[0] == "":
            filter_ticket_developer_all_bool = True
            filter_4 = filter_3
        else:
            for ticket in filter_3:
                if str(ticket.assigned_id) in filter_ticket_developer:
                    filter_4.append(ticket)
        
        if len(filter_4) == 0:
            if filter_ticket_id_all_bool and filter_ticket_status_all_bool and filter_ticket_owner_all_bool and filter_ticket_developer_all_bool:
                pass
            else:
                flash('No Tickets Exist With These Filters, Returning All', category='error')

            output_tickets = all_tickets
        else:
            output_tickets = filter_4

            
        return render_template('tickets.html', tickets=output_tickets, all_tickets=all_tickets, all_ticket_statuses=all_ticket_statuses, all_users=all_users)

    
    #Split tickets page on developers/users
    if request.method == 'GET':
        cur_user = User.query.filter_by(id=current_user.id).first()
        all_ticket_statuses = Ticket_Status.query.all()
        all_users = User.query.all()
        if cur_user.user_type == 1 or cur_user.admin == 1:
            all_tickets = Ticket.query.all()
            return render_template('tickets.html', tickets=all_tickets, all_tickets = all_tickets, all_ticket_statuses=all_ticket_statuses, all_users=all_users)
        else:
            all_tickets = Ticket.query.filter_by(owner_id=cur_user.id).all()
            return render_template('tickets.html', tickets=all_tickets ,all_tickets = all_tickets, all_ticket_statuses=all_ticket_statuses, all_users=all_users)

        

    
    # GETS TICKET STATUSES
    # tickets = Ticket.query.join(Ticket_Status, Ticket.ticket_statuses).first()
    # return str(tickets.id) + ' ' + str(tickets.title) + ' ' + str(tickets.ticket_status.first().name) + ' ' + str(tickets.title)

    # GIVES PRIORITY
    # tickets = Ticket.query.join(Priority, Ticket.req_priority==Priority.id).first()
    # return str(tickets.id) + ' ' + str(tickets.req_priority) + ' ' + str(tickets.priority.priority_decoded)
 

@views.route('/ticket-<ticket_id>', methods=['GET','POST'])
@login_required
def view_single_ticket(ticket_id):


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
        ticket_status.append([ status_dict[statuses[i][1]]  , statuses[i][2] ])
    
    # Get List of developers
    developers = User.query.filter_by(user_type=1).order_by(User.id).all()

    #Get List of statuses for updates
    ticket_statuses = Ticket_Status.query.order_by(Ticket_Status.id).all()

    priorities = Priority.query.all()
    
    
    return render_template('single_ticket_info.html', ticket=ticket, ticket_status=ticket_status[::-1], count_status=len(statuses), 
                developers=developers, developer_length = len(developers), ticket_statuses=ticket_statuses, current_ticket_status=current_ticket_status,
                priorities = priorities)
    


# Update Ticket Info Through single_ticket_info.html
@views.route('/update_ticket', methods=['POST'])
@login_required
def update_ticket():
    if request.method == 'POST':

        ticket_id = int(request.form.get('ticket_id'))
        # Get current ticket entitiy
        ticket = Ticket.query.filter_by(id=ticket_id).first()

                
        ticket_title = request.form.get('ticket_title')
        # update ticket title
        if ticket.title != ticket_title:
            ticket.title = ticket_title
            # return 'title ' + str(ticket_title)
        
        ticket_overview = request.form.get('ticket_overview')
        # update ticket overview
        if ticket.overview != ticket_overview:
            ticket.overview = ticket_overview
            # return 'overview ' + str(ticket_overview)
        
        special_requirements = request.form.get('special_requirements')
        # update ticket special_requirements
        if ticket.special_requirements != special_requirements:
            ticket.special_requirements = special_requirements
            # return 'spec_req ' + str(special_requirements)
        
        initial_review_text = request.form.get('task_review')
        # update ticket special_requirements
        if ticket.initial_review_task != initial_review_text:
            ticket.initial_review_task = initial_review_text
            # return 'spec_req ' + str(special_requirements)
        

        updated_status = int(request.form.get('update_status'))
        # update ticket status
        if ticket.ticket_statuses.all()[-1].id != updated_status:
            new_status = Ticket_Status.query.filter_by(id=updated_status).first()
            for status in ticket.ticket_statuses.all():
                if status.id >= new_status.id:
                    status = Ticket_Status.query.filter_by(id=status.id).first()
                    ticket.ticket_statuses.remove(status)
            ticket.ticket_statuses.append(new_status)
            # return 'status ' + str(new_status.id) + str(ticket.ticket_statuses.all()[-1].id)
        
        
        if request.form.get('assigned_user') != '':
            assigned_user_id = int(request.form.get('assigned_user'))
            # update ticket assigned_user
            # if no assigned user
            if not ticket.assigned_user:
                ticket.assigned_id = assigned_user_id
                # return 'new assigned_dev ' + str(assigned_user_id)+ str(ticket.assigned_id)
            else:
            # if there is an assigned user
                if ticket.assigned_user.id != assigned_user_id:
                    ticket.assigned_id = assigned_user_id
                    # return 'assigned_dev ' + str(assigned_user_id)+ str(ticket.assigned_user.id)


        if request.form.get('assigned_priority') != '':
            assigned_priority = int(request.form.get('assigned_priority'))
            # assign a priority
            if not ticket.assigned_pri:
                ticket.assigned_priority = assigned_priority
                # return 'new assigned_pri ' + str(assigned_priority)+ str(ticket.assigned_priority)
            else:
                if ticket.assigned_pri.id != assigned_priority:
                    ticket.assigned_priority = assigned_priority
                    # return 'assigned_pri ' + str(assigned_priority)+ str(ticket.assigned_pri.id)
        
        

        # Commit Updates
        db.session.commit() 

        # return str(ticket_id) + ' ' + str(ticket_title) + ' ' + str(ticket_overview) + ' ' + str(special_requirements) + ' ' + str(updated_status) + ' ' + str(assigned_user_id)
        # return str(ticket.id) + ' ' + str(ticket.title) + ' ' + str(ticket.overview) + ' ' + str(ticket.special_requirements) + ' ' + str(ticket.requested_pri.id)
        return redirect(url_for('views.view_all_tickets'))


# View User Info Through users.html
@views.route('/admin-users', methods=['GET','POST'])
@login_required
def view_all_users():

    #Split users page on admin/ everyone else
    cur_user = User.query.filter_by(id=current_user.id).first()
    if cur_user.admin == 1:
        users = User.query.all()
        return render_template('users.html', users=users)
    else:
        return redirect(url_for('views.view_single_user', user_id = cur_user.id))


# View Single User Info Through single_user_info.html
@views.route('/admin-user-<user_id>', methods=['GET','POST'])
@login_required
def view_single_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user == None:
        flash('User Doesn\'t Exist', category='error')
        return redirect(url_for('views.dashboard'))
    elif current_user.admin != 1 and current_user.id != user.id:
        flash('You don\'t have access', category='error')
        return redirect(url_for('views.dashboard'))
    else:
        user_types = User_Type.query.all()
        return render_template('single_user_info.html', user = user, user_types = user_types)



