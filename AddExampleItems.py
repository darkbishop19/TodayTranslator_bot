import database

table = database.table
items = [
                {'id_user': 0, 'id_tg_user': '1936243'},
                {'id_user': 1, 'id_tg_user': '13682683'}
            ]
with table.batch_writer() as writer:
    for item in items:
        response = writer.put_item(Item=item)

print(response)
