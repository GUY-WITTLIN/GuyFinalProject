from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import Form, BooleanField, PasswordField , HiddenField , DateTimeField , IntegerField , DecimalField , FloatField , RadioField
from wtforms import Form, SelectMultipleField , BooleanField
from wtforms import TextField, TextAreaField, SelectField
from wtforms import validators, ValidationError
from wtforms.fields.html5 import DateField

from wtforms.validators import DataRequired
from wtforms.validators import InputRequired


class UserDataQuery(FlaskForm):
    Start_Date = DateField('Start Date:' , format='%Y-%m-%d' , validators = [DataRequired])
    End_Date = DateField('End Date:' , format='%Y-%m-%d' , validators = [DataRequired])
    submit = SubmitField('Submit')


class AllOfTheAboveForm(FlaskForm):
    string_field_entry = StringField('Enter a String:' , validators = [DataRequired])
    text_area_field_entry = TextAreaField('Enter Text:' , validators = [DataRequired])
    password_field_entry = PasswordField('Enter Password:' , validators = [DataRequired])
    date_field_entry = DateField('Enter Date:' , format='%Y-%m-%d' , validators = [DataRequired])
    integer_field_entry = IntegerField('Enter an Integer:' , validators = [DataRequired])
    decimal_field_entry = DecimalField('Enter a Decimal:' , validators = [DataRequired])
    boolean_field_entry = BooleanField('Enter a Boolean:' , validators = [DataRequired])
    radio_field_entry = RadioField('Choose one of:' , validators = [DataRequired] , choices=[('1', 'A'), ('2', 'B'), ('3', 'C') , ('4', 'D')])
    select_field_entry = SelectField('Select:' , validators = [DataRequired] , choices=[('trump', 'Trump'), ('obama', 'Obama'), ('bush', 'Bush') , ('clinton', 'Clinton')])
    select_field_multiple_entry = SelectMultipleField('Select Multiple:' , validators = [DataRequired] , choices=[('trump', 'Trump'), ('obama', 'Obama'), ('bush', 'Bush') , ('clinton', 'Clinton')])
    subnmit = SubmitField('submit')
