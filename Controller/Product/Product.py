from flask import render_template,request,session,g,flash,Flask,redirect,url_for
from Controller import Configure
import pyrebase

firebase = pyrebase.initialize_app(Configure.firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()


def product_type_id(product_type_result,product_name):
    try:
        item_id = ""
        for k, (key, value) in enumerate(product_type_result.items()):
            if value["Product Type"] == product_name:
                item_id = key

                break


        return  item_id
    except:
        print("false")


def get_product_id(product_type_result,product_name):
    try:
        item_id = ""
        for k, (key, value) in enumerate(product_type_result.items()):
            if value["Name"] == product_name:
                item_id = key

                break


        return  item_id
    except:
        print("false")


def Product_info(name,formula,description,item_id):



    try:
        data={
            'Name':str(name),
            'Formula':str(formula),
            'Description': str(description),
            "Item type id":str(item_id)
        }

        print(data)
        db.child('Product').push(data)
        return True
    except:
        return False

 #<< ============  Insert Product Type Data  ================ >>



def product_type(product_name):


    try:
        data={
            "Product Type":str(product_name)
        }
        db.child("Item Type").push(data)

        return  True

    except:
        return  False

def get_product_discription(result,name):
    try:
        description = ""
        product_id=""
        for k, (key, value) in enumerate(result.items()):
            if value["Name"] == name:
                description = value["Description"]
                product_id=key

                break


        return  description,product_id
    except:
        print("false")


#<========================= update product Quantity =====================

def update_product_quantity(id,quantity):
    try:
        data={
            "quantity":quantity
        }
        db.child("Product Quantity").child(id).update(data)



        return  True
    except:
        return False


#<------------------------------- Update Product --------------------------------->


def update_product(name,formular,id):
    try:
        data = {
            'Name': name,
            'Formula': formular,
        }
        db.child("Product").child(id).update(data)
        return True
    except:
        return False



#<---------------------------------------------------------------------------------->