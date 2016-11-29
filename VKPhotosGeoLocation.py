import time
import vk

print('VK Photos geo location')

#	Авторизуем сессию с помощью access token

session = vk.Session('da4c8acd70a144c86613dc28d0e11227dd78b730315b144a2ab3372ec7a2c5e2c31f72a9769433782f31b')

# или с помощью id приложения и данных авторизации пользователя

#	session = vk.AuthSession('арр id', 'user login', 'user password')

# Создаем объект API
api = vk.API(session)

#	Запрашиваем список всех друзей
friends = api.friends.get()

print(len(friends))
print(friends)

#	Получаем список всех друзей
friends = api.friends.get()

#	Получаем информацию о всех друзьях
friends_info = api.users.get(user_ids=friends)

#	Выведем список друзей в удобном виде
for friend in friends_info:
    print('ID: %s Имя: %s %s' % (friend['uid'], friend['last_name'], friend['first_name']))

# Здесь будут храниться геоданные
geolocation = []

# Получим геоданные всех фотографий каждого друга
# Цикл перебирающий всех друзей
for id in friends:
    print('Получаем данные пользователя: %s' % id)
    # Получаем все альбомы пользователя, кроме служебных
    albums = api.photos.getAlbums(owner_id=id)
    print('\t... альбомов %s...' % len(albums))
    # Цикл перебирающий все альбомы пользователя
    for album in albums:
        # Обрабатываем исключение для приватных альбомов/фото
        try:
            # Получаем все фотографии из альбома
            photos = api.photos.get(owner_id=id, album_id=album['aid'])
            print('\t\t...обрабатываем фотографии альбома...')
            # Цикл перебирающий все фото в альбоме
            for photo in photos:
                # Если в фото имеются геоданные, то добавим их в список geolocation
                if 'lat' in photo and 'long' in photo:
                    geolocation.append((photo['lat'], photo['long']))
            print('\t\t...найдено %s фото..' % len(photos))
        except:
            pass
        # Задержка между запросами photos.get
        time.sleep(0.5)
    # Задержка между запросами photos.getAlbums
    time.sleep(0.5)

js_code = ""

# Проходим по всем геоданным и генерируем JS команду добавления маркера
for loc in geolocation:
    js_code += 'new google.maps.Marker({ position: {lat: %s, lng: %s}, map: map });\n' % (loc[0], loc[1])

# Считываем из файла-шаблона html данные
html = open('map.html').read()
# Заменяем placeholder на сгенерированый код
html = html.replace('/* PLACEHOLDER */', js_code)

# Записываем данные в новый файл
f = open('VKPhotosGeoLocation.html', 'w')
f.write(html)
f.close()