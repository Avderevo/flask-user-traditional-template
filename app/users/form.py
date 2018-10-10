from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[validators.DataRequired()])
    email = StringField('email', [validators.DataRequired(), validators.email()])
    password = PasswordField('password', validators=[validators.DataRequired(), validators.EqualTo('confirm', message='passwords must match')])

    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[validators.DataRequired()])

    password = PasswordField('password', validators=[validators.DataRequired])

class UserEditForm(FlaskForm):
    username = StringField('username', validators=[validators.DataRequired()])
    email = StringField('email', [validators.DataRequired(), validators.email()])
    old_password = PasswordField('old password', validators=[validators.DataRequired()])
    new_password = PasswordField('new_password', validators=[validators.DataRequired(),
                                                     validators.EqualTo('confirm', message='passwords must match')])

    confirm = PasswordField('Repeat Password')