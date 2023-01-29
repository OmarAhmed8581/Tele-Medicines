from flask import render_template,request,session,g,flash,Flask,redirect,url_for
from Controller import Configure
import pyrebase


firebaseConfig = {
    "apiKey": "AIzaSyAAZSDa4A3ytc-QbeIYCV86QPzlexS2HOg",
    "authDomain": "telemedicines-123c0.firebaseapp.com",
    "databaseURL": "https://telemedicines-123c0.firebaseio.com",
    "projectId": "telemedicines-123c0",
    "storageBucket": "telemedicines-123c0.appspot.com",
    "messagingSenderId": "490806536805",
    "appId": "1:490806536805:web:73a3b462b3e52df8c5748c",
    "measurementId": "G-QPEMY0KWSQ"
  }

def connect_firebase():
# add a way to encrypt those, I'm a starter myself and don't know how
    username: "telemedicinefyp@gmail.com"
    password: "telemedicinefyp123"

    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth() 

    #authenticate a user > descobrir como não deixar hardcoded
    user = auth.sign_in_with_email_and_password(username, password)

    #user['idToken']
    # At pyrebase's git the author said the token expires every 1 hour, so it's needed to refresh it
    user = auth.refresh(user['refreshToken'])

    #set database
    db = firebase.database()

    return db