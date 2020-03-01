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
from GuyFinalProject.Models.QueryFormStructure import ExpandForm
from GuyFinalProject.Models.QueryFormStructure import CollapseForm 
from flask_bootstrap import Bootstrap
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
        title='This Is My Conatct Page',
        year=datetime.now().year,
        message='You Can Call Me Or Email Me :-)'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About Me',
        year=datetime.now().year,
    )


@app.route('/Album')
def Album():
    """Renders the about page."""
    return render_template(
        'PictureAlbum.html',
        title='Pictures',
        year=datetime.now().year,
        message='Welcome to my picture album'
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
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='In This Page You Can Register New User',
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
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\data\\Whether.csv'))
    raw_data_table = ''

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
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
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\data\\Car.csv'))
    raw_data_table = ''

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
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