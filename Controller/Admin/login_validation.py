

#<----------- Import File -------------->

from Controller import  Configure
from Controller import  libraries

#<-------------------------------------->


# <--------------   FireBase Initiailzation ----------------------->

firebase = libraries.pyrebase.initialize_app(Configure.firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()


#<---------------------------------- Get local id from admin database --------------------------------------------->

def Admin_local_id(local_id):
    result=db.child("Admin").child(local_id).get().val()

    if result!=None:
        for d3,(key,value) in enumerate(result.items()):
            admin_id=key
            admin_email=db.child("Admin").child(local_id).child(admin_id).get().val()
            return admin_id,admin_email["email"]
    else:
        return None

