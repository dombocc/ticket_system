from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Ticket, Ticket_Status, Priority, User_Type
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
        elif validate_password_requirements(password1,password2):
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method='sha256'), user_type = 2, admin = 0)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')

            # Initialize Data for database
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
                user_types = ['Developer', 'Read_Only']
                for i, types in enumerate(user_types):
                    new_user_type = User_Type(id=i+1, user_type_decoded=types)
                    db.session.add(new_user_type)
                db.session.commit()  
            #Redirect to Dashboard    
            return redirect(url_for('views.dashboard'))

    return render_template("sign_up.html", user=current_user)


# Update User Info Through single_user_info.html
@auth.route('/admin-update_user', methods=['POST'])
@login_required
def update_user():

    user_id = int(request.form.get('user_id'))
    if current_user.admin == 1 or current_user.id == user_id:
        if request.method == 'POST':

            # Get user entitiy
            user = User.query.filter_by(id=user_id).first()

                    
            first_name = request.form.get('first_name')
            # update user first_name
            if user.first_name != first_name:
                user.first_name = first_name
            
            last_name = request.form.get('last_name')
            # update user last_name
            if user.last_name != last_name:
                user.last_name = last_name


            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
            # update user password
            if password1 == '' or check_password_hash(user.password, password1):
                pass
            elif validate_password_requirements(password1, password2):
                return redirect(url_for('views.view_single_user', user_id = user_id))
            else:
                user.password = generate_password_hash(password1, method='sha256')
            
            user_type = int(request.form.get('user_type'))
            # update user user_type
            if user.user_type != user_type:
                user.user_type = user_type

            admin_level = int(request.form.get('admin_level'))
            # update user admin level
            if user.admin != admin_level:
                user.admin = admin_level
                    
            # Commit Updates
            db.session.commit() 

            # return to all users
            return redirect(url_for('views.view_all_users'))


    # flash ineligble to make changes and return to dashboard
    else:
        flash('You are not eligible to make these changes', category='error')
        return redirect(url_for('views.dashboard'))

def validate_password_requirements(pass1,pass2):
    if pass1 != '':
        if pass1 != pass2:
            flash('Passwords don\'t match.', category='error')
            return True
        elif len(pass1) < 7:
            flash('Password must be at least 7 characters.', category='error')
            return True
        else:
            return False