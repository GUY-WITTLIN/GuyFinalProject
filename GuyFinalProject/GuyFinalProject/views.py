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


from GuyFinalProject.Models.QueryFormStructure import LoginFormStructure 
from GuyFinalProject.Models.QueryFormStructure import UserRegistrationFormStructure
from GuyFinalProject.Models.Forms import UserDataQuery 
from GuyFinalProject.Models.QueryFormStructure import ExpandForm
from GuyFinalProject.Models.QueryFormStructure import CollapseForm 
from flask_bootstrap import Bootstrap

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

bootstrap = Bootstrap(app)
db_Functions = create_LocalDatabaseServiceRoutines()
#----------------------------------------------------------#



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
    """Renders the contact page."""
    chart = 'static\\Images\\AboutPhoto.jpg' #The Image
    return render_template(
        'about.html',
        chart=chart,
        title='About The Project:',
        year=datetime.now().year,
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

            flash('Thank You, You Will Register Now :) '+ form.FirstName.data + " " + form.LastName.data ) #Register After All Good
        else:
            flash('Error: User with this Username already exist! - '+ form.username.data) #Error That The Username Is Exist
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='In This Page You Can Register New User:',
        year=datetime.now().year,
        )


@app.route('/DataModel')
def DataModel():
    """DataModel Home Page."""
    return render_template(
        'DataModel.html',
        title='This Is My DataModel',
        year=datetime.now().year,
        message='In This DataModel I Will Take 2 Datasets And Try To Find The Connection Between Them.'
    )


@app.route('/data/Data1' , methods = ['GET' , 'POST'])
def Data1():
    """First Data Page"""
    form1 = ExpandForm() #Expand/QueryFormStructure.
    form2 = CollapseForm() #Collapse/QueryFormStructure.
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/Whether.csv'))
    raw_data_table = '' #No DataSet Table

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.head(101).to_html(classes = 'table table-hover') #DataSet Table
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = '' #No DataSet Table
   
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
    """Second Data Page."""
    form1 = ExpandForm() #Expand/QueryFormStructure.
    form2 = CollapseForm() #Collapse/QueryFormStructure
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/Car.csv'))
    raw_data_table = '' #No DataSet Table

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.head(101).to_html(classes = 'table table-hover') #DataSet Table
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = '' #No DataSet Table
   
    return render_template(
        'Data2.html',
        title='The Car Accidents Data',
        year=datetime.now().year,
        message='This Data Shows If There Was A Car Accidents, The Time And Where.',
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2
    )


# -------------------------------------------------------
# Login New User
# -------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)
    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('You Successfully Login To The Website!') #After Login Message
            return redirect('Dataquery') #Moves to another page (DataQuery Page)
        else:
            flash('Error In - Username and/or Password!!!') #Error Text
    return render_template(
        'login.html', 
        form=form, 
        title='In This Page You Can Login To The Website:',
        year=datetime.now().year,
    )


@app.route('/Dataquery', methods=['GET', 'POST'])
def Dataquery():
    form = UserDataQuery(request.form) #UserDataQuery/Forms
    chart = 'static\\Images\\CarRain.jpg' #The Image

    if (request.method == 'POST'):
        Start_Date = form.Start_Date.data #Start_Date/UserDataQuery/Forms
        End_Date = form.End_Date.data #End_Date/UserDataQuery/Forms

        Car = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\Car.csv'))
        Car = Car.drop(['Location', 'Person count', 'Vehicle Count', 'Injuries', 'Hit Parked Car'],1) #Remove Things That We Don't Need
        Car = Car.groupby('Date').size().to_frame()
        Car.index = pd.to_datetime(Car.index) #Move Car.index to datetime
        Car = Car.sort_index()
        Car = Car[Start_Date:End_Date] #Put User Start Date And End Date To The Dataset
        Car = Car.reset_index()
        Car['Date'] = Car['Date'].astype(str) #Change the Date to string.

        Whether = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\Whether.csv'))
        Whether = Whether.drop(['Max Temp' ,'Min Temp'],1) #Remove Things That We Don't Need
        Whether['DATE'] = pd.to_datetime(Whether['DATE']) #Change Whether Date To Date Time
        Whether = Whether.set_index('DATE')
        Whether = Whether.sort_index()
        Whether = Whether[Start_Date:End_Date] #Put User Start Date And End Date To The Dataset
        Whether['RAIN'] = Whether['RAIN'].apply(lambda x:convert_bool_to_int(x)) #def Conver_Bool_To_Int (Down In this page). Changes From bool (true/false) To 0 or 1 (int)
        Whether = Whether.reset_index()   
        Whether = Whether.rename(columns = {'DATE' : 'Date'}) #Rename From DATE to Date (capslock off)
        Whether['Date'] = Whether['Date'].astype(str) #Change the Date to string.

        #Error Message Every Time The DataSet Can't Show You Something
        if End_Date < pd.to_datetime('2004-01-01'):
            chart = 'static\\Images\\WRONG.jpg'
        elif Start_Date < pd.to_datetime('2004-01-01'):
            chart = 'static\\Images\\WRONG.jpg'
        elif Start_Date > End_Date:
            chart = 'static\\Images\\WRONG2.jpg'
        elif End_Date > pd.to_datetime('2017-12-14'):
            chart = 'static\\Images\\WRONG.jpg'

        else:
            dfMerged = pd.merge(Whether , Car , on = 'Date') #Merge the 2 Datasets.
            dfMerged = dfMerged.set_index('Date')
            dfMerged = dfMerged.rename(columns = {0 : 'Accidents'}) #Rename Colums

        if len(dfMerged) > 12: #If More Thank The Graph can read
            dfMerged.index = pd.to_datetime(dfMerged.index)
            s = dfMerged['Accidents']
            s = s.resample('M').mean() #average for Car.csv by Month
            dfnew = s.to_frame()
            v = dfMerged['RAIN']
            v = v.resample('M').mean() #Average For Whether.csv by Month
            dfnew1 = v.to_frame()
            dfnew['RAIN'] = dfnew1['RAIN']
            dfnew = dfnew.reset_index()
            dfnew['Date'] = dfnew['Date'].astype(str)
            dfnew = dfnew.set_index('Date')
            fig, ax1 = plt.subplots(figsize=(15, 10))
            dfnew['RAIN'].plot(kind='bar', color='blue') #did The Graph
            dfnew['Accidents'].plot(kind='line', color='orange', secondary_y=True) #Secondary y
            chart = plt_to_img(fig) #The Def Plt_to_Img (Down This Page)
        else:
            fig, ax1 = plt.subplots(figsize=(15, 10)) #graph fig sizes.
            dfMerged['RAIN'].plot(kind='bar', color='blue') #did The Graph
            dfMerged['Accidents'].plot(kind='line', color='orange', secondary_y=True) #Secondary y
            chart = plt_to_img(fig) #The Def Plt_to_Img (Down This Page)

    return render_template(
        'Dataquery.html', 
        form=form, 
        chart=chart,
        title='This Is My DataQuery Page, Please Enter A Start Date And End Date:',
        message='Please Enter A Date Between 01/01/2004 - 14/12/2017: (If You Put More Than 12 Days Diff, You Will See The Average Of Every Month)',
        year=datetime.now().year,
    )



def plt_to_img(fig):
    """Def that Changes The Plot To Image And Then To You Can See The Graph"""
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String


def convert_bool_to_int(s):
    """Def that Changes From False To 0 and True To 1"""
    if s == False:
        return 0
    else:
        return 1

app.config['SECRET_KEY'] = 'For PA' #For Python AnyWhere