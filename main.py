import random, requests
import telebot, wikipedia, re
from telebot import types
import os
from fuzzywuzzy import fuzz

bot = telebot.TeleBot('5363919453:AAFca8tyFEAvzbHPOztYcDRZ06eRnjsU7Oo')
wikipedia.set_lang("ru")



mas = []
if os.path.exists('talking.txt'):
    f = open('talking.txt', 'r', encoding='UTF-8')
    for x in f:
        if len(x.strip()) > 2:
            mas.append(x.strip().lower())
    f.close()


def answer(text):
    try:
        text = text.lower().strip()
        if os.path.exists('talking.txt'):
            a = 0
            n = 0
            nn = 0
            for q in mas:
                if('u: ' in q):
                    aa = (fuzz.token_sort_ratio(q.replace('u: ',''), text))
                    if(aa > a and aa!= a):
                        a = aa
                        nn = n
                n = n + 1
            s = mas[nn + 1]
            return s
        else:
            return 'Ошибка'
    except:
        return 'Ошибка'


def get_a_joke():
    f = open('jokes.txt', 'r', encoding='UTF-8')
    jokes = f.read().split('<>')
    f.close()
    return random.choice(jokes)


def getwiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext = ny.content[:1000]
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not('==' in x):
                if(len((x.strip()))>3):
                   wikitext2 = wikitext2+x+'.'
            else:
                break

        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)

        return wikitext2

    except Exception as e:
        return 'В энциклопедии нет информации об этом'


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.from_user.id, "Привет, друг!")
    keyboard = types.InlineKeyboardMarkup()

    key_wikipedia = types.InlineKeyboardButton(text='Поиск по Wikipedia', callback_data='wikisearch')
    keyboard.add(key_wikipedia)
    key_jokes = types.InlineKeyboardButton(text='Анекдоты', callback_data='jokes')
    keyboard.add(key_jokes)
    key_talking = types.InlineKeyboardButton(text='Пообщаемся?', callback_data='chatbot')
    keyboard.add(key_talking)
    bot.send_message(m.from_user.id, text='Выберите нужную вам функцию', reply_markup=keyboard)
        #bot.send_message(m.chat.id, 'Отправьте мне любое слово, я найду его значение на Wikipedia')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    previous_message = ''
    if message.text == "Пообщаемся?":
        previous_message = message.text
    if previous_message == "Пообщаемся?":
        f = open(str(message.chat.id) + '_log.txt', 'a', encoding='UTF-8')
        s = answer(message.text)
        f.write('u: ' + message.text + '\n' + s + '\n')
        f.close()
        bot.send_message(message.chat.id, s)
    else:
        if message.text == "/help":
            bot.send_message(message.from_user.id, "Напиши /start")
        elif message.text == "Поиск по Wikipedia" or message.text == 'поиск по википедии' \
                or message.text == 'найти на википедии' or message.text == 'поиск по Wikipedia':
            bot.send_message(message.from_user.id, 'Отправьте мне любое слово, я найду его значение на Wikipedia')
        elif message.text == "Анекдоты" or message.text == "анекдоты" or message.text == "анекдот" \
                or message.text == "Анекдоты":
            bot.send_message(message.from_user.id, get_a_joke())
        else:
            bot.send_message(message.from_user.id, getwiki(message.text))


#@bot.message_handler(content_types=["Пообщаемся?"])
#def handle_text(message):
 #   bot.send_message(message.from_user.id, 'Приветик. поболтаем?)')
   # f = open(str(message.chat.id) + '_log.txt', 'a', encoding='UTF-8')
   # s = answer(message.text)
   # f.write('u: ' + message.text + '\n' + s +'\n')
   # f.close()
   # bot.send_message(message.chat.id, s)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "wikisearch":
        bot.send_message(call.from_user.id, 'Отправьте мне любое слово, я найду его значение на Wikipedia')
    elif call.data == "jokes":
        bot.send_message(call.from_user.id, get_a_joke())
    elif call.data == "chatbot":
        bot.send_message(call.from_user.id, 'Приветик. поболтаем?)')
bot.polling(none_stop=True, interval=0)

