#coding=utf-8
'''
Created on 2016年12月30日

@author: huangning
'''
from flask_wtf import Form
from wtforms import StringField, TextField,PasswordField
from wtforms.validators import DataRequired, Length,EqualTo
from models import User
from flask import flash



class LoginForm(Form):
    """Login Form"""

    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired()])

    def validate(self):
        """Validator for check the account information."""
        check_validata = super(LoginForm, self).validate()
        
        # If validator no pass
        if not check_validata:
            
            return False

        # Check the user whether exist.
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username')
            return False

        # Check the password whether right.
        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid password.')
            return False
        return check_validata
class RegisterForm(Form):
    """Register Form."""

    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired(), Length(min=8,message='Passwords at least 8 bits.')])
    confirm = PasswordField('Confirm Password', [DataRequired(), EqualTo('password',message='Passwords must match.')])
    #recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        # If validator no pass
        if not check_validate:
            return False

        # Check the user whether exist.
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('User with that name already exists.')
            return False
        return True