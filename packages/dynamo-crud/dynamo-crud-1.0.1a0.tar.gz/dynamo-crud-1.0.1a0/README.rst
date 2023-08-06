dynamo-crud

CRUD Connector for Dynamodb

DynamoDB API. Under GPL3 license with the Pengin Open Source Foundation and subject to the supervision of Tobu Pengin, LLC.

This package will allow for easy deployment of a CRUD connection to your DynamoDB tables. The aim of this library is to create a worker for an individual DynamoDB session that can be made to connect to a table and run a CRUD operation, return the result, delete the operation, and return the worker to passive mode. The framework is being designed to seemlessly integrate with a Django or Flask based web app. You may freely diseminate and modify this code according to the GPL3 license it falls under.

parts: init.py #controls the configs and workflow of the app .env #contains the amazon credentials for the app, and any additional configurations connector.py #creates the dynamodb connection crud.py #contains the CRUD operations. run as an exectution in a with statement with the database connector
