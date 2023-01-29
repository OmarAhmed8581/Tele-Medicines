from flask import *
from Controller import Configure
import pyrebase
from collections import OrderedDict
import socket
import collections
import os
import re

firebase = pyrebase.initialize_app(Configure.firebaseConfig)
auth = firebase.auth()
db = firebase.database()
app = Flask(__name__)



from Controller.Customer import Customer_data
from Controller.Employee import Employee_data
from Controller.Stock import Stock
from Controller.Supplier import Supplier
from Controller.Item_invoicing import Item_invoice
from Controller.ItemType import Item_type
from Controller.Order import Order
from Controller.Order_detail import Order_detail
from Controller.Product import Product
from Controller.Admin import  login_validation
from Controller.Session import  Session


#<========================================  Login File ===============================================================================>
@app.route("/")
def login():
    return render_template("index.html")



@app.route("/get_login", methods=['GET', 'POST'])
def get_login():

    # <--------------------------------------------- Get email and password from user form ----------------------------------------->
    email = request.args.get('email')
    password = request.args.get('password')


    #<------------------------------------------------- SPACING REMOVE -------------------------------------------------------------->

    email = email.strip()
    password = password.strip()


    #<-------------------------------------------------- Create Session --------------------------------------------------------------->

    session.pop('uid', None)
    user = auth.sign_in_with_email_and_password(email, password)

    session_id = user['idToken']
    session['uid'] = str(session_id)


    # <----------------------------------------------   Get local id form admin and employees ----------------------------------------->

    idtoken = session['uid']
    local_id = Session.get_local_id(idtoken)
    admin_id = login_validation.Admin_local_id(local_id)
    emp_name, emp_id = Employee_data.employees_Name(local_id)


    #<------------------------------------------- Verify a local id from condition  ------------------------------------------------------->
    if admin_id!=None:
        return redirect(url_for("loader"))

    elif emp_id!=None:
        return redirect(url_for("emp_loader"))

    return redirect(url_for("loader"))




#<==============================   Admin Flow =======================================================================>


@app.route("/Analysics")
def analysics():
    return render_template("Admin/Analysics.html",menu="analysics",title="Analysics")



@app.route("/Admin_dashboard")
def dashboard():
    try:

        # <-------------------------------------------- Get local id from session ------------------------------------------------------>

        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id,admin_email = login_validation.Admin_local_id(local_id)
        print(admin_email)


        # <--------------------------------------------- Get Admin Email by local id ----------------------------------------------------->



        #<----------------------------------- Get Customer Information from database  and reverse data ------------------------------------------->

        result_c = db.child("Customer").get().val()  # fetch
        dreversed_c = OrderedDict()

        if result_c != None:

            # <------------------------- Reverse data -------------------------------------------->

            for k in reversed(result_c):
                dreversed_c[k] = result_c[k]

        # <----------------------------------- Get Employees Information from database  and reverse data ------------------------------------------->

        emp_result = db.child("Employee").get().val()
        dreversed = OrderedDict()


        if emp_result != None:

            emp_r={}

            for d3,(key,value) in enumerate(emp_result.items()):
                for d4,(k,v)  in enumerate(value.items()):
                    emp_r[k]=v

            #<------------------------- Convert Order dict -------------------------------------->

            emp_r=collections.OrderedDict(emp_r)

            #<------------------------- Reverse data -------------------------------------------->

            for k in reversed(emp_r):
                dreversed[k] = emp_r[k]


        #<------------------------------------------- Error handling using if condition  --------------------------------------------------------->


        if result_c == None and emp_result == None:
            dreversed = {}
            dreversed_c = {}
            return render_template("Admin/dashboard.html", customer_view=dreversed_c, employees_view=dreversed,email=admin_email,menu="home",title="Admin Dashboard")

        elif result_c == None:
            dreversed_c = {}
            return render_template("Admin/dashboard.html", customer_view=dreversed_c, employees_view=dreversed,email=admin_email,menu="home",title="Admin Dashboard")
        elif emp_result == None:
            dreversed = {}
            return render_template("Admin/dashboard.html", customer_view=dreversed_c, employees_view=dreversed,email=admin_email,menu="home",title="Admin Dashboard")

        return render_template("Admin/dashboard.html", customer_view=dreversed_c, employees_view=dreversed,email=admin_email,menu="home",title="Admin Dashboard")
    except:
        return  redirect(url_for("adminLogin"))


@app.route("/loader")
def loader():
    return render_template("Admin/Loader.html")


# <======== View File ==================>




@app.route("/area")
def Add_area():

    try:
    
        # <-------------------------------------------- Get local id from session --------------------------------------------------------------->

        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id,admin_email = login_validation.Admin_local_id(local_id)

        #<-------------------------------------------------- Get value form customer form -------------------------------------------------------->

        result=db.child("area").get().val();
        if result==None:
            result={}
            return render_template("Admin/Add_Area.html",menu="area",title="Add Area",area_data=result,count=len(result))


        return render_template("Admin/Add_Area.html",menu="area",title="Add Area",area_data=result,count=len(result))
    except:
        return  redirect(url_for("adminLogin"))



@app.route("/get_area",methods=['GET', 'POST'])
def get_area():

    try:
    
        # <-------------------------------------------- Get local id from session --------------------------------------------------------------->

        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id,admin_email = login_validation.Admin_local_id(local_id)


        name=request.form.get("area_names")

        if name!=None:
            data={
                "name":str(name)
            }
            db.child("area").push(data)

        result=db.child("area").get().val();
        if result==None:
            result={}
            return render_template("Admin/Add_Area.html",menu="area",title="Add Area",area_data=result,count=len(result))


        return render_template("Admin/Add_Area.html",menu="area",title="Add Area",area_data=result,count=len(result))
    except:
        return  redirect(url_for("adminLogin"))

        
