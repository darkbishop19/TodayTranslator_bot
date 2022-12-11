import telebot

from boto3.dynamodb.conditions import Key
from telebot.types import ReplyKeyboardRemove
from deep_translator import GoogleTranslator
import config
import database
import text_mapping

bot = telebot.TeleBot(config.TOKEN)
API_key = config.API_key
table = database.table


def lang_trans(message, chosen_language, initial_language):
    list_lang = text_mapping.pick_langs(chosen_language, initial_language)
    source_language = list_lang[0]
    target_language = list_lang[1]

    translated_text = GoogleTranslator(source=source_language, target=target_language).translate(message.text)

    total_text = f'{translated_text}\n\n©*2022 ArtCher*'
    put_message(message, chosen_language, initial_language, translated_text)
    bot.reply_to(message, total_text, parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())
    # bot.send_message(config.admin_id, f'{total_text}\n'
    #    f'Отправлен: {message.chat.id} {message.from_user.first_name} {message.from_user.last_name}')


def put_message(message, chosen_language, initial_language, translated_text):
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
