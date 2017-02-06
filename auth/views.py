#coding=utf-8
'''
Created on 2016年12月30日

@author: huangning
'''
from . import auth
from flask import flash,redirect,render_template,url_for
from forms import LoginForm,RegisterForm
from models import User,db
from uuid import uuid4



@auth.route('/login', methods=['GET', 'POST'])
def login():
    """View function for login."""

    # Will be check the account whether rigjt.
    form = LoginForm()

    if form.validate_on_submit():
        flash("You have been logged in.", category="success")
        print "ssss"
        return redirect(url_for('main.home'))

    return render_template('auth/login.html',
                           form=form)


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    """View function for logout."""

    flash("You have been logged out.", category="success")
    return redirect(url_for('main.home'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """View function for Register."""

    # Will be check the username whether exist.
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(id=str(uuid4()),
                        username=form.username.data,
                        password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash('Your user has been created, please login.',
              category="success")

        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html',
                           form=form)