"""Blogly application."""

from flask import Flask, request, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

#USER

@app.route('/')
def home():
    """Homepage"""
    return redirect('/users')

@app.route('/users')    
def users_index():
    """List of users page"""

    users = User.query.all()
    return render_template('/users/index.html', users=users)

@app.route('/users/new_user', methods=['GET'])
def new_user_page():
    """Shows a form for new user (get request)"""
    return render_template('/users/new_user.html')

@app.route('/users/new_user', methods=['POST'])
def new_user_form():
    """Handle form submission for creating a new user (post request)"""

    new = User(first_name=request.form['first_name'], last_name=request.form['last_name'], image_url=request.form['image_url'] or None)

    db.session.add(new)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_page(user_id):
    """Show information about given user"""

    user = User.query.get_or_404(user_id)
    return render_template('/users/user_page.html', user=user)

@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show the edit page for a user (get request)"""

    user = User.query.get_or_404(user_id)
    return render_template('/users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def users_update(user_id):
    """Process the edit form to update an existing user (post request) """
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def users_delete(user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

#POST

@app.route('/users/<int:user_id>/posts/new_post')
def show_new_form(user_id):
    """Show form to add a post for that user"""
    user = User.query.get_or_404(user_id)
    return render_template('/posts/new_post.html', user=user)

@app.route('/users/<int:user_id>/posts/new_post', methods=['POST'])
def add_post(user_id):
    """Handle add form. add post and redirect to user detail page"""
    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'], 
                    content=request.form['content'], user_id=user_id)

    db.session.add(new_post)
    db.session.commit()
    
    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/post_detail.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Shows form to edit post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    """Handle for submission for updating a post"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Handle form submission to delete post"""
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


