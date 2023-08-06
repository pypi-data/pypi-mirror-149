'''
Writen by: Stuart Anderson
Copyright: Tobu Pengin, LLC. 2022
'''

class Operation:
    def __init__(self, dbc, table, create=None):
        if create is None:
            self.table = dbc().Table(table)
        else:
            self.create(dbc,create)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        del self
    
    def create(self):
        return self.table.put_item(
            Item = self.data['data']
        )

    def read(self, data):
        return self.table.get_item(
            Key = data['data'],
            AttributesToGet= data['get']
        )

    def update(self, data):
        return self.table.update_item(
            Key = data['data'],
            AttributeUpdates=self.data['updates'],
            ReturnValues="UPDATED_NEW"
        )

    def delete(self):
        return self.table.delete_item(
            Key = self.data['data']
        )

    def create_all(self, dbc, **kw):
        dbc().create_table(
            AttributeDefinitions=kw.get("attributes"),
            TableName = kw.get("tablename"),
            KeyShema = kw.get("schema"),
         BillingMode = 'PAY_PER_REQUEST'
         )