@app.route("/area_update",methods=['GET', 'POST'])
def area_update():
    try:

    # <-------------------------------------------- Get local id from session --------------------------------------------------------------->

        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id,admin_email = login_validation.Admin_local_id(local_id)

        id=request.form.get("areaID")
        name=request.form.get("area_name")

        if name!=None and id!=None:
            data={
                "name":str(name)
            }
            db.child("area").child(id).update(data)

        result=db.child("area").get().val();
        if result==None:
            result={}
            return render_template("Admin/Add_Area.html",menu="area",title="Add Area",area_data=result,count=len(result))


        return render_template("Admin/Add_Area.html",menu="area",title="Add Area",area_data=result,count=len(result))
    except:
        return  redirect(url_for("adminLogin"))

@app.route("/customer_info_update" , methods=['GET', 'POST'])
def customer_info_update1():
    try:
        # <-------------------------------------------- Get local id from session --------------------------------------------------------------->

        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id,admin_email = login_validation.Admin_local_id(local_id)

        #<-------------------------------------------------- Get value form customer form -------------------------------------------------------->

        user_data = db.child("Customer").get().val()
        name=request.form.get('user_name')
        age=request.form.get('Age')
        C_NIC=request.form.get('NIC')
        phone=request.form.get('Phone')
        address=request.form.get('address')


        #<----------------------------------------------------- Update a Customer Data  ------------------------------------------------------------->

        update=Customer_data.update_customer_data(user_data,C_NIC,name,age,phone,address)


        result = db.child("Customer").get().val()
        name, nic, phone, address, gender, ages = Customer_data.get_customer_information(result, C_NIC)

        nic = request.form.get('nic')
        result1 = db.child("Order").get().val()
        custid = Customer_data.get_customerid(result, C_NIC)
        print("customer id", custid)
        record_list = Customer_data.get_customer_order_information(result1, custid)

        result2 = db.child("order detail").get().val()
        print(record_list)
        if result1 == None:
            result1 = {}

            return render_template("Admin/customer_info_display.html", name=name, nic=C_NIC, phone=phone, address=address,
                                   gender=gender, ages=ages, record_list=record_list, order=result1, custid=custid,
                                   order_detail=result2,menu="customer",title="Customer Data")

        return render_template("Admin/customer_info_display.html", name=name, nic=C_NIC, phone=phone, address=address,
                               gender=gender, ages=ages, record_list=record_list, order=result1, custid=custid,
                               order_detail=result2,menu="customer",title="Customer Data")
    except:
        return redirect(url_for("adminLogin"))





@app.route("/customer_display")
def customer_display():

    try:
        # <-------------------------------------------- Get local id from session --------------------------------------------------------------->

        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id,admin_email = login_validation.Admin_local_id(local_id)

        # <-------------------------------------------- Get NIC from URL --------------------------------------------------------------->

        C_NIC = request.args.get('nic')
        print(C_NIC)

        # <-------------------------------------------- Remove spacing --------------------------------------------------------------->

        if C_NIC != None:
            C_NIC = re.sub(r"^\s+", "", C_NIC)
        else:
            C_NIC=request.form.get('NIC')
            print("update",C_NIC)

        # <-------------------------------------------- Get Customer from Customer table  --------------------------------------------------------------->

        result = db.child("Customer").get().val()

        # <------------------------------------ Get Specific customer get  from COntroller  ( Customer ) --------------------------------------------------------------->

        name, nic, phone, address, gender, ages = Customer_data.get_customer_information(result, C_NIC)
        
        

        nic=request.form.get('nic')
        result1 = db.child("Order").get().val()
        custid=Customer_data.get_customerid(result,C_NIC)
        print("customer id",custid)
        record_list = Customer_data.get_customer_order_information(result1, custid)

        result2=db.child("order detail").get().val()
        print(record_list)
        if result1 == None:

            result1={}



            return render_template("Admin/customer_info_display.html", name=name, nic=C_NIC, phone=phone, address=address,
                               gender=gender, ages=ages,record_list=record_list,order=result1,custid=custid,order_detail=result2,email=admin_email,menu="customer",title="Customer Display")



        return render_template("Admin/customer_info_display.html", name=name, nic=C_NIC, phone=phone, address=address,
                               gender=gender, ages=ages,record_list=record_list,order=result1,custid=custid,order_detail=result2,email=admin_email,menu="customer",title="Customer Display")

    except:
        return redirect(url_for("adminLogin"))




@app.route("/employees_update_data",methods=['GET', 'POST'])
def employees_update():
    try:

        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id = login_validation.Admin_local_id(local_id)

        user_data = db.child("Employee").get().val()
        name = request.form.get('user_name')
        age = request.form.get('Age')
        C_NIC = request.form.get('NIC')
        phone = request.form.get('Phone')
        address = request.form.get('address')
        salary = request.form.get('Salary')
        time = request.form.get('Timing')

        update=Employee_data.Employees_update_data(user_data,C_NIC,name,address,phone,salary,time,age)

        result = db.child("Employee").get().val()

        name, nic, phone, address, gender, ages, salary, date, time = Employee_data.get_employees_information(result, C_NIC)

        return render_template("Admin/Employees_info_display.html", name=name, nic=nic, phone=phone, address=address,
                               gender=gender,
                               ages=ages, salary=salary, date=date, time=time,
                               menu="employee", title = "Employee Display"
                               )

    except:
        return redirect(url_for("adminLogin"))


@app.route("/employees_display")
def employees_display():
    try:
        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id,admin_email = login_validation.Admin_local_id(local_id)

        C_NIC = request.args.get('nic')
        C_NIC = re.sub(r"^\s+", "", C_NIC)

        result = db.child("Employee").get().val()

        name, nic, phone, address, gender, ages, salary, date, time = Employee_data.get_employees_information(result, C_NIC)



        return render_template("Admin/Employees_info_display.html", name=name, nic=nic, phone=phone, address=address,
                               gender=gender,
                               ages=ages, salary=salary, date=date, time=time,email=admin_email,menu="employee",title="Employees Information")
    except:
        return redirect(url_for("adminLogin"))

