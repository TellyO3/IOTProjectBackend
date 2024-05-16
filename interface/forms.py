from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import SubmitField


class PeopleInputForm(FlaskForm):
    amount = IntegerField('Amount of people in queue: ')
    submit = SubmitField('Enter')
