from Controller import libraries
from Controller import Configure

firebase = libraries.pyrebase.initialize_app(Configure.firebaseConfig)
auth = firebase.auth()


#<----------------- Employees local id get kre ga ------------------------->
def get_local_id(id_token):


    local_id = auth.get_account_info(id_token)
    local_id = local_id['users']
    local_id = local_id[0]
    local_id = local_id['localId']
    return local_id

