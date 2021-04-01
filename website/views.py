from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def front_page():
    return render_template('front_page.html')

@views.route('/dashboard')
def home():
    return render_template('dashboard.html')