@app.route("/employees_info")
def employees_info():

    try:
        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id,admin_email = login_validation.Admin_local_id(local_id)

        return render_template("Admin/Employees_info.html",email=admin_email,menu="employee",title="Employees Add")
    except:
        return redirect(url_for("adminLogin"))


@app.route("/supplier_display")
def supplier_display():
    try:
        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id = login_validation.Admin_local_id(local_id)

        user_id = request.args.get('user_id')
        user_id = re.sub(r"^\s+", "", user_id)

        result = db.child("Supplier").get().val()
        companyname, phone, address, status, age, supplier_name, email = Supplier.get_supplier_information(result,
                                                                                                           user_id)
        product_result=db.child("Product").get().val()
        supplier_result=db.child("Supplier").get().val()
        Stock_result=db.child("Stock").get().val()

        print(companyname)

        return render_template("Admin/supplier_info_display.html", companyname=companyname, phone=phone, address=address,
                               status=status,
                                   age=age, supplier_name=supplier_name, email=email,product_result=product_result,supplier_result=supplier_result,Stock_result=Stock_result,id=user_id
                               , menu="supplier", title="Supplier Display"
                               )
    except:
        return redirect(url_for("adminLogin"))

@app.route("/supplier_update_data",methods=["GET","POST"])
def supplier_update_data():
    name = request.form.get('user_name')
    age = request.form.get('Age')
    user_id = request.form.get('user_id')
    phone = request.form.get('Phone')

    address = request.form.get('address')

    data={
        "Address":address,
        "Age":age,
        "Phone":phone,
        "Supplier_Name":name
    }
    result=Supplier.update_supplier(user_id,data)
    print(data)
    print(result)

    if result==True:
        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id = login_validation.Admin_local_id(local_id)

        result = db.child("Supplier").get().val()
        companyname, phone, address, status, age, supplier_name, email = Supplier.get_supplier_information(result,
                                                                                                           user_id)
        product_result = db.child("Product").get().val()
        supplier_result = db.child("Supplier").get().val()
        Stock_result = db.child("Stock").get().val()

        print(companyname)
        return render_template("Admin/supplier_info_display.html", companyname=companyname, phone=phone,
                               address=address,
                               status=status,
                               age=age, supplier_name=supplier_name, email=email, product_result=product_result,
                               supplier_result=supplier_result, Stock_result=Stock_result, id=user_id
                               , menu="supplier", title="Supplier Display"
                               )


@app.route("/Supplier_info")
def Supplier_info():
    return render_template("Admin/Supplier_info.html", menu="supplier", title="Supplier Information")


@app.route("/Supplier_info_display")
def Supplier_info_diplay():
    return render_template("Admin/supplier_info_display.html", menu="supplier", title="Supplier display")


@app.route("/Customer_view")
def customer_view():

    try:
        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id,admin_email = login_validation.Admin_local_id(local_id)

        index = 0
        result = db.child("Customer").get().val()
        dreversed = OrderedDict()
        if result != None:

            for k in reversed(result):
                dreversed[k] = result[k]

        print(result)
        print(dreversed)
        # for key, value in result.items():
        #    print(value)
        #
        # print(dict)
        if result == None:
            # Customer nae hai DB me
            result = {}

            return render_template("Admin/Customer_view.html", dict=result, index=index,email=admin_email
                                   , menu="customer", title="customer view",search='search'
                                   )

        return render_template("Admin/Customer_view.html", dict=dreversed, index=index,email=admin_email, menu="customer", title="customer view",search='search')
    except:
        return redirect(url_for("adminLogin"))


@app.route("/Employees_view")
def employees_view():

    try:
        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id,admin_email = login_validation.Admin_local_id(local_id)



        # Employee view
        index = 0
        emp_result = db.child("Employee").get().val()

        if emp_result==None:
            emp_r={}
            return render_template("Admin/Employees_view.html", dict=emp_r, index=index,email=admin_email,menu="employee",title="Employees Views",search='search')

        dreversed = OrderedDict()

        emp_r = {}
        for d3, (key, value) in enumerate(emp_result.items()):
            for d4, (k, v) in enumerate(value.items()):
                emp_r[k] = v

        emp_r = collections.OrderedDict(emp_r)

        return render_template("Admin/Employees_view.html", dict=emp_r, index=index,email=admin_email,menu="employee",title="Employees Views",search='search')

    except:
        return redirect(url_for("adminLogin"))


@app.route("/Order_view")
def order_view():
    try:
        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id,admin_email = login_validation.Admin_local_id(local_id)


        result1 = db.child("Customer").get().val()

        result = db.child("Order").get().val()
        dreversed = OrderedDict()

        if result==None:
            return render_template("Admin/Order_view.html", order_view=dreversed, customer_name=result1,email=admin_email
                                   , menu="order", title="Order view",search='search')

        for k in reversed(result):
            dreversed[k] = result[k]

        return render_template("Admin/Order_view.html", order_view=dreversed, customer_name=result1,email=admin_email
                               , menu="order", title="Order view",search='search')
    except:
        return redirect(url_for("adminLogin"))

@app.route("/Online_Order_view")
def Online_order_view():
    try:
        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id,admin_email = login_validation.Admin_local_id(local_id)


        result1 = db.child("onlinecustomerdetails").get().val()

        result = db.child("onlineorder").get().val()
        dreversed = OrderedDict()

        if result==None:
            return render_template("Admin/Online_Order_view.html", order_view=dreversed, customer_name=result1,email=admin_email
                                   , menu="online_order", title="Online Order view",search='search')

        for k in reversed(result):
            dreversed[k] = result[k]

        return render_template("Admin/Online_Order_view.html", order_view=dreversed, customer_name=result1,email=admin_email
                               , menu="online_order", title="Online Order view",search='search')
    except:
        return redirect(url_for("adminLogin"))


