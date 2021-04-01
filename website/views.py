from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def front_page():
    return render_template('front_page.html')

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@views.route('/new_ticket')
@login_required
def new_ticket():
    return render_template('new_ticket.html')