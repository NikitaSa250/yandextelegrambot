import telebot, wikipedia, re
import random
from telebot import types
#from langdetect import detect



bot = telebot.TeleBot('5363919453:AAFca8tyFEAvzbHPOztYcDRZ06eRnjsU7Oo')

wikipedia.set_lang("ru")


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

        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)

        return wikitext2

    except Exception as e:
        return 'В энциклопедии нет информации об этом'

@bot.message_handler(commands=["start"])
def start(m, res=False):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Поиск в википедии")
        item2 = types.KeyboardButton("Анекдоты")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(m.chat.id, 'Отправьте мне любое слово, и я найду его значение на Wikipedia')

#@bot.message_handler(content_types=["text"])
#def handle_text(message):
  #  if message.text.strip() == 'Факт':
   # bot.send_message(message.chat.id, getwiki(message.text))



@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Анекдоты' :
            answer = "he-he"
            bot.send_message(message.chat.id, answer)
    elif message.text.strip() == 'Поиск в википедии':
            bot.send_message(message.chat.id, 'Отправьте мне любое слово, и я найду его значение на Wikipedia')
    else:
        bot.send_message(message.chat.id, getwiki(message.text))
    #bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True, interval=0)