@app.route("/Supplier_view")
def supplier_view():
    try:
        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id = login_validation.Admin_local_id(local_id)

        result = db.child("Supplier").get().val()
        dreversed = OrderedDict()

        if result==None:
            return render_template("Admin/Supplier_view.html", supplier_view=dreversed,
                                   menu="supplier", title="Supplier view",search='search')

        for k in reversed(result):
            dreversed[k] = result[k]

        return render_template("Admin/Supplier_view.html", supplier_view=dreversed
                               ,
                               menu="supplier", title="Supplier view",search='search'
                               )

    except:
        return redirect(url_for("adminLogin"))

@app.route("/product_view")
def product_view():

    try:
        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id = login_validation.Admin_local_id(local_id)

        product_result = db.child("Product").get().val()
        product_type= db.child("Item Type").get().val()
        Product_Quantity = db.child("Product Quantity").get().val()


        dreversed = OrderedDict()
        if product_result==None:
            dreversed={}
            return render_template("Admin/Product_view.html", product_list=dreversed,product_type=product_type
                                   ,
                                   menu="product", title="Product view",search='search'
                                   )


        for k in reversed(product_result):
            dreversed[k] = product_result[k]


        if Product_Quantity==None:

            return render_template("Admin/Product_view.html", product_list=dreversed, product_type=product_type
                                   ,
                                   menu="product", title="Product view",search='search'
                                   )






        return render_template("Admin/Product_view.html",product_list=dreversed,product_type=product_type,Product_Quantity=Product_Quantity
                               ,menu="product", title="Product view",search='search'
                               )
    except:
        return redirect(url_for("adminLogin"))


@app.route("/product_type")
def product_type():


    product_type_result = db.child("Item Type").get().val()

    return render_template("Admin/Product_type.html", Item=product_type_result,menu="product", title="Product Type")


@app.route("/add_Order", methods=['GET', 'POST'])
def add_order():
    try:
        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id,admin_email = login_validation.Admin_local_id(local_id)

        C_Name = request.args.get('Customer_Name')
        C_NIC = request.args.get('NIC')

        C_Name = re.sub(r"^\s+", "", C_Name)
        C_NIC = re.sub(r"^\s+", "", C_NIC)
        # print("name"+a)

        product_type_result = db.child("Item Type").get().val()
        a = {}
        b = {}
        return render_template("Admin/Order_info.html", Item=product_type_result, order_detail=a, product=b, name=C_Name,
                               nic=C_NIC,email=admin_email,menu="order", title="Order Information")
    except:
        return redirect(url_for("adminLogin"))


@app.route("/adminLogin")
def adminLogin():

    session.pop('uid', None)

    return  redirect(url_for('login'))


@app.route("/customer_info")
def customer_infor():
    try:
        # <-------------------------------------------- Get local id from session ------------------------------------------------------>

        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id, admin_email = login_validation.Admin_local_id(local_id)
        print(admin_email)



        return render_template("Admin/Customer_info.html",email=admin_email
                               ,menu="customer", title="Customer Information")
    except:
        return redirect(url_for('login'))


# <======  End View file ==============>


#  <========== Add file ================>


@app.route("/add_customer", methods=['GET', 'POST'])
def customer_info_get():



    name = request.form.get("name")
    NIC = request.form.get("nic")
    phone_number = request.form.get("phone")
    age = request.form.get("age")
    gender = request.form.get("gender")
    address = request.form.get("address")

    method_call = Customer_data.customer_info(name, NIC, phone_number, age, gender, address,"None")
    if method_call == True:
        return redirect(url_for('customer_view'))
    else:
        flash("Customer data is not insert")
        return redirect(request.url)

    return redirect(url_for('customer_view'))


@app.route("/add_employee", methods=['GET', 'POST'])
def employee_info_get():


    empname = request.form.get("name")
    empphone = request.form.get("phone")
    empage = request.form.get("age")
    empemail = request.form.get("email")
    empgender = request.form.get("gender")
    empsalary = request.form.get("salary")
    empaddress = request.form.get("address")
    emptime = request.form.get("timing")
    empcnic = request.form.get("cnic")
    emppass=request.form.get("password")

    if empname != None and empphone != None and empage != None and empemail != None and empgender != None and empsalary != None and empaddress != None and emptime != None and empcnic != None and emppass!=None:

        method_call = Employee_data.employee_info(empname, empemail, empage, empphone, empgender, empaddress, empsalary,
                                                  emptime, empcnic,emppass)

        if method_call == True:
            print("Employee data inserted successfully!!")
        else:
            flash("Email is already Existed","warning")
            return redirect(url_for('employees_info'))

    return redirect(url_for('employees_view'))



@app.route("/add_product_type", methods=['GET', 'POST'])
def product_type_get():


    idtoken = session['uid']
    local_id = Session.get_local_id(idtoken)
    admin_id, admin_email = login_validation.Admin_local_id(local_id)
    print(admin_email)

    name = request.form.get("product type")
    result = Product.product_type(name)
    if result == True:

        product_type_result = db.child("Item Type").get().val()

        return render_template("Admin/Product_type.html", Item=product_type_result,email=admin_email
                               ,menu="product", title="Product Type")

    else:
        print("didn't Add product type ")


@app.route("/add_product", methods=['GET', 'POST'])
def product_get():


    idtoken = session['uid']
    local_id = Session.get_local_id(idtoken)
    admin_id, admin_email = login_validation.Admin_local_id(local_id)

    item_type = request.form.get("product type")


    name1 = request.form.get("name")
    name1=name1.capitalize()
    formular1 = request.form.get("Formular")
    discription1 = request.form.get("discription")

    product_type_result = db.child("Item Type").get().val()
    item_id = Product.product_type_id(product_type_result, item_type)

    product_result = Product.Product_info(name1, formular1, discription1,item_id)

    if product_result == True:
        product_result = db.child("Product").get().val()
        product_id = Product.get_product_id(product_result, name1)
        result = Stock.stock_info(product_id, item_id)
        if result == True:
            return render_template("Admin/Product_type.html", Item=product_type_result,email=admin_email,menu="product", title="Product Type")

    return render_template("Admin/Product_type.html", Item=product_type_result,email=admin_email
                           , menu="product", title="Product Type"
                           )


