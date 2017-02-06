#coding=utf-8
'''
Created on 2016年12月29日

@author: huangning
'''
from flask_wtf import Form
from wtforms import StringField, TextField,PasswordField,TextAreaField
from wtforms.validators import DataRequired, Length
from models import User

class CommentForm(Form):
    """Form vaildator for comment."""

    # Set some field(InputBox) for enter the data.
    # patam validators: setup list of validators
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=255)])

    text = TextField(u'Comment', validators=[DataRequired()])
    
    
class PostForm(Form):
    """Form vaildator for comment."""

    # Set some field(InputBox) for enter the data.
    # patam validators: setup list of validators
    title = StringField('Title', [DataRequired(), Length(max=255)])
    text = TextAreaField('Blog Content', [DataRequired()])    
    
