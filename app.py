"""Blogly application."""

from crypt import methods
from curses.ascii import US
from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def root():
    return redirect("/users")

@app.route('/users', methods=["GET"])
def show_users():
    """show a page listing all users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def new_user_form():
    """Gives user a form to fill out to sign up"""

    return render_template('users/new.html')

@app.route('/users/new', methods=["POST"])
def new_user_form_submit():
    """handles user submitting form when signing up"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return render_template("/users")

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """render a page with info about a particular user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

@app.route('users/<int:user_id>/edit')
def users_edit(user_id):
    """shows form to edit info on a particular user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user_submit(user_id):
    """handles submitting of form to edit a particular user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes a particular user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")