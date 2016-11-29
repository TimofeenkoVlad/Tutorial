import pyowm
import datetime
print("OpenWeatherMap")
owm = pyowm.OWM('66e17093b04397104960767aaed6fb63')
observation = owm.weather_at_place('Rostov-on-Don,ru')
weather = observation.get_weather()
location = observation.get_location()
translate = {'Rostov-na-Donu':'Ростов-на-Дону', 'RU':'Россия'}


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

def weatherToWord():
    if 0<=weather.get_clouds()<=10:
        return 'ясная'
    if 10<=weather.get_clouds()<=30:
        return 'немного облачная'
    if 30<=weather.get_clouds()<=70:
        return 'пасмурная'
    if 70<=weather.get_clouds()<=100:
        return 'мрачная'

print(owm)
print(weather)
print()
print('Погода в городе ' + translate[location.get_name()] + ' (' + translate[location.get_country()] + ')' +
      ' на сегодня в ' + str(datetime.datetime.now().strftime('%H:%M'))+ ' ' + weatherToWord() + ', облачность составляет ' +
      str(weather.get_clouds()) + '%, давление ' + str(weather.get_pressure()['press']) + ' мм. рт. ст., температура '
      + str(int(weather.get_temperature('celsius')['temp'])) + ' градусов Цельсия, ночью ' +
      str(int(weather.get_temperature('celsius')['temp_min'])) + ', днем ' + str(int(weather.get_temperature('celsius')['temp_max'])) +
      '. Ветер ' + typeOfWind() + ' ' + str(weather.get_wind()['speed']) + ' м.\с.')

