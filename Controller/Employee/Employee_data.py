
#<----------- Import File -------------->

from Controller import  Configure
from Controller import  libraries

#<-------------------------------------->


# <--------------   FireBase Initiailzation ----------------------->

firebase = libraries.pyrebase.initialize_app(Configure.firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

#<-------------------------------------------------------------------->



# <--------------------  Insert Employees Table ------------------------>

def employee_info(emp_name,emp_email,emp_age,emp_phone,emp_gender,emp_address,emp_salary,emp_timing,emp_CNIC,emp_pass):
    try:
        employees_session_id = auth.create_user_with_email_and_password(emp_email, emp_pass)
        #         Current date time

        date = libraries.datetime.datetime.now()
        date = date.strftime("%d/%B/%Y")

        data={
            'Name':str(emp_name),
            'Email':str(emp_email),
            'Age':str(emp_age),
            'Phone':str(emp_phone),
            'Gender':str(emp_gender),
            'Address':str(emp_address),
            'Salary':str(emp_salary),
            'Timing':str(emp_timing),
            'Date of Join':str(date),
            'CNIC':str(emp_CNIC),
            'Password':str(emp_pass)
        }
        print(data)
        db.child('Employee').child(employees_session_id['localId']).push(data)
        return True
    except:
        return False

#< ----------------------------------------------------------------------------------------- >



#<---------------------------------- Employees Update Data ----------------------------------->


def Employees_update_data(user_data,nic,name,address,phone,salary,timing,age):
    try:
        for d2, (key, value) in enumerate(user_data.items()):
            for d3 , (k,v) in enumerate(value.items()):
                if v["CNIC"]==nic:
                    data={
                        "CNIC":nic,
                        "Age":age,
                        "Salary":salary,
                        "Name":name,
                        "Phone":phone,
                        "Timing":timing,
                        "Address":address
                    }
                    db.child("Employee").child(key).child(k).update(data)
                    return  True
    except:
        return  False



#<--------------------------------------------------------------------------------------------->


# < ---------------------- Get Employees Information ---------------------------------------->


def get_employees_information(emp_result,nic):
    try:
        name=""
        nic1=""
        phone=""
        address=""
        gender=""
        ages=""
        salary=""
        date=""
        time=""

        for k, (key1, value1) in enumerate(emp_result.items()):
            emp_result1=db.child("Employee").child(key1).get().val()
            for k, (key, value) in enumerate(emp_result1.items()):

                if value["CNIC"] == nic:
                    name = value["Name"]
                    nic1 = nic
                    phone=value["Phone"]
                    address=value["Address"]
                    gender=value["Gender"]
                    ages=value["Age"]
                    salary=value["Salary"]
                    date=value["Date of Join"]
                    time=value["Timing"]

        return name,nic1,phone,address,gender,ages,salary,date,time

    except:
        return False


# < ----------------------------------------------------------------------------------------->



#<--------------------------- SMS Sever using SMTP  ----------------------------------------->

def Email_SMS(recever,messages):

    try:
        content=messages

        mail=libraries.smtplib.SMTP('smtp.gmail.com',587)  #specifying smtp server and port 685 can be use too
        mail.ehlo()  #helo is use for regular and ehlo is esmtp is server means extented smtp
        mail.starttls()  #transport layer security ,any smtp command come after this it going to be encrypted
        mail.login('telemedicinefyp@gmail.com','telemedicinefyp123')
        mail.sendmail('telemedicinefyp@gmail.com',recever,content)
        mail.close()

        return True
    except :
        return False


#<------------------------------------------------------------------------------------------------------->



#<-------------------------------------- Generate password ----------------------------------------------->

def generate_password(length):
    letters = libraries.string.ascii_lowercase
    result_str = ''.join(libraries.random.choice(letters) for i in range(length))
    return result_str

#<-------------------------------------------------------------------------------------------------------->



#<-------------------------------- Get Employees Name using local id -------------------------------------->


def employees_Name(local_id):

    result=db.child("Employee").child(local_id).get().val()

    if result!=None:
        for d3,(key,value) in enumerate(result.items()):
            emp_id=key
            name=value["Name"]
            return name,emp_id

    else:
        return None,None


#<---------------------------------------------------------------------------------------------------------->


#<-------------------------------- Get Employees Name using local id -------------------------------------->


def employees_info(local_id):
    result=db.child("Employee").child(local_id).get().val()
    for d3,(key,value) in enumerate(result.items()):

        name=value["Name"]
        cnic=value["CNIC"]
        ages=value["Age"]
        Phone=value["Phone"]
        Gender=value["Gender"]
        Email=value["Email"]
        Address=value['Address']

        return name,cnic,ages,Phone,Gender,Email,Address



#<---------------------------------------------------------------------------------------------------------->