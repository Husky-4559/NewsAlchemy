from flask import Blueprint, render_template, url_for, flash, redirect, jsonify, request
from flask_login import login_user, current_user, logout_user, login_required
from forms import RegistrationForm, LoginForm
from models import db, User, Favorite
import requests
from flask import current_app as app

main = Blueprint('main', __name__)

@main.route("/")
@login_required
def home():
    return render_template('home.html')

@main.route("/sports")
@login_required
def sports():
    return render_template('sports.html')

@main.route("/entertainment")
@login_required
def entertainment():
    return render_template('entertainment.html')

@main.route("/technology")
@login_required
def technology():
    return render_template('technology.html')

@main.route("/favorites", methods=['GET', 'POST', 'DELETE'])
@login_required
def favorites():
    if request.method == 'GET':
        user_favorites = Favorite.query.filter_by(user_id=current_user.id).all()
        return render_template('favorites.html', favorites=user_favorites)

    if request.method == 'POST':
        try:
            data = request.get_json()
            title = data.get('title')
            url = data.get('url')
            if not title or not url:
                return jsonify({'success': False, 'message': 'Invalid data'}), 400

            # Check for existing favorite
            existing_favorite = Favorite.query.filter_by(user_id=current_user.id, url=url).first()
            if existing_favorite:
                return jsonify({'success': False, 'message': 'Article is already in favorites'}), 400

            favorite = Favorite(user_id=current_user.id, title=title, url=url)
            db.session.add(favorite)
            db.session.commit()
            return jsonify({'success': True, 'favorite': {'id': favorite.id, 'title': favorite.title, 'url': favorite.url}})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    if request.method == 'DELETE':
        try:
            favorite_id = request.args.get('id')
            favorite = Favorite.query.get(favorite_id)
            if favorite and favorite.user_id == current_user.id:
                db.session.delete(favorite)
                db.session.commit()
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': 'Favorite not found or unauthorized'}), 404
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

@main.route("/auth/<action>", methods=['GET', 'POST'])
def auth(action):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    login_form = LoginForm()
    register_form = RegistrationForm()

    if request.method == 'POST':
        if action == 'login' and login_form.validate_on_submit():
            user = User.query.filter_by(username=login_form.username.data).first()
            if user and user.check_password(login_form.password.data):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('main.favorites'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')

        if action == 'register' and register_form.validate_on_submit():
            user = User(username=register_form.username.data, email=register_form.email.data)
            user.set_password(register_form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('main.auth', action='login'))

    return render_template('auth.html', title='Login/Register', login_form=login_form, register_form=register_form, action=action)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.auth', action='login'))

@main.route("/fetch_news")
def fetch_news_route():
    category = request.args.get('category', 'general')
    news_data = fetch_news(category)
    app.logger.info(f"Fetched news for category: {category} | Data: {news_data}")  # Added logging
    return jsonify(news_data)

def fetch_news(category: str):
    url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={app.config['NEWS_API_KEY']}"
    response = requests.get(url)
    if response.status_code != 200:
        app.logger.error(f"Error fetching news: {response.status_code} {response.text}")
        return []
    articles = response.json().get('articles', [])
    # Filter out articles that have [Removed] in the title or null authors
    filtered_articles = [article for article in articles if '[Removed]' not in article.get('title', '') and article.get('author') is not None]
    app.logger.info(f"Fetched {len(filtered_articles)} articles for category '{category}'")
    return filtered_articles