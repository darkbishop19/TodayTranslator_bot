import database

table = database.table
scan = table.scan()
with table.batch_writer() as batch:
    for each in scan['Items']:
        batch.delete_item(
            Key={
                'id_chat': each['id_chat'],
                'id_message': each['id_message']
            }
        )