global count


@app.route("/add_order_value", methods=['GET', 'POST'])
def order_add():


    idtoken = session['uid']
    local_id = Session.get_local_id(idtoken)
    admin_id, admin_email = login_validation.Admin_local_id(local_id)

    user_result = db.child("Customer").get().val()

    name = request.form.get("product name")
    class_get = request.form.get("suggested table")

    if class_get != "Select Suggestion Medicine":
        name = class_get

    q = request.form.get("quantity")

    p = request.form.get("price")

    result = Customer_data.customer_id(user_result)
    product_result = db.child("Product").get().val()

    temp = False
    for d2, (key, value) in enumerate(product_result.items()):
        if value["Name"] == name:
            quantity_sug = value["Quantity"]
            quantity_sug = int(quantity_sug) - int(q)
            if quantity_sug < 0:
                print("limit exceed!!")
                temp = True
            # /print(quantity_sug)
            else:
                data = {
                    'Name': value["Name"],
                    'Formula': value["Formula"],
                    'Quantity': str(quantity_sug),
                    'Each_price': value["Each_price"],
                    'Date_of_expire': value["Date_of_expire"],
                    'Description': value["Description"],
                }
                print(key)
                db.child("Product").child(key).update(data)
    if temp == False:
        id = Product.get_product_id(product_result, name)
        result1 = Order.order(name, q, p)

        if result1 == True:
            product_detail = db.child("Temp_Order").get().val()

            product_type_result = db.child("Item Type").get().val()
            print(result)

            return render_template("Admin/Order_info.html", Item=product_type_result, order_detail=product_detail,
                                   product=product_result,email=admin_email
                                   , menu="order", title="Order information"
                                   )

    a = {}
    product_type_result = db.child("Item Type").get().val()
    print(result)
    return render_template("Admin/Order_info.html", Item=product_type_result, order_detail={}, product={}, count=0,email=admin_email
                           , menu="order", title="Order information"
                           )


@app.route("/add_to_cart")
def Add_cart():

    result=Order.delete_temp_order()
    if result==True:
        return  redirect(url_for("customer_view"))

    return redirect(url_for("customer_view"))


@app.route("/add_supplier", methods=['GET', 'POST'])
def add_supplier():
    name = request.form.get("name")
    company_name = request.form.get("company name")
    age = request.form.get("age")
    phone = request.form.get("phone")
    email = request.form.get("email")
    address = request.form.get("address")
    result = Supplier.supplier_info(name, None, company_name, address, phone, "offline", email, age)

    if result == True:
        return redirect(url_for("supplier_view"))

    return redirect(url_for("supplier_view"))

    


# <============ End Add ======================>

# Summary order display

@app.route("/summary")
def summary():


    idtoken = session['uid']
    local_id = Session.get_local_id(idtoken)
    admin_id,admin_email = login_validation.Admin_local_id(local_id)



    name=request.args.get('Cname')
    price=request.args.get('price')
    id=request.args.get('key')
    quantity=request.args.get('quantity')



    name = name.strip()
    price = price.strip()
    id = id.strip()
    quantity=quantity.strip()



    Order_list = request.args.get('Order_list')

    Product_list,Order_length=Order.Order_list(Order_list)

    product_result=db.child("Product").get().val()

    Stock_result = db.child("Stock").get().val()

#<-----------------   expri date comparision  ------------------------------------>
    for i1 in range(0,len(Product_list)):
        Expire_date=[]
        for d1,(key,value) in enumerate(product_result.items()):
            if value['Name']== Product_list[i1][0]:
                for d2, (stock_key, stock_value) in enumerate(Stock_result.items()):
                    if key == stock_value['product_id']:
                        if stock_value['expire_date'] != '0':
                            Expire_date.append(stock_value['expire_date'])

                Expire_date_sorted=Order.sorted_Expire_date(Expire_date)
                product_quantity =  Product_list[i1][1]
                product_quantity=int(product_quantity)

                while(product_quantity>0):
                    for i in range(0,len(Expire_date_sorted)):
                        for d3, (key1, value1) in enumerate(Stock_result.items()):
                            if key == value1['product_id']:
                                if value1['expire_date'] == Expire_date_sorted[i]:
                                    q=int(value1['Quantity'])
                                    if product_quantity<=q:
                                        q1=q-product_quantity
                                        product_quantity=0
                                        data={
                                            'Quantity':str(q1)
                                        }
                                        db.child("Stock").child(key1).update(data)
                                    else:

                                        q1=product_quantity-q
                                        product_quantity=q1

                                        data = {
                                            'Quantity': str(0)
                                        }
                                        db.child("Stock").child(key1).update(data)
                        if product_quantity==0:
                            break


    result=Product.update_product_quantity(id,quantity)

    temp_order = db.child("Temp_Order").get().val()




    return render_template("Admin/Summary_order.html",temp_order=temp_order,name=name,price=price
                           , menu="summary", title="Summary Order")




@app.route("/product_update",methods=['GET', 'POST'])
def product_update():


    idtoken = session['uid']
    local_id = Session.get_local_id(idtoken)
    admin_id,admin_email = login_validation.Admin_local_id(local_id)

    item_id = request.form.get('itemID')
    product_id = request.form.get('product_id')
    type_name = request.form.get('typeName')
    name = request.form.get('name')
    formular = request.form.get('formular')

    print(item_id)
    print(type_name)

    a=Item_type.product_type_update(type_name,item_id)
    b=Product.update_product(name,formular,product_id)

    product_result = db.child("Product").get().val()

    description, product_id = Product.get_product_discription(product_result, name)
    print(description)

    item_result = db.child("Item Type").get().val()
    item_id = Item_type.item_type_id(item_result, type_name)

    return render_template("Admin/product_display.html", type_name=type_name, name=name, formular=formular,
                           description=description, product_id=product_id, item_id=item_id,email=admin_email
                           , menu="product", title="Product display")


