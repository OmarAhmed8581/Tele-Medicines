from flask import render_template,request,session,g,flash,Flask,redirect,url_for
from Controller import Configure
import pyrebase

firebase = pyrebase.initialize_app(Configure.firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()


def Order_detail_info(order_detail_id,product_id,quantity,each_price):
    try:
        data={
            'order_detail_id':str(order_detail_id),
            'product_id':str(product_id),
            'Quantity':str(quantity),
            'each_price':str(each_price),
            
            
        }
        print(data)
        db.child('Order Details').push(data)
        return True
    except:
        return False