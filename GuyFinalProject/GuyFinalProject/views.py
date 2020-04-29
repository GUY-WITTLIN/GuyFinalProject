"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from GuyFinalProject import app
from GuyFinalProject.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError


from GuyFinalProject.Models.QueryFormStructure import QueryFormStructure
from GuyFinalProject.Models.QueryFormStructure import LoginFormStructure 
from GuyFinalProject.Models.QueryFormStructure import UserRegistrationFormStructure
from GuyFinalProject.Models.Forms import UserDataQuery 
from GuyFinalProject.Models.QueryFormStructure import ExpandForm
from GuyFinalProject.Models.QueryFormStructure import CollapseForm 
from flask_bootstrap import Bootstrap

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def convert_bool_to_int(s):
    if s == False:
        return 0
    else:
        return 1

bootstrap = Bootstrap(app)

db_Functions = create_LocalDatabaseServiceRoutines()


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='This Is My Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='On This Page You Can See Details About Me:',
        year=datetime.now().year,
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About The Project',
        year=datetime.now().year,
    )


@app.route('/Album')
def Album():
    """Renders the about page."""
    return render_template(
        'PictureAlbum.html',
        title='This Is My Picture Album',
        year=datetime.now().year,
        message='The Biggest Wins Of The Best National & Club Teams In Football (From 2010-2019):'
    )

# -------------------------------------------------------
# Register new user page
# -------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thank You, You Will Register Now :) '+ form.FirstName.data + " " + form.LastName.data )
        else:
            flash('Error: User with this Username already exist! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='In This Page You Can Register New User:',
        year=datetime.now().year,
        repository_name='Pandas',
        )


@app.route('/DataModel')
def DataModel():
    """Renders the contact page."""
    return render_template(
        'DataModel.html',
        title='This Is My DataModel',
        year=datetime.now().year,
        message='In This DataModel I Will Take 2 Datasets And Try To Find The Connection Between Them.'
    )

@app.route('/data/Data1' , methods = ['GET' , 'POST'])
def Data1():
    form1 = ExpandForm()
    form2 = CollapseForm()
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/Whether.csv'))
    raw_data_table = ''

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.head(101).to_html(classes = 'table table-hover')
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''
   
    return render_template(
        'Data1.html',
        title='The Rain Data',
        year=datetime.now().year,
        message='This Data Shows If There Was A Rain Every Day Since 1948 In Seattle, USA.',
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2
    )

@app.route('/data/Data2' , methods = ['GET' , 'POST'])
def Data2():
    form1 = ExpandForm()
    form2 = CollapseForm()
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/Car.csv'))
    raw_data_table = ''

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.head(101).to_html(classes = 'table table-hover')
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''
   
    return render_template(
        'Data2.html',
        title='The Car Accidents Data',
        year=datetime.now().year,
        message='This Data Shows If There Was A Car Accidents, The Time And Where.',
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2
    )

@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)
    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('You Successfully Login To The Website!')
            return redirect('Dataquery')
        else:
            flash('Error In - Username and/or Password!!!')
   
    return render_template(
        'login.html', 
        form=form, 
        title='In This Page You Can Login To The Website:',
        year=datetime.now().year,
    )

@app.route('/Dataquery', methods=['GET', 'POST'])
def Dataquery():
    form = UserDataQuery(request.form)
    chart = 'static\\Images\\CarRain.jpg'
    height_case_1 = "100"
    width_case_1 = "400"
    if (request.method == 'POST'):
        Car = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\Car.csv'))
        Car = Car.drop(['Location', 'Person count', 'Vehicle Count', 'Injuries', 'Hit Parked Car'],1)
        Car = Car.groupby('Date').size().to_frame()
        Car = Car.rename(columns={0: "NumOfAccidents"})
        Car.index = pd.to_datetime(Car.index)
        Car = Car.sort_index()
        Car = Car.rename(columns={'0': 'Accidents'})
        Start_Date = form.Start_Date.data
        End_Date = form.End_Date.data
        Car = Car[Start_Date:End_Date]
        fig1 = plt.figure()
        ax = fig1.add_subplot(111)
        fig1.subplots_adjust(bottom=0.4)
        Car.plot(ax = ax, kind = 'bar')
        chart = plt_to_img(fig1)

    return render_template(
        'Dataquery.html', 
        form=form, 
        chart=chart,
        height_case_1=height_case_1,
        width_case_1=width_case_1,
        title='This Is My DataQuery Page, Please Enter A Start Date And End Date:',
        year=datetime.now().year,
    )
def plt_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String

app.config['SECRET_KEY'] = 'For PA'