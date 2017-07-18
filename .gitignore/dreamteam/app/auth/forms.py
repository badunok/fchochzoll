from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Spieler


class RegistrationForm(FlaskForm):
    """
    Form REGISTER
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Benutzername', validators=[DataRequired()])
    vorname = StringField('Vorname', validators=[DataRequired()])
    nachname = StringField('Nachname', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Passwort wiederholen')
    submit = SubmitField('Registrieren')

    def validate_email(self, field):
        if Spieler.query.filter_by(email=field.data).first():
            raise ValidationError('Email ist bereits im System.')

    def validate_username(self, field):
        if Spieler.query.filter_by(username=field.data).first():
            raise ValidationError('Benutzername schon vergeben.')


class LoginForm(FlaskForm):
    """
    Form LOGIN
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Login')
