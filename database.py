import boto3
import config

telegram_test_db = boto3.resource(
    'dynamodb',
    endpoint_url=config.USER_STORAGE_URL,
    region_name='ru-central1',
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
)
table = telegram_test_db.Table('telebot-translate')
