from flask_login import UserMixin 
from . import db
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


# login_manager = LoginManager()
# @login_manager.user_loader
# def user_loader(email):
#     if email not in users:
#         return
    
#     user = User()
#     user.id = email
#     return user

# @login_manager.request_loader
# def request_loader(request):
#     email = request.form.get('email')
#     if email not in users:
        # return
