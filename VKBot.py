import vk
import time
import datetime

from OpenWeatherMap import translate, location, WhatlsCloudness, typeOfWind
from OpenWeatherMap import weather

print('VKBot')

# Авторизуем сессию с помощью access токена
session = vk.Session('3994efb0c527364bb3426885c71d182c128880d24eb7fbec3e5ad23a5fd5c884d30b805905b28d811f9b2')

# Создаем объект API
api = vk.API(session)

while (True):
    # Получим 20 последних входящих сообщений
    messages = api.messages.get()

    # Создадим список поддерживаемых комманд
    commands = ['help', 'weather', 'hello', 'До Встречи', 'привет']

    # Найдем среди них непрочитанные сообщения с поддерживаемыми командами
    # таким образом получим список в формате [(1d_пользователя, id_сообщения, команда), ...]
    messages = [(m['uid'], m['mid'], m['body'])
                for m in messages[1:] if m['body'] in commands and m['read_state'] == 0]

    # Отвечаем на полученные команды
    for m in messages:
        user_id = m[0]
        message_id = m[1]
        comand = m[2]

        # Сформируем строку с датой и временем сервера
        date_time_string = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')

        if comand == 'help':
            api.messages.send(user_id=user_id,
                              message=date_time_string + '\n>VKBot vO.1\n>Разработал: Влад')

        if comand == 'weather':
            api.messages.send(user_id=user_id,
                              message=date_time_string + 'Погода в городе ' + translate[location.get_name()] + ' (' + translate[location.get_country()] + ')' +
      ' на сегодня в ' + str(datetime.datetime.now().strftime('%H:%M'))+ ' ' + WhatlsCloudness() + ', облачность составляет ' +
      str(weather.get_clouds()) + '%, давление ' + str(weather.get_pressure()['press']) + ' мм. рт. ст., температура '
      + str(int(weather.get_temperature('celsius')['temp'])) + ' градусов Цельсия, ночью ' +
      str(int(weather.get_temperature('celsius')['temp_min'])) + ', днем ' + str(int(weather.get_temperature('celsius')['temp_max'])) +
      '. Ветер ' + typeOfWind() + ' ' + str(weather.get_wind()['speed']) + ' м.\с.')
        if comand == 'hello':
            api.messages.send(user_id=user_id,
                              message=date_time_string + '\n>VKBot vO.1\n>Hi')
        if comand == 'До Встречи':
            api.messages.send(user_id=user_id,
                              message=date_time_string + '\n>VKBot vO.1\n>До свидания ')
        if comand == 'привет':
            api.messages.send(user_id=user_id,
                              message='\nДоброго времени суток')

    # Формируем список id всех сообщений с командами через запятую
    ids = ', '.join([str(m[1]) for m in messages])

    # Помечаем полученные сообщения как прочитанные
    if ids:
        api.messages.markAsRead(message_ids=ids)

    # Проверяем сообщения каждые 3 секунды
    time.sleep(3)
