from flask import render_template,request,session,g,flash,Flask,redirect,url_for
from Controller import Configure
import pyrebase

firebase = pyrebase.initialize_app(Configure.firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()


def stock_info(product_id,Item_type_id):
    try:
        data={

            'Product_id':str(product_id),
            'Item_type_id':str(Item_type_id)
            
        }
        print(data)
        db.child('Stock').push(data)
        return True
    except:

        return False

def update_sell_price(stock_result,stock_id,Sell_Price,Expire_Date):
    try:
        for k, (key, value) in enumerate(stock_result.items()):
            if key==stock_id:
                data = {
                    "Sell price": str(Sell_Price),
                    "expire_date": str(Expire_Date)
                }
                db.child("Stock").child(key).update(data)

        return True
    except:

        return False


def product_quantity(product_id,sell_price,Quantity):
    result=db.child("Product Quantity").get().val()
    flat=False
    if result!=None:
        for k, (key, value) in enumerate(result.items()):
            if product_id == value['product id']:
                q=value["quantity"]
                q=int(q)+int(Quantity)
                data={
                    "Sell price":str(sell_price),
                    "quantity":str(q)

                }
                db.child("Product Quantity").child(key).update(data)
                flat=True
                break
        if flat==False:
            data = {
                "product id":str(product_id),
                "Sell price": str(sell_price),
                "quantity": str(Quantity)

            }
            db.child("Product Quantity").push(data)
        return  True
    else:
        data = {
            "product id": str(product_id),
            "Sell price": str(sell_price),
            "quantity": str(Quantity)
        }
        db.child("Product Quantity").push(data)
        return True


def get_product_id(stock_result,stock_id):
    product_id=""
    quantity=""
    for k, (key, value) in enumerate(stock_result.items()):
        if stock_id==key:
            product_id=value["product_id"]
            quantity=value["Quantity"]
            return product_id,quantity