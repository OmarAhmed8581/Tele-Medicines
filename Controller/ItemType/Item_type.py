from flask import render_template,request,session,g,flash,Flask,redirect,url_for
from Controller import Configure
import pyrebase

firebase = pyrebase.initialize_app(Configure.firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()


def Item_type_info(item_id,name,stock_id):
    try:
        data={
            'Item_id':str(item_id),
            'Name':str(name),
            'Stock_id':str(stock_id)
           
            
        }
        print(data)
        db.child('Item_type').push(data)
        return True
    except:
        return False



def product_type_update(name,id):
    try:
        data = {
            'Product Type': name,

        }
        db.child("Item Type").child(id).update(data)
        return True
    except:
        return False


# <--------------------------- Get Product Type id ------------------------------>

def item_type_id(data_result,name):
    try:

        item_id=""
        for k, (key, value) in enumerate(data_result.items()):
            if value["Product Type"] == name:
                item_id=key

                break


        return item_id
    except:
        return 0


