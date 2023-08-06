'''
Writen by: Stuart Anderson
Copyright: Tobu Pengin, LLC. 2022
'''
from python-decouple import config
from .connector import DynDBC as DBC
from .crud import Operation as execute


"""
EXAMPLE:

#Declare AWS credential variables using .env keys -> see .env file for key values

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
REGION_NAME = config("REGION_NAME")

dbc = DBC(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION_NAME)

if __name__ == "__main__":
    with execute(dbc,'tablename') as ex:
        response = ex.read({'data':{'email':'myemail@email.com'},'get':['email','firstname']}).get('Item')
        print(str(response))

"""        
