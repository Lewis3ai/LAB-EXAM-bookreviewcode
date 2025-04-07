import click, csv
from flask import Flask
from flask.cli import with_appcontext
from App import app, Book, Review, initialize_db
from App.models import User, db  # Import User and db


@app.cli.command("init")
def initialize():
  initialize_db()


@app.cli.command("list-books")
def list_books():
  books = Book.query.all()
  print(books)

@app.cli.command("create-user")
@click.argument("username")
@click.argument("password")
def create_user_command(username, password):
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        print(f"Error: A user with the username '{username}' already exists.")
        return
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    print(f"{username} created!")