@app.route("/product_display")
def product_display():


    idtoken = session['uid']
    local_id = Session.get_local_id(idtoken)
    admin_id, admin_email = login_validation.Admin_local_id(local_id)


    type_name=request.args.get('item_name')
    name = request.args.get('name')
    formular = request.args.get('formular')


    type_name=type_name.strip()
    name = name.strip()
    formular = formular.strip()


    product_result = db.child("Product").get().val()

    description,product_id=Product.get_product_discription(product_result,name)
    print(description)

    item_result = db.child("Item Type").get().val()
    item_id=Item_type.item_type_id(item_result,type_name)



    return  render_template("Admin/product_display.html",type_name=type_name,name=name,formular=formular,description=description,product_id=product_id,item_id=item_id,email=admin_email
                            , menu="product", title="Product display")

@app.route("/Stock_view")
def stock_view():
    try:
        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id,admin_email = login_validation.Admin_local_id(local_id)

        product_result = db.child("Product").get().val()
        supplier_result = db.child("Supplier").get().val()
        stock_result = db.child("Stock").get().val()
        product_type= db.child("Item Type").get().val()
        if stock_result==None:
            product_result={}
            supplier_result={}
            stock_result={}
            product_type={}



        return  render_template("Admin/Stock_view.html",product_result=product_result,supplier_result=supplier_result,stock_result=stock_result,product_type=product_type,email=admin_email,
                                menu="stock", title="Stock view",search="search")
    except:
        return redirect(url_for('login'))


@app.route("/supplier_add_product")
def supplier_add_product():


    company_name = request.args.get('company_name')
    company_name = company_name.strip()

    supplier_result = db.child("Supplier").get().val()
    supplier_id=Supplier.get_supplier_id(supplier_result,company_name)

    product_type_result = db.child("Item Type").get().val()

    stock_result=db.child("Stock").get().val()

    dreversed = OrderedDict()
    if stock_result != None:

        for k in reversed(stock_result):
            dreversed[k] = stock_result[k]

    if stock_result==None:
        dreversed={}

    product_result = db.child("Product").get().val()

    return render_template("Admin/Supplier_add_product.html",company_name=company_name,Item=product_type_result,stock_item=dreversed,Supplier_id=supplier_id,product_result=product_result
                           ,menu="supplier", title="Supplier Add product"
                           )


@app.route("/supplier_arrived_product")
def supplier_arrived_product():

    try:

        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id = login_validation.Admin_local_id(local_id)

        company_name = request.args.get('company')
        company_name = company_name.strip()

        product_name = request.args.get('product_name')
        product_name = product_name.strip()

        company_price = request.args.get('company_price')
        company_price = company_price.strip()

        Quantity1 = request.args.get('Quantity1')
        Quantity1 = Quantity1.strip()

        stock_id= request.args.get('stock_id')
        stock_id = stock_id.strip()

        return render_template("Admin/Supplier_Arrived_product.html",company_name=company_name,product_name=product_name,company_price=company_price,Quantity1=Quantity1,stock_id=stock_id
                               ,menu="supplier", title="Supplier Arrived product")
    except:
        return redirect(url_for('login'))


@app.route("/supplier_add_stock",methods=['GET', 'POST'])
def supplier_add_stock():

    Sell_Price = request.args.get('sell_price')
    Sell_Price = Sell_Price.strip()

    Expire_Date = request.args.get('Expire_date')
    Expire_Date = Expire_Date.strip()

    id = request.args.get('id')
    id = id.strip()


    stock_result = db.child("Stock").get().val()


    a=Stock.update_sell_price(stock_result,id,Sell_Price,Expire_Date)
    product_id,quantity=Stock.get_product_id(stock_result,id)
    a1=Stock.product_quantity(product_id,Sell_Price,quantity)

    return redirect(url_for("supplier_view"))


@app.route("/Customer_order_display")
def Customer_order_display():

    try:

        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id,admin_email = login_validation.Admin_local_id(local_id)

        order_id = request.args.get('order_id')
        order_id = order_id.strip()

        customer_name = request.args.get('customer_name')
        customer_name = customer_name.strip()

        price = request.args.get('price')
        price = price.strip()

        customer_id = request.args.get('customer_id')
        customer_id = customer_id.strip()

        customer_detail=db.child("Customer").get().val()

        address=""
        phone=""
        for d1,(key,value) in enumerate(customer_detail.items()):
            if key==customer_id:
                address=value["address"]
                phone = value["phone_number"]





        order_detail=db.child("order detail").get().val()


        return render_template("Admin/Customer_Order_display.html",order_id=order_id,customer_name=customer_name,price=price,order_detail=order_detail,email=admin_email,
                               menu="customer", title="Customer Order display",address=address,phone=phone)
    except:
        return redirect(url_for('login'))



@app.route("/Customer_online_order_display")
def Customer_online_order_display():

    try:

        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id,admin_email = login_validation.Admin_local_id(local_id)

        order_id = request.args.get('order_id')
        order_id = order_id.strip()

        customer_name = request.args.get('customer_name')
        customer_name = customer_name.strip()

        price = request.args.get('price')
        price = price.strip()



        customer_id = request.args.get('customer_id')
        customer_id = customer_id.strip()

        customer_detail=db.child("onlinecustomerdetails").get().val()

        address=""
        phone=""
        age=""
        date=""
        for d1,(key,value) in enumerate(customer_detail.items()):
            if key==customer_id:
                address=value["address"]
                phone = value["phone_number"]
                date = value["date"]
                age=value["age"]








        order_detail=db.child("onlineorderdetail").get().val()


        return render_template("Admin/Customer_online_order_display.html",order_id=order_id,customer_name=customer_name,price=price,order_detail=order_detail,email=admin_email,date=date,age=age,
                               menu="customer", title="Customer Online Order display",address=address,phone=phone)
    except:
        return redirect(url_for('login'))


