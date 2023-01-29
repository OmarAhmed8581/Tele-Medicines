from flask import render_template,request,session,g,flash,Flask,redirect,url_for
from Controller import Configure
import pyrebase

firebase = pyrebase.initialize_app(Configure.firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()


def Item_invoicing_info(invoice_id,supplier_id,quantity,arrived_date,arrived_time):
    try:
        data={
            'Invoice_id':str(invoice_id),
            'Supplier_id':str(supplier_id),
            'Quantity':str(quantity),
            'Arrived_date':str(arrived_date),
            'Arrived_time':str(arrived_time),
            
        }
        print(data)
        db.child('Item_invoicing').push(data)
        return True
    except:
        return False