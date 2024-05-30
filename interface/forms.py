from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.fields.simple import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, ValidationError, EqualTo

from interface.models import User


class AdminPanelForm(FlaskForm):
    people_amount = IntegerField('Aantal mensen in de rij: ')
    truck_amount = FloatField('Aantal trucks die gevuld worden: ')
    submit = SubmitField('Enter')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Wachtwoord',
                             validators=[DataRequired(),
                                         EqualTo('pass_confirm', message='Wachtwoorden komen niet overeen!')])
    pass_confirm = PasswordField('Bevestig wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Registreer!')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Deze gebruikersnaam is al in gebruik!')

class LoginForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    submit = SubmitField('log in')
