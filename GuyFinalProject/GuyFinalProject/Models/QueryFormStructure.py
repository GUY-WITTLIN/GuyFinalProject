from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import Form, BooleanField, PasswordField
from wtforms import TextField, TextAreaField, SelectField, DateField
from wtforms import validators, ValidationError
from wtforms.validators import DataRequired
from wtforms.validators import InputRequired
#------------------------------------------------#




class LoginFormStructure(FlaskForm): #Class That Shows All Of the fields That We need to put in the Login Page.
    username   = StringField('Username:  ' , validators = [DataRequired()])
    password   = PasswordField('Password:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')


class UserRegistrationFormStructure(FlaskForm): #Class That Shows All Of the field that We need to Put in the Register Page.
    FirstName  = StringField('First name:  ' , [validators.Length(min=2)]) #Min,Max = The Minimun and the maximun That You Need to put On Some Fields.
    LastName   = StringField('Last name:  ' , [validators.Length(min=2)])
    PhoneNum   = StringField('Phone number:  ' , [validators.Length(min=10, max=10)])
    EmailAddr  = StringField('E-Mail:  ' , [validators.Email()])
    username   = StringField('Username:  ' , [validators.Length(min=5, max=15)])
    password   = PasswordField('Password:  ' , [validators.Length(min=5, max=15)]) #PasswordField Puts The Password On Points and not visible
    submit = SubmitField('Submit')


class ExpandForm(FlaskForm): #Expand, Open The DataSet On Data1/2.html
    submit1 = SubmitField('Expand')
    name="Expand" 
    value="Expand"

class CollapseForm(FlaskForm): #Collapse, Close The DataSet On Data1/2.html
    submit2 = SubmitField('Collapse')
    name="Collapse" 
    value="Collapse"