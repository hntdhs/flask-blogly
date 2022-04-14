"""Blogly application."""

from crypt import methods
from curses.ascii import US
import re
from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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
    """Show recent posts, most recent first"""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    # what is the all()?
    return render_template("posts/homepage.html")

@app.errorhandler(404)
def page_not_found(e):
    """show 404 error page if user wants non-existent page"""

    return render_template('404.html'), 404
    #  why the integer 404 after render template?

############ User template

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
    flash(f"User {new_user.full_name} added.")

    return render_template("/users")
    # noticed in earlier version they had this as render template, and in part 2 solution it's redirect("/users"). does it matter?

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

####### Posts route

@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Shows a form that creates a new post for a certain user"""

    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])    
def submit_new_post(user_id):
    """form submission handler for creating new post"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'], content=request.form['content'], user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post {'new_post.title'} added.")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id')
def show_post(post_id):
    """show info for a requested post"""

    post = Post.query.get_or_404(post_id)
    return render_template('/posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """shows a form to edit existing post"""

    post = Post.query.get_or_404(post_id)
    return render_template('/posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """handles form submission for editing an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"f/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """handles form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' deleted.")

    return redirect(f"/users/{post.user_id}")