from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    login = request.form.get('login')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(login=login).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.index'))
'''
@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    login = request.form.get('login')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(login=login).first()

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Login address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(login=login, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))
'''
@auth.route('/change_password')
@login_required
def change_password():
    return render_template('change_password.html')

@auth.route('/change_password', methods=['POST'])
@login_required
def change_password_post():
    # code to validate and add user to database goes here
    old_pass = request.form.get('old_pass')
    new_pass = request.form.get('new_pass')

    user = User.query.filter_by(login='admin').first()

    if not user or not check_password_hash(user.password, old_pass):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.change_password')) # if the user doesn't exist or password is wrong, reload the page

    user.password = generate_password_hash(new_pass, method='pbkdf2:sha256')

    db.session.commit()

    return redirect(url_for('auth.logout'))

@auth.route('/delete_admin')
@login_required
def delete_admin():

    User.query.filter(User.login == "admin").delete()
    db.session.commit()

    return redirect(url_for('auth.logout'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))