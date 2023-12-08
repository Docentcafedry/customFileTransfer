import bcrypt
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from models import User, db


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter(User.email == email).first()

        if not user or not bcrypt.checkpw(password.encode(), user.password):
            flash('Incorrect credential')
            return redirect(url_for('auth.login'))

        return redirect('profile')

    return render_template('login.html')

@auth.route('/signup' ,methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("name")
        password = request.form.get("password")

        user = User.query.filter(User.email == email).first()

        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        salt = bcrypt.gensalt()

        new_user = User(
            email=email,
            name=username,
            password=bcrypt.hashpw(password.encode(), salt)
        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('signup.html')



@auth.route('/logout')
def logout():
    return render_template('logout.html')



