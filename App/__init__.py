from flask import Flask
from .models import db, User, Book, Review

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Update with your database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def initialize_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database initialized!")

app = create_app()