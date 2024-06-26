import re

from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.fields.simple import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, ValidationError, EqualTo, StopValidation, input_required

from interface.models import User


class AdminPanelForm(FlaskForm):
    change_people = IntegerField('Pas wachtrij aan', validators=[DataRequired()])
    submit = SubmitField('Voeg toe')


class RegistrationForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    password = PasswordField('Wachtwoord',
                             validators=[DataRequired(),
                                         EqualTo('pass_confirm', message='Wachtwoorden komen niet overeen!')])
    pass_confirm = PasswordField('Bevestig wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Registreer!')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Deze gebruikersnaam is al in gebruik.")

    def validate_password(self, field):

        if len(field.data) < 8:
            raise ValidationError("Wachtwoorden moeten minimaal 8 tekens lang zijn.")

        if re.search(r"\d", field.data) is None:
            raise ValidationError("Wachtwoorden moeten minimaal één nummer bevatten.")

        if re.search(r"[A-Z]", field.data) is None:
            raise ValidationError("Wachtwoorden moeten minimaal één hoofdletter bevatten.")

        if re.search(r"[a-z]", field.data) is None:
            raise ValidationError("Wachtwoorden moeten minimaal één kleine letter bevatten.")

        if re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', field.data) is None:
            raise ValidationError("Wachtwoorden moeten minimaal één speciaal karakter zoals !#$% bevatten.")


def validate_password(form, field):
    user = User.query.filter_by(username=form.username.data).first()
    if user:
        password_hash = user.password_hash
        if not check_password_hash(password_hash, field.data):
            raise ValidationError("Incorrect wachtwoord.")


class LoginForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    password = PasswordField('Wachtwoord', validators=[DataRequired(), validate_password])
    submit = SubmitField('log in')

    def validate_username(self, field):
        if not User.query.filter_by(username=field.data).first():
            raise StopValidation("Deze gebruikersnaam bestaat niet.")


class SettingsForm(FlaskForm):
    truck_count = IntegerField('Hoeveelheid Trucks', validators=[input_required("Voeg in ieder geval 1 truck toe.")])
    delay_amount = IntegerField('Hoeveelheid Oponthoud', validators=[input_required("Je moet opgeven hoe veel "
                                                                                    "oponthoud er is.")])
    submit = SubmitField('Pas aan')