@app.route("/update_customer_deliver")
def update_customer_deliver():
    try:

        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        admin_id,admin_email = login_validation.Admin_local_id(local_id)

        order_id = request.args.get('order_id')
        order_id = order_id.strip()

        data={
            "status":"deliver"
        }
        db.child("onlineorder").child(order_id).update(data)

        return redirect(url_for('Online_order_view'))


    except:
        return redirect(url_for('login'))

#<==============================  End Admin Flow =======================================================================>



#<================================ Employees Flow ======================================================================>

@app.route("/emp_loader")
def emp_loader():
    return  render_template("Employee/loader.html")



@app.route("/Employee_dashboard_route")
def employee_dashboard():
    try:
        idtoken = session['uid']

        local_id = Session.get_local_id(idtoken)
        emp_name,emp_id = Employee_data.employees_Name(local_id)


        # print(emp_id)
        result_c = db.child("Customer").get().val()
        dreversed_c = OrderedDict()

        if result_c != None:

            for k in reversed(result_c):
                dreversed_c[k] = result_c[k]

        emp_result = db.child("Order").get().val()
        dreversed = OrderedDict()
        if emp_result != None:

            for k in reversed(emp_result):
                dreversed[k] = emp_result[k]
        order_detail=db.child("order detail").get().val()
        if result_c == None and emp_result == None:
            dreversed = {}
            dreversed_c = {}
            return render_template("Employee/Employee_dashboard.html", customer_view=dreversed_c, order=dreversed,emp_name=emp_name,emp_id=emp_id,order_detail=order_detail
                                   ,menu="home", title="Employee Dashboard")

        elif result_c == None:
            dreversed_c = {}
            return render_template("Employee/Employee_dashboard.html", customer_view=dreversed_c, order=dreversed,emp_name=emp_name,emp_id=emp_id,order_detail=order_detail
                                   ,menu="home", title="Employee Dashboard")
        elif emp_result == None:
            dreversed = {}
            return render_template("Employee/Employee_dashboard.html", customer_view=dreversed_c, order=dreversed,emp_name=emp_name,emp_id=emp_id,order_detail=order_detail
                                   ,menu="home", title="Employee Dashboard")

        return render_template("Employee/Employee_dashboard.html", customer_view=dreversed_c, order=dreversed,emp_name=emp_name,emp_id=emp_id,order_detail=order_detail
                               ,menu="home", title="Employee Dashboard")

    except:
        return redirect(url_for("logout"))





@app.route("/Emp_Customer_view")
def emp_customer_view():
    try:
        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        emp_name,emp_id = Employee_data.employees_Name(local_id)




        index = 0
        result = db.child("Customer").get().val()
        dreversed = OrderedDict()
        if result != None:

            for k in reversed(result):
                dreversed[k] = result[k]

        print(result)
        print(dreversed)

        if result == None:

            result = {}

            return render_template("Employee/emp_customer_view.html", dict=result, index=index,emp_name=emp_name,emp_id=emp_id
                                   ,menu="customer", title="Customer View",search="search")

        return render_template("Employee/emp_customer_view.html", dict=dreversed, index=index,emp_name=emp_name,emp_id=emp_id
                               ,menu="customer", title="Customer View",search="search")
    except:
        return redirect(url_for("logout"))


@app.route("/Emp_customer_add")
def emp_customer_add():
    try:
        print("a")
        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        emp_name, emp_id = Employee_data.employees_Name(local_id)

        return render_template("Employee/emp_customer_add.html",emp_name=emp_name
                               ,menu="customer", title="Customer Add")
    except:
        return redirect(url_for("logout"))



@app.route("/Emp_Order_view")
def emp_order_view():
    try:
        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        emp_name, emp_id = Employee_data.employees_Name(local_id)
        result1 = db.child("Customer").get().val();

        result = db.child("Order").get().val();
        dreversed = OrderedDict()

        for k in reversed(result):
            dreversed[k] = result[k]

         # return render_template("Admin/Order_view.html", order_view=dreversed, customer_name=result1)
        return render_template("Employee/emp_order_view.html",order_view=dreversed, customer_name=result1,emp_name=emp_name
                               ,menu="order", title="Order View",search="search")
    except:
        return redirect(url_for("logout"))


@app.route("/Emp_customer_get", methods=['GET', 'POST'])
def emp_customer_info_get():


    idtoken = session['uid']
    local_id = Session.get_local_id(idtoken)
    emp_name, emp_id = Employee_data.employees_Name(local_id)


    name = request.form.get("name")
    NIC = request.form.get("nic")
    phone_number = request.form.get("phone")
    age = request.form.get("age")
    gender = request.form.get("gender")
    address = request.form.get("address")



    method_call = Customer_data.customer_info(name, NIC, phone_number, age, gender, address,str(emp_id))
    if method_call == True:
        print("customer inserted successfully!!")
    else:
        print("customer inserted failed!")

    return redirect(url_for('emp_customer_view'))



@app.route("/emp_add_order", methods=['GET', 'POST'])
def emp_add_order():
    C_Name = request.args.get('Customer_Name')
    C_NIC = request.args.get('NIC')

    C_Name = re.sub(r"^\s+", "", C_Name)
    C_NIC = re.sub(r"^\s+", "", C_NIC)



    product_type_result = db.child("Item Type").get().val()
    a = {}
    b = {}
    return render_template("Employee/emp_order_info.html", Item=product_type_result, order_detail=a, product=b, name=C_Name,
                           nic=C_NIC
                           ,menu="order", title="Order Information")


@app.route("/emp_add_Order", methods=['GET', 'POST'])
def emp_add_order1():


    idtoken = session['uid']
    local_id = Session.get_local_id(idtoken)
    emp_name, emp_id = Employee_data.employees_Name(local_id)


    C_Name = request.args.get('Customer_Name')
    C_NIC = request.args.get('NIC')

    C_Name = re.sub(r"^\s+", "", C_Name)
    C_NIC = re.sub(r"^\s+", "", C_NIC)
    # print("name"+a)


    product_type_result = db.child("Item Type").get().val()
    a = {}
    b = {}
    return render_template("Employee/emp_order_info.html", Item=product_type_result, order_detail=a, product=b, name=C_Name,
                           nic=C_NIC,emp_id=emp_id
                           ,menu="order", title="Order Information")


