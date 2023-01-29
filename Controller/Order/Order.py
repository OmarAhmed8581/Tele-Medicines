from flask import render_template,request,session,g,flash,Flask,redirect,url_for
from Controller import Configure
import pyrebase
from datetime import datetime

firebase = pyrebase.initialize_app(Configure.firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

def delete_temp_order():
    try:
        db.child("Temp_Order").remove()
        return True
    except:
        return False
#--------------------Sorted date ho ri hey

def sorted_Expire_date(array):
    array.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
    return array


def Order_list(Order_list):

    Product_list = []
    Order_list = Order_list.split(',')
    count = 0
    length = int(len(Order_list) / 3)

    for i in range(0, length):
        product = []
        for j in range(0, 3):
            product.append(Order_list[count])
            count = count + 1

        Product_list.append(product)

    return Product_list,length


def order(product_id,quantity,prices):
    try:
        data={
            "product id":str(product_id),
            "quantity":str(quantity) ,
            "price":str(int(prices)*int(quantity))

        }

        db.child('Temp_Order').push(data)


        return True
    except:
        return False

def Order_info(customer_id,employee_id,total_price,time,date,status):
    try:
        data={

            'Customer_id':str(customer_id),
            'Employee_id':str(employee_id),
            'Total_price':str(total_price),
            'Time':str(time),
            'Date':str(date),
            'Status':str(status)
           
            
        }
        print(data)
        db.child('Order').push(data)
        return True
    except:
        return False