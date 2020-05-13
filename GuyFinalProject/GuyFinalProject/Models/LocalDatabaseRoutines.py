from os import path
import json
import pandas as pd
#--------------------#


def create_LocalDatabaseServiceRoutines():
    return LocalDatabaseServiceRoutines()


class LocalDatabaseServiceRoutines(object):
    def __init__(self):
        self.name = 'Data base service routines'
        self.index = {}
        self.UsersDataFile = path.join(path.dirname(__file__), '..\\static\\Data\\users.csv')

    #Read User Data
    def ReadCSVUsersDB(self):
        df = pd.read_csv(self.UsersDataFile)
        return df

    #Write The Csv User Data
    def WriteCSVToFile_users(self, df):
        df.to_csv(self.UsersDataFile, index=False)

    #Find Is User Exist
    def IsUserExist(self, UserName):
        df = self.ReadCSVUsersDB()
        df = df.set_index('username')
        return (UserName in df.index.values)

    #Try If The Login Is Good
    def IsLoginGood(self, UserName, Password):
        df = self.ReadCSVUsersDB()
        df=df.reset_index()
        selection = [UserName]
        df = df[pd.DataFrame(df.username.tolist()).isin(selection).any(1)]
        df = df.set_index('password')
        return (Password in df.index.values)
     
    #Add New User
    def AddNewUser(self, User):
        df = self.ReadCSVUsersDB()
        dfNew = pd.DataFrame([[User.FirstName.data, User.LastName.data, User.PhoneNum.data, User.EmailAddr.data, User.username.data, User.password.data]], columns=['FirstName', 'LastName', 'PhoneNum', 'EmailAddr',  'username', 'password'])
        dfComplete = df.append(dfNew, ignore_index=True)
        self.WriteCSVToFile_users(dfComplete)