@app.route("/emp_summary")
def emp_summary():
    name = request.args.get('Cname')
    price = request.args.get('price')
    id = request.args.get('key')
    quantity = request.args.get('quantity')

    name = name.strip()
    price = price.strip()
    id = id.strip()
    quantity = quantity.strip()

    Order_list = request.args.get('Order_list')

    Product_list, Order_length = Order.Order_list(Order_list)

    product_result = db.child("Product").get().val()

    Stock_result = db.child("Stock").get().val()

    for i1 in range(0, len(Product_list)):
        Expire_date = []
        for d1, (key, value) in enumerate(product_result.items()):
            if value['Name'] == Product_list[i1][0]:
                for d2, (stock_key, stock_value) in enumerate(Stock_result.items()):
                    if key == stock_value['product_id']:
                        if stock_value['expire_date'] != '0':
                            Expire_date.append(stock_value['expire_date'])

                Expire_date_sorted = Order.sorted_Expire_date(Expire_date)
                product_quantity = Product_list[i1][1]
                product_quantity = int(product_quantity)

                while (product_quantity > 0):
                    for i in range(0, len(Expire_date_sorted)):
                        for d3, (key1, value1) in enumerate(Stock_result.items()):
                            if key == value1['product_id']:
                                if value1['expire_date'] == Expire_date_sorted[i]:
                                    q = int(value1['Quantity'])
                                    if product_quantity <= q:
                                        q1 = q - product_quantity
                                        product_quantity = 0
                                        data = {
                                            'Quantity': str(q1)
                                        }
                                        db.child("Stock").child(key1).update(data)
                                    else:

                                        q1 = product_quantity - q
                                        product_quantity = q1

                                        data = {
                                            'Quantity': str(0)
                                        }
                                        db.child("Stock").child(key1).update(data)
                        if product_quantity == 0:
                            break

    result = Product.update_product_quantity(id, quantity)

    temp_order = db.child("Temp_Order").get().val()

    return render_template("Employee/emp_customer_summary.html", temp_order=temp_order, name=name, price=price
                           ,menu="summary", title="Customer Summary")


@app.route("/emp_customer_display")
def emp_customer_display():
    C_NIC = request.args.get('nic')
    print(C_NIC)
    if C_NIC != None:
        C_NIC = re.sub(r"^\s+", "", C_NIC)
    else:
        C_NIC = request.form.get('NIC')
        print("update", C_NIC)

    result = db.child("Customer").get().val()
    name, nic, phone, address, gender, ages = Customer_data.get_customer_information(result, C_NIC)

    nic = request.form.get('nic')
    result1 = db.child("Order").get().val()
    custid = Customer_data.get_customerid(result, C_NIC)
    print("customer id", custid)
    record_list = Customer_data.get_customer_order_information(result1, custid)

    result2 = db.child("order detail").get().val()
    print(record_list)
    if result1 == None:
        result1 = {}

        return render_template("Employee/emp_customer_display.html", name=name, nic=C_NIC, phone=phone, address=address,
                               gender=gender, ages=ages, record_list=record_list, order=result1, custid=custid,
                               order_detail=result2
                               ,menu="customer", title="Customer Display")

    return render_template("Employee/emp_customer_display.html", name=name, nic=C_NIC, phone=phone, address=address,
                           gender=gender, ages=ages, record_list=record_list, order=result1, custid=custid,
                           order_detail=result2
                           ,menu="customer", title="Customer Display")


@app.route("/index")
def logout():

    session.pop('uid', None)

    return  redirect(url_for('login'))

@app.route("/emp_customer_order_display")
def emp_customer_order_display():

    order_id = request.args.get('order_id')
    order_id = order_id.strip()

    customer_name = request.args.get('customer_name')
    customer_name = customer_name.strip()

    price = request.args.get('price')
    price = price.strip()





    order_detail=db.child("order detail").get().val()


    return render_template("Employee/emp_customer_order_display.html",order_id=order_id,customer_name=customer_name,price=price,order_detail=order_detail
                           ,menu="order", title="Customer Order display")


@app.route("/profile")
def profile():

    try:



        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        emp_name, emp_id = Employee_data.employees_Name(local_id)

        name, cnic, ages, Phone, Gender, Email,Address=Employee_data.employees_info(local_id)

        return render_template("Employee/emp_profile.html",name=name,cnic=cnic,ages=ages,Phone=Phone,Gender=Gender,Email=Email,Address=Address,emp_name=emp_name
                               ,menu="employee", title="Profile")
    except:
        return redirect(url_for("logout"))

@app.route("/profile_update",methods=["GET","POST"])
def profile_update():

    try:

        idtoken = session['uid']
        local_id = Session.get_local_id(idtoken)
        emp_name, emp_id = Employee_data.employees_Name(local_id)

        name = request.form.get('user_name')
        ages = request.form.get('Age')
        cnic = request.form.get('NIC')
        Phone = request.form.get('Phone')
        Address = request.form.get('address')

        data={
            "Address":Address,
            "Age":ages,
            "CNIC":cnic,
            "Name":name,
            "Phone":Phone
        }
        print(data)
        db.child("Employee").child(local_id).child(emp_id).update(data)

        return redirect(url_for("profile"))







    except:
        return redirect(url_for("logout"))


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    try:
        #<------------------------ get value from url ------------------------------------------------------------------------------>

        email = request.args.get('confirm_Email')
        email = email.strip()

        # <----------------------  Send the link to gmail accoutn for reset password ------------------------------------------------->

        auth.send_password_reset_email(email)

        return redirect(url_for("logout"))


    except:
        return redirect(url_for("logout"))

@app.route("/")
def index():
    return render_template("home_index.html")


#<======================================================================================================================>




if __name__ == '__main__':
   
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    app.secret_key = os.urandom(24)
    app.run(debug=True)

