from flask import Flask, escape, request, render_template
from flask_login import LoginManager
from .models import User




def create_app():
    app = Flask(__name__)
    # login_manager = LoginManager()
    # login_manager.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    

    # @login_manager.user_loader
    # def load_user(id):
    #     return User.get(int(id))
    
    return app
