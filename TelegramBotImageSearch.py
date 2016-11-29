import os
import re
import logging
import telebot
import requests
import time
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup as bs

bot = telebot.TeleBot('273459341:AAHBcAeU_ecVwzqxnRr7cZSk7HeMxBc0OYc')

@bot.message_handler(commands=['test'])
def find_file_ids(message):
    for file in os.listdir('music/'):
        if file.split('.')[-1] == 'ogg':
            f = open('music/'+file, 'rb')
            res = bot.send_voice(message.chat.id, f, None)
            print(res)
        time.sleep(3)


@bot.message_handler(commands=['start'])
def SendInfo(message):
    bot.send_message(message.chat.id, 'Привет! я твой бот. Введи запрос для поиска изображения:')


@bot.message_handler(commands=['help'])
def SendHelp(message):
    bot.send_message(message.chat.id, "Список доступных коммад: /start, /about ")


@bot.message_handler(content_types='text')
def SendMessage(message):
    bot.send_message(message.chat.id, "Ожидайте, мы ищем для Вас картиночки!")
    images = SearchGoogleImages(message.text, message.chat.id)
    for image in images:
        bot.send_photo(message.chat.id, open(image, 'rb'))


def SearchGoogleImages(query, id):
    # Создаем папку по id-пользователя
    path = os.path.abspath(os.curdir)
    path = os.path.join(path, str(id))

    if not os.path.exists(path):
        os.makedirs(path)

    # Запрос поисковой системы
    query = query.split()
    query = '+'.join(query)
    query = 'https://www.google.ru/search?' \
            'q= ' + query + \
            '&newwindow=l' \
            '&source=lnms' \
            '&tbm=isch' \

    # Производим запрос
    req = requests.get(query, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/54.0.2840.99 Safari/537.36'})
    soup = bs(req.content, "html.parser")

    # Выбираем только img c data-src
    images = soup.find_all('img', {'data-src': re.compile('gstatic.com')})

    # Массив для хранения путей к найденным изображениям
    imagePaths = []

    # Загружаем первые 10 изображений и сохраняем их
    for number, tag in enumerate(images[:10]):
        data = requests.get(tag['data-src'])
        image = Image.open(BytesIO(data.content))
        imagePath = os.path.join(path, str(number) + '.' + image.format.lower())
        image.save(imagePath)
        imagePaths.append(imagePath)

    return imagePaths


if __name__ == '__main__':
    # Сконфигурируем Log-файл
    logging.basicConfig(filename='botLog.log',
                        format='%(filename)s[LINE:%(lineno)d]# '
                               '%(levelname)-8s [%(asctime)s] '
                               '%(message)s',
                        level=logging.DEBUG)

    logging.info('Start the bot.')

    # В случае возникновения ошибки в Log-файл
    # будет добавлена инфорамция и перезапущен бот
    try:
        bot.polling(none_stop=True)
    except Exception:
        logging.critical('ERROR...')
    finally:
        bot.polling(none_stop=True)