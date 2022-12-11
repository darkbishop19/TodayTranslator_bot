import telebot

import requests
import json

from boto3.dynamodb.conditions import Key
from telebot.types import ReplyKeyboardRemove

import config
import database
import text_mapping


bot = telebot.TeleBot(config.TOKEN)
IAM_TOKEN = config.IAM_TOKEN
folder_id = config.folder_id

API_key = config.API_key
table = database.table


def lang_trans(message, chosen_language, initial_language):
    list_lang = text_mapping.pick_langs(chosen_language, initial_language)
    source_language = list_lang[0]
    target_language = list_lang[1]

    body = {
        "targetLanguageCode": target_language,
        "sourceLanguageCode": source_language,
        "texts": message.text,
        "folderId": folder_id,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key {0}".format(API_key)
    }

    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                             json=body,
                             headers=headers
                             )

    json_text_function = json.loads(response.text)
    x = json_text_function['translations']

    for i in x:
        translated_text = i['text']
        total_text = f'{translated_text}\n\n©*2022 ArtCher*'
        put_message(message, chosen_language, initial_language, translated_text)
        bot.reply_to(message, total_text, parse_mode="Markdown", reply_markup = ReplyKeyboardRemove())
        # bot.send_message(config.admin_id, f'{total_text}\n'
        #                  f'Отправлен: {message.chat.id} {message.from_user.first_name} {message.from_user.last_name}')


def put_message(message, chosen_language, initial_language,  translated_text):
    resp = table.query(KeyConditionExpression=Key('id_chat').eq(f'{message.chat.id}'))
    last_item = resp['Items'][-1]
    
    response = table.put_item(
        Item={
            'id_chat': f'{message.chat.id}',
            'id_message': last_item.get('id_message') + 1,
            'chosen_language': chosen_language,
            'initial_language': initial_language,
            'message': message.text,
            'translated_text': translated_text,
            'username': message.from_user.username
        }
    )

