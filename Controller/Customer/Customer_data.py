from Controller import  libraries
from Controller import  Configure



firebase = libraries.pyrebase.initialize_app(Configure.firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()


def customer_info(customer_name,nic,phone_number,age,gender,address,emp_id):
    try:
        date=libraries.datetime.datetime.now()
        date=date.strftime("%d/%B/%Y")
        data={
            'customer_name':str(customer_name),
            'NIC':str(nic),
            'employee_id':None,
            'phone_number':str(phone_number),
            'age':str(age),
            'gender':str(gender),
            'address':str(address),
            'date':str(date),
            'employees_id': str(emp_id)
        }

        db.child('Customer').push(data)
        return True
    except:
        return False

def customer_id(customer_id):
    try:
        customer_id1=""
        for k, (key, value) in enumerate(customer_id.items()):

                customer_id1 = key



        return  customer_id1
    except:
        return 1

def get_customer_information(customer_result,nic):
    try:
        customer_name=""
        customer_nic=""
        phone=""
        address=""
        gender=""
        ages=""
        id=""

        for k, (key, value) in enumerate(customer_result.items()):

            if value["NIC"] == nic:
                customer_name = value["customer_name"]
                customer_nic = nic
                phone=value["phone_number"]
                address=value["address"]
                gender=value["gender"]
                ages=value["age"]
                id=key
        return customer_name,customer_nic,phone,address,gender,ages

    except:
        return False


def update_customer_data(user_data,nic,name,age,phone,address):
    try:

        for d2, (key, value) in enumerate(user_data.items()):

            if nic == value["NIC"]:
                data = {
                    'customer_name': name,
                    'age': age,
                    'NIC': nic,
                    'phone_number': phone,
                    'address': address
                }
                print("key ", key)
                db.child("Customer").child(key).update(data)
                return True
    except:
        return False

def get_customerid(customer_result,nic):
    try:
        
        
        cust_id=""
        

        for k, (key, value) in enumerate(customer_result.items()):

            if value["NIC"] == nic:
               cust_id=key
        return cust_id

    except:
        return False




def get_customer_order_information(customer_result,cust_id):
    try:
        order_id=""
        product_name=""
        price=""
        quantity=""
        totalbill=""
        record_list=[]
        for k, (key, value) in enumerate(customer_result.items()):
            list=[]

            if value["Customer id"] == cust_id:
                product_name = value["Product Name"]
                quantity=value["Quantity"]
                price=value["Price"]
                totalbill=value["Total bill"]
                list.append(product_name)
                list.append(quantity)
                list.append(price)
                list.append(totalbill)
                record_list.append(list)
        print(record_list)
                

        return record_list

    except:
        return False