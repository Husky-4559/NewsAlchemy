# cSpell:ignore sqlalchemy jsonify wtforms newsalchemyuser yourpassword

from flask import Flask, render_template, url_for, flash, redirect, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_session import Session
from forms import RegistrationForm, LoginForm
from models import db, User, Favorite
import requests

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(int(user_id))

# Initialize Flask-Session
app.config['SESSION_SQLALCHEMY'] = db
Session(app)

@app.route("/")
@login_required
def home():
    news_data = fetch_news('general')
    return render_template('home.html', news_data=news_data)

@app.route("/sports")
@login_required
def sports():
    news_data = fetch_news('sports')
    return render_template('sports.html', news_data=news_data)

@app.route("/entertainment")
@login_required
def entertainment():
    news_data = fetch_news('entertainment')
    return render_template('entertainment.html', news_data=news_data)

@app.route("/technology")
@login_required
def technology():
    news_data = fetch_news('technology')
    return render_template('technology.html', news_data=news_data)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/favorite/<string:title>/<string:url>")
@login_required
def favorite(title, url):
    favorite = Favorite(user_id=current_user.id, title=title, url=url)
    db.session.add(favorite)
    db.session.commit()
    flash('Article added to favorites!', 'success')
    return redirect(request.referrer)

@app.route("/fetch_news")
@login_required
def fetch_news_route():
    category = request.args.get('category', 'general')
    news_data = fetch_news(category)
    return jsonify(news_data)

def fetch_news(category: str):
    url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={app.config['NEWS_API_KEY']}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json().get('articles')

if __name__ == '__main__':
    app.run(debug=True)