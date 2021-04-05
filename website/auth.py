from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Ticket, Ticket_Status, Priority
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    #if user currently logged in, go to dashboard
    if current_user.get_id():
        return redirect(url_for('views.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    
    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.front_page'))


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            if current_user.id == 1:
                priorities = ['low','medium','high','critical']
                for i,priority in enumerate(priorities):
                    new_priority = Priority(id = i+1, priority_decoded=priority)
                    db.session.add(new_priority)
                statuses = ['Request Submitted', 'Initial Review', 'Development 1', 'QA 1', 'Development 2', 'QA 2', 'Completed', 'Cancelled']
                for i, status in enumerate(statuses):
                    new_status = Ticket_Status(id=i+1, name=status)
                    db.session.add(new_status)
                db.session.commit()    
            return redirect(url_for('views.dashboard'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/new_ticket', methods=['GET', 'POST'])
@login_required
def new_ticket():
    if request.method == 'POST':
        ticket_name = request.form.get('ticket_name')
        ticket_desc = request.form.get('ticket_desc')
        spec_requirements = request.form.get('spec_requirements')
        req_priority = request.form.get('req_priority')

        status = Ticket_Status.query.filter_by(id='1').first()
        
        new_ticket = Ticket(title=ticket_name, overview=ticket_desc, spec_requirements=spec_requirements, req_priority=req_priority, owner_id=current_user.id )

        new_ticket.ticket_ticket_status.append(status)

        

        db.session.add(new_ticket)
        db.session.commit()
        flash('Request submitted!', category='success')

        # return str(new_ticket.title) + ' ' + str(new_ticket.overview) + ' ' + str(new_ticket.spec_requirements) + ' ' + str(new_ticket.req_priority) + ' ' + str(new_ticket.owner_id) + ' ' + str(user_id) + ' ' + str(status.id)
        # return str(status)
        return redirect(url_for('views.dashboard'))
     