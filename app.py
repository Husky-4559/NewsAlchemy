# cSpell:ignore sqlalchemy jsonify wtforms newsalchemyuser yourpassword

import os
from flask import Flask, redirect, url_for
from models import db, bcrypt, User
from flask_login import LoginManager
from routes import main as main_blueprint
from config import Config

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Set the login view with the default action
    login_manager.login_view = 'main.auth'
    login_manager.login_message = u"Please log in to access this page."
    login_manager.login_message_category = "info"

    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()  # Ensure the database tables are created

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Override the default unauthorized handler to add the action parameter
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('main.auth', action='login'))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)