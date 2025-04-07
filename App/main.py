import os, csv
from flask import Flask, redirect, render_template, jsonify, request, send_from_directory, flash, url_for
from flask_cors import CORS
from sqlalchemy.exc import OperationalError, IntegrityError
from App.models import db, Book, Review, User
from datetime import timedelta
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
    current_user,
    set_access_cookies,
    unset_jwt_cookies,
)

def create_app():
    app = Flask(__name__, static_url_path='/static')
    CORS(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
    app.config['SECRET_KEY'] = 'MySecretKey'
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
    app.config["JWT_COOKIE_SECURE"] = True
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
    app.app_context().push()
    return app

app = create_app()
db.init_app(app)

jwt = JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.get(identity)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_action():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        response = redirect(url_for('home'))
        access_token = create_access_token(identity=user.id)
        set_access_cookies(response, access_token)
        return response
    else:
        flash('Invalid username or password')
        return redirect(url_for('login'))

@app.route('/app')
@jwt_required()
def home():
    books = Book.query.all()
    return render_template('index.html', books=books, user=current_user)

@app.route('/logout')
def logout():
    response = redirect(url_for('login'))
    unset_jwt_cookies(response)
    flash('Logged out successfully')
    return response

@app.route('/add-review/<isbn>', methods=['POST'])
@jwt_required()
def add_review(isbn):
    rating = request.form.get('rating')
    text = request.form.get('text')
    book = Book.query.filter_by(isbn=isbn).first()
    if book:
        review = Review(text=text, rating=int(rating), isbn=isbn, user_id=current_user.id)
        db.session.add(review)
        db.session.commit()
        flash('Review added successfully!')
        return redirect(url_for('home'))
    flash('Error adding review.')
    return redirect(url_for('home'))

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)