#<----------- Import File -------------->

from Controller import  Configure
import pyrebase
#<-------------------------------------->

# <--------------   FireBase Initiailzation ----------------------->

firebase = pyrebase.initialize_app(Configure.firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

#<-------------------------------------------------------------------->

def a(email1,password):
    admin_session_id = auth.create_user_with_email_and_password(email1, password)
    data={
        "email":str(email1),
        "password":str(password)
    }
    db.child('Admin').child(admin_session_id['localId']).push(data)


if __name__ == '__main__':
    a("admin",password="admin")