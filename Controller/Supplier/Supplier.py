from flask import render_template,request,session,g,flash,Flask,redirect,url_for
from Controller import Configure
import pyrebase

firebase = pyrebase.initialize_app(Configure.firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()


def supplier_info(name,emp_id,company_name,address,phone,status,email,ages):
    try:
        data={
            'Supplier_Name':str(name),
            'Employee_id':str(emp_id),
            'Company_name':str(company_name),
            'Address':str(address),
            'Phone':str(phone),
            'Status':str(status),
            'Email':str(email),
            'Age': str(ages)
            
        }
        print(data)
        db.child('Supplier').push(data)
        return True
    except:
        return False

def get_supplier_id(supplier_result,name):
    try:
        supplier_id = ""
        for k, (key, value) in enumerate(supplier_result.items()):
            if value["Company_name"] == name:
                supplier_id = key

                break

        return supplier_id

    except:
        print("false")


def get_supplier_information(emp_result,user_id):
    try:
        name=""
        phone=""
        address=""
        status=""
        age=""
        supplier_name=""
        email=""
        employee_id=""

        for k, (key, value) in enumerate(emp_result.items()):

            if key == user_id:
                name = value["Company_name"]
                phone=value["Phone"]
                address=value["Address"]
                status=value["Status"]
                age=value["Age"]
                supplier_name=value["Supplier_Name"]
               
                email=value["Email"]

        return name,phone,address,status,age,supplier_name,email

    except:
        return False

# <------------------------- Update Supplier ---------------------------------------------------->

def update_supplier(user_id,data):
    try:
        db.child("Supplier").child(user_id).update(data)
        return True
    except:
        return False