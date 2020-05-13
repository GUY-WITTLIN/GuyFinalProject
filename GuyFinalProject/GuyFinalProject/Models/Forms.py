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
#------------------------------------------------#



class UserDataQuery(FlaskForm): #The Class Where You Can Write The Start Date And End Date as A Date Field
    Start_Date = DateField('Start Date:' , format='%Y-%m-%d' , validators = [DataRequired]) #DateField Puts The Date That You Can Chose A Date And Not string
    End_Date = DateField('End Date:' , format='%Y-%m-%d' , validators = [DataRequired])
    submit = SubmitField('Submit') #SubmitField Do The Submit