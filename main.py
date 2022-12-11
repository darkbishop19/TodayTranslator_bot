import telebot
from boto3.dynamodb.conditions import Key
from telebot import types
import json
import config
import database
import Lang_trans
import text_samples

bot = telebot.TeleBot(config.TOKEN)
folder_id = config.folder_id
target_language = 'ru'
API_key = config.API_key


def handler(event, context):
    body = json.loads(event['body'])
    update = telebot.types.Update.de_json(body)
    bot.process_new_updates([update])


telegram_test_db = database.telegram_test_db
table = database.table


@bot.message_handler(commands=['start'])
def get_start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}!\n'
                                      f'Это бот, который переводит текст с изображения или в письменной форме на русский язык\n')
    create_user_db(message)
    offer_to_translate(message)


def create_user_db(message):
    response = table.put_item(
        Item={
            'id_chat': f'{message.chat.id}',
            'id_message': table.item_count,
            'username': message.from_user.username
        }
    )
    return response


def offer_to_translate(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    russian = types.KeyboardButton(text_samples.russian_text)
    english = types.KeyboardButton(text_samples.english_text)
    chinese = types.KeyboardButton(text_samples.chinese_text)
    german = types.KeyboardButton(text_samples.german_text)
    spanish = types.KeyboardButton(text_samples.spanish_text)
    korean = types.KeyboardButton(text_samples.korean_text)
    serbian = types.KeyboardButton(text_samples.serbian_text)
    polish = types.KeyboardButton(text_samples.polish_text)
    french = types.KeyboardButton(text_samples.french_text)
    turkish = types.KeyboardButton(text_samples.turkish_text)
    swedish = types.KeyboardButton(text_samples.swedish_text)
    ukrainian = types.KeyboardButton(text_samples.ukrainian_text)
    markup.add(russian, english, chinese, german, spanish, french, korean, serbian, polish,
               turkish, ukrainian, swedish)
    bot.send_message(message.chat.id, 'Выбери с какого языка будешь переводить ? 👇', reply_markup=markup)
    bot.register_next_step_handler(message, take_a_scope)


def take_a_scope(message):
    if message.text in text_samples.lang_list:
        resp = table.query(KeyConditionExpression=Key('id_chat').eq(f'{message.chat.id}'))

        last_item = resp['Items'][-1]
        response = table.put_item(
            Item={
                'id_chat': f'{message.chat.id}',
                'id_message': last_item.get('id_message') + 1,
                'chosen_language': message.text,
                'username': message.from_user.username
            }
        )
        initial_lang(message)
    else:
        bot.send_message(message.chat.id, 'Видимо вы выбрали язык не из списка\n'
                                          'Пожалуйста, начните процедуру выбора языка c которого переводят заново, '
                                          'команда: /menu ')


def initial_lang(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    russian = types.KeyboardButton(text_samples.russian_text)
    english = types.KeyboardButton(text_samples.english_text)
    chinese = types.KeyboardButton(text_samples.chinese_text)
    german = types.KeyboardButton(text_samples.german_text)
    spanish = types.KeyboardButton(text_samples.spanish_text)
    korean = types.KeyboardButton(text_samples.korean_text)
    serbian = types.KeyboardButton(text_samples.serbian_text)
    polish = types.KeyboardButton(text_samples.polish_text)
    french = types.KeyboardButton(text_samples.french_text)
    turkish = types.KeyboardButton(text_samples.turkish_text)
    swedish = types.KeyboardButton(text_samples.swedish_text)
    ukrainian = types.KeyboardButton(text_samples.ukrainian_text)
    markup.add(russian, english, chinese, german, spanish, french, korean, serbian, polish,
               turkish, ukrainian, swedish)
    bot.send_message(message.chat.id, 'Выберите на какой язык будете переводить ? 👇', reply_markup=markup)
    bot.register_next_step_handler(message, put_initial_lang)


def put_initial_lang(message):
    resp = table.query(KeyConditionExpression=Key('id_chat').eq(f'{message.chat.id}'))
    last_item = resp['Items'][-1]

    if last_item.get('chosen_language') is None:
        bot.send_message(message.chat.id, 'Пожалуйста выберите язык с которого переводят\n'
                                          'Для этого пропишите команду:  /choose_language')
    else:
        if message.text in text_samples.lang_list:
            # print(f'initial lang: {message.text}')
            # bib = last_item.get('id_chat')
            # bob = last_item.get('id_message')
            # print(f'id_chat of last item: {bib} ')
            # print(f'id_message of last item {bob}')
            response = table.update_item(
                Key={
                    'id_chat': last_item.get('id_chat'),
                    'id_message': last_item.get('id_message')
                },
                UpdateExpression='set initial_language= :s',
                ExpressionAttributeValues={
                    ':s': message.text
                }
            )

        else:
            bot.send_message(message.chat.id, 'Видимо вы выбрали язык не из списка кнопок\n'
                                              'Пожалуйста, начните процедуру выбора языка заново, команда: /choose_language')


@bot.message_handler(commands=['menu'])
def menu(message):
    offer_to_translate(message)


@bot.message_handler(commands=['get_info'])
def get_info(message):
    resp = table.query(KeyConditionExpression=Key('id_chat').eq(f'{message.chat.id}'))
    last_item = resp['Items'][-1]
    bot.send_message(message.chat.id, 'Ваш язык с которого переводят 👉"{chosen_language}" \n'
                                      'Ваш язык на который переводят 👉"{initial_language}"'
                     .format(chosen_language=last_item.get('chosen_language'),
                             initial_language=last_item.get('initial_language')))


@bot.message_handler(commands=['choose_language'])  # Выбрать язык для перевода
def choose_language(message):
    offer_to_translate1(message)


def offer_to_translate1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    russian = types.KeyboardButton(text_samples.russian_text)
    english = types.KeyboardButton(text_samples.english_text)
    chinese = types.KeyboardButton(text_samples.chinese_text)
    german = types.KeyboardButton(text_samples.german_text)
    spanish = types.KeyboardButton(text_samples.spanish_text)
    korean = types.KeyboardButton(text_samples.korean_text)
    serbian = types.KeyboardButton(text_samples.serbian_text)
    polish = types.KeyboardButton(text_samples.polish_text)
    french = types.KeyboardButton(text_samples.french_text)
    turkish = types.KeyboardButton(text_samples.turkish_text)
    swedish = types.KeyboardButton(text_samples.swedish_text)
    ukrainian = types.KeyboardButton(text_samples.ukrainian_text)
    markup.add(russian, english, chinese, german, spanish, french, korean, serbian, polish,
               turkish, ukrainian, swedish)
    bot.send_message(message.chat.id, 'Выберите с какого языка будешь переводить ? 👇', reply_markup=markup)
    bot.register_next_step_handler(message, take_a_scope1)


def take_a_scope1(message):
    if message.text in text_samples.lang_list:
        resp = table.query(KeyConditionExpression=Key('id_chat').eq(f'{message.chat.id}'))
        last_item = resp['Items'][-1]
        response = table.put_item(
            Item={
                'id_chat': f'{message.chat.id}',
                'id_message': last_item.get('id_message') + 1,
                'chosen_language': message.text,
                'initial_language': last_item.get('initial_language'),
                'username': message.from_user.username
            }
        )
    else:
        bot.send_message(message.chat.id, 'Видимо вы выбрали язык не из списка\n'
                                          'Пожалуйста, начните процедуру выбора языка заново c которого переводят, '
                                          'команда: /choose_language или /menu ')


@bot.message_handler(commands=['initial_language'])  # Выбрать язык на который переводят
def pick_initial_language(message):
    initial_lang(message)


@bot.message_handler(content_types=['text'])
def translate(message):
    try:
        resp = table.query(KeyConditionExpression=Key('id_chat').eq(f'{message.chat.id}'))
        last_item = resp['Items'][-1]
    except:
        bot.send_message(message.chat.id, 'Видимо база данных бота была обновлена.\n'
                                          'Возможно данные бота о вашем аккаунте утеряны.\n'
                                          'Пожалуйста, начните процедуру регистрации в боте заново, команда: /start')
    if last_item.get('chosen_language') is None:
        bot.send_message(message.chat.id, 'Пожалуйста выбери язык для перевода.\n'
                                          'Для этого пропиши команду:  /menu или /choose_language')
    elif last_item.get('initial_language') is None:
        bot.send_message(message.chat.id, 'Пожалуйста выбери язык на который переводят.\n'
                                          'Для этого пропиши команду: /menu-initial')
    else:
        chosen_language = last_item['chosen_language']
        initial_language = last_item['initial_language']
        Lang_trans.lang_trans(message, chosen_language, initial_language)


bot.infinity_polling()
