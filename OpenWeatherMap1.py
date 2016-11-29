

import pyowm
import time
import datetime
from fnmatch import translate
from Tools.demo.ss1 import translate
from pyowm.webapi25 import observation
from pyowm.webapi25 import weather

print('openweathermap')
own = pyowm.OWM('180686b776c7052a520c83b711c4be09')
observation = own.weather_at_place('Rostov-on-Don,ru')
weather = observation.get_weather()
location = observation.get_location()
translate = {'Rostov-na-Donu':'Ростов-на-Дону', 'RU':'Россия'}

print(own)
print(observation)
print(weather)
print(location)

print('Страна: ' + location.get_country())


print('Город: ' + location.get_name())

print('Долгота:	' + str(location.get_lon()))

print('Широта: ' + str(location.get_lat()))

print('Облачность:	'+ str(weather.get_clouds()))

print('Статус:	'+ str(weather.get_detailed_status()))

print('Давление:	' + str(weather.get_pressure()))

print('Дождь:	' + str(weather.get_rain()))

print('Снег:	' + str(weather.get_snow()))

print('Время:	' + str(weather.get_reference_time('iso')))

print('Статус:	' + str(weather.get_status()))

print('Восход:	' + str(weather.get_sunrise_time('iso')))

print('Закат:	' + str(weather.get_sunset_time('iso')))

print('Температура:	' + str(weather.get_temperature('celsius')))

print('Видимость:	' + str(weather.get_visibility_distance()))

print('Изображение:	' + weather.get_weather_icon_name())

print('Ветер:	' + str(weather.get_wind()))


def WhatlsCloudness():
    if 0 <= weather.get_clouds() <= 10:  return 'ясная'
    if 10 < weather.get_clouds() <= 30:  return 'немного облачная'
    if 30 < weather.get_clouds() <= 70:  return 'пасмурная'
    if 70 < weather.get_clouds() <= 100: return 'мрачная'


def typeOfWind():
    if 0 <= weather.get_wind()['deg']<=45:
        return 'северный'
    if 45<=weather.get_wind()['deg']<=90:
        return 'северо-восточный'
    if 90<=weather.get_wind()['deg']<=135:
        return 'восточный'
    if 135<=weather.get_wind()['deg']<=180:
        return 'юго-восточный'
    if 180<=weather.get_wind()['deg']<=225:
        return 'южный'
    if 225<=weather.get_wind()['deg']<=270:
        return 'юго-западный'
    if 270<=weather.get_wind()['deg']<=315:
        return 'западный'
    if 315<=weather.get_wind()['deg']<=330:
        return 'северо-западный'
    if 330<=weather.get_wind()['deg']<=360:
        return 'северный'


    print('Погода в городе ' + translate[location.get_name()] + ' (' + translate[location.get_country()] + ')' +
      ' на сегодня в ' + str(datetime.datetime.now().strftime('%H:%M'))+ ' ' + WhatlsCloudness() + ', облачность составляет ' +
      str(weather.get_clouds()) + '%, давление ' + str(weather.get_pressure()['press']) + ' мм. рт. ст., температура '
      + str(int(weather.get_temperature('celsius')['temp'])) + ' градусов Цельсия, ночью ' +
      str(int(weather.get_temperature('celsius')['temp_min'])) + ', днем ' + str(int(weather.get_temperature('celsius')['temp_max'])) +
      '. Ветер ' + typeOfWind() + ' ' + str(weather.get_wind()['speed']) + ' м.\с.')

