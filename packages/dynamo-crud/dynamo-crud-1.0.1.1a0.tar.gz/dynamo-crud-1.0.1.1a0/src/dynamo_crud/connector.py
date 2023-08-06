'''
Writen by: Stuart Anderson
Copyright: Tobu Pengin, LLC. 2022
'''
from boto3 import Session as Dyn_ses #import for dynamoDB session


class DynDBC():
    def __init__(self, **credentials):
        #try to create an AWS session object
        try:
            self.aws_session = Dyn_ses(aws_access_key_id=credentials.get("AWS_ACCESS_KEY_ID"), aws_secret_access_key=credentials.get("AWS_SECRET_ACCESS_KEY"))
        except Exception as e:
            raise e.message

        #try to create the DynamoDB resource object
        try:
            self.aws_resource = self.aws_session.resource('dynamodb', region_name=credentials.get("REGION_NAME"))
        except Exception as e:
            raise e.message

    def __call__(self):
        return self.aws_resource
