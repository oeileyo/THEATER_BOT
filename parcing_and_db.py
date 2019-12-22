import requests
from bs4 import BeautifulSoup
import re
import sqlite3


# PART 1. ПАРСИНГ KARO
def remove_all(string):
    pattern = re.compile(r'[А-Яа-яёЁ0-9 ]+')
    return pattern.findall(string)[0].strip()


def find_all_theaters_KARO(theatres):
    dicti = {}
    metro_class = 'cinemalist__cinema-item__metro__station-list__station-item'
    for theater in theatres:
        data_id_list.append(theater['data-id'])
        dicti[theater.findAll('h4')[0].text] = {
            'metro': [remove_all(i.text) for i in theater.findAll('li', class_=metro_class)],
            'address': theater.findAll('p')[0].text.split('+')[0].strip(),
            'phone': '+' + theater.findAll('p')[0].text.split('+')[-1],
            'data-id': theater['data-id']
        }
    return dicti


url = "https://karofilm.ru"
url_theaters = url + "/theatres"

data_id_list = []
r = requests.get(url_theaters)
if r.status_code == 200:
    soup = BeautifulSoup(r.text, "html.parser")
    theaters = soup.findAll('li', class_='cinemalist__cinema-item')
    karo_theatres = find_all_theaters_KARO(theaters)
else:
    print("Страница не найдена")
# print(karo_theatres)


def film_time(films):
    dicti = {}
    dicti2 = {}
    for film in films:
        dicti2 = {}
        for i in film.findAll('div', class_='cinema-page-item__schedule__row__board-row'):
            time_dimension = i.findAll('div', class_='cinema-page-item__schedule__row__board-row__left')[0].text.strip()
            time = i.findAll('div', class_='cinema-page-item__schedule__row__board-row__right')[0].findAll('a')
            time_lst = dict(time=[j.text for j in time])

            dicti2['2D'] = {'time': ''}
            dicti2['BLACK 2D'] = {'time': ''}
            dicti2['3D'] = {'time': ''}
            dicti2['IMAX 3D'] = {'time': ''}
            dicti2['КАРОакция'] = {'time': ''}
            dicti2['Luxe 3D'] = {'time': ''}

            dicti2[time_dimension] = time_lst
            dicti[film.findAll('h3')[0].text] = dicti2
    return (dicti)


karo_theaters_films = {}
for id_ in data_id_list:
    url_films = url + "/theatres?id=" + id_
#     print(url_films)
    r = requests.get(url_films)
    if r.status_code == 200:
        s = BeautifulSoup(r.text, "html.parser")
        films = s.findAll('div', class_='cinema-page-item__schedule__row')
        name_cin = s.findAll('div', class_='cinema-page-item__title__left')
        karo_films = film_time(films)
#         print(karo_films)

        karo_theaters_films[id_] = karo_films
    else:
        print("Страница не найдена")
# print(karo_theaters_films)


# PART 1. ПАРСИНГ KINOMAX
def find_all_theaters_KINOMAX(theatres):
    dicti = {}
    count = 0
    for theater in theatres:
        data_id_list_max.append(theater.findAll('a')[0].get('href')[1:-1])
        dicti[theater.findAll('a')[0].text] = {
            'metro': theater.findAll('div', class_='fs-08')[0].text.split('·')[0].strip(),
            'address': theater.findAll('div', class_='fs-08')[-1].text.split('·')[-1].strip(),
            'data-id': count
        }
        count += 1
    return dicti


url = "https://kinomax.ru"
url_theaters = url + "/finder"

data_id_list_max = []
r = requests.get(url_theaters)
if r.status_code == 200:
    soup_max = BeautifulSoup(r.text, "html.parser")
    theaters = soup_max.findAll('div', class_='pt-3 pb-3')
    kinomax_theatres = find_all_theaters_KINOMAX(theaters)
else:
    print("Страница не найдена")
# print(kinomax_theatres)


def film_time_max(films):
    dicti = {}
    dicti2 = {}
    for film in films:
        dicti2 = {}
        for i in range(
                len(film.findAll('div', class_='d-flex w-100 schedule-row'))):  # строки с dimension, time и price
            time_dimension = film.findAll('div', class_='w-10 format-tag')[i].text[12:-10]  # строка с dimension
            time = [j.text for j in film.findAll('div', class_='d-flex w-100 schedule-row')[i].findAll('a')]
            # массив с всем временем для этого dimension
            price = [j.text[17:-15] for j in film.findAll('div', class_='d-flex w-100 schedule-row')[i].findAll('div',
                                                                                                                class_='fs-07 text-main pt-2 text-center')]
            # массив с всеми ценами для этого dimension

            dicti2['2D'] = {'time': '', 'price': ''}
            dicti2['VIP 2D'] = {'time': '', 'price': ''}
            dicti2['3D'] = {'time': '', 'price': ''}
            dicti2['VIP 3D'] = {'time': '', 'price': ''}
            dicti2['DolbyAtmos 3D'] = {'time': '', 'price': ''}
            dicti2['Детский зал'] = {'time': '', 'price': ''}
            dicti2['Комфорт'] = {'time': '', 'price': ''}
            dicti2['Комфорт 3D'] = {'time': '', 'price': ''}
            dicti2['D-BOX 3D'] = {'time': '', 'price': ''}
            dicti2['IMAX 3D'] = {'time': '', 'price': ''}
            dicti2['VIP D-BOX'] = {'time': '', 'price': ''}
            dicti2['IMAX Лазер 3D'] = {'time': '', 'price': ''}
            dicti2['Релакс'] = {'time': '', 'price': ''}
            dicti2['Релакс 3D'] = {'time': '', 'price': ''}

            # если сеанс уже начался, то время можно спарсить, а цену - нет, => убираем
            if len(price) != len(time):
                time = time[1:]

            dicti2[time_dimension]['time'] = time
            dicti2[time_dimension]['price'] = price

        dicti[film.findAll('div', class_='w-70')[0].text[1:-1]] = dicti2  # название фильма
    return dicti


kinomax_theaters_films = {}
for n,id_ in enumerate(data_id_list_max):
    url_films = url + '/' + id_ +'/'
    r = requests.get(url_films)
    if r.status_code == 200:
        s_max = BeautifulSoup(r.text, "html.parser")
        films_max = s_max.findAll('div', class_='d-flex border-bottom-1 border-stack film')
        kinomax_films = film_time_max(films_max)
        kinomax_theaters_films[n] = kinomax_films
    else:
        print("Страница не найдена")


# Part 3. Подключение SQL для KARO
con=sqlite3.connect('karodima.db')
cur=con.cursor()

cur.execute('drop table cinemas')

cur.execute("""CREATE TABLE cinemas( 
             id integer PRIMARY KEY,
             cinema_id integer,
             cinema_name TEXT,
             cinema_address TEXT,
             cinema_metro TEXT, 
             cinema_phone TEXT,
             film_name text,
             t_2d text,
             t_black_2d text,
             t_3d text,
             t_imax3d text,
             t_karosale text,
             t_luxe3d text
             )""")
con.commit()

for i in karo_theatres:
    dataid = karo_theatres[i]['data-id']
    address = karo_theatres[i]['address']
    metro = karo_theatres[i]['metro']
    phone = karo_theatres[i]['phone']
    address = re.sub('"', ' ', address)
    for film_name in karo_theaters_films[dataid]:
        t_2d = karo_theaters_films[dataid][film_name]['2D']['time']
        t_black_2d = karo_theaters_films[dataid][film_name]['BLACK 2D']['time']
        t_3d = karo_theaters_films[dataid][film_name]['3D']['time']
        t_imax3d = karo_theaters_films[dataid][film_name]['IMAX 3D']['time']
        t_karosale = karo_theaters_films[dataid][film_name]['КАРОакция']['time']
        t_luxe3d = karo_theaters_films[dataid][film_name]['Luxe 3D']['time']
        cur.execute(
            f'insert into cinemas(cinema_id, cinema_name, cinema_address, cinema_metro, cinema_phone, film_name, t_2d, '
            f't_black_2d, t_3d, t_imax3d, t_karosale, t_luxe3d) values("{dataid}", "{i}", "{address}", "{metro}", '
            f'"{phone}", "{film_name}", "{t_2d}", "{t_black_2d}", "{t_3d}", "{t_imax3d}", "{t_karosale}", "{t_luxe3d}")')
con.commit()


# Part 4. Подключение SQL для KINOMAX
con=sqlite3.connect('kinomaxx.db')
cur=con.cursor()

cur.execute('drop table cinemas_kinomax')

cur.execute("""CREATE TABLE cinemas_kinomax( 
             id integer PRIMARY KEY,
             cinema_id text,
             cinema_name TEXT,
             cinema_address TEXT,
             cinema_metro TEXT, 
             film_name text,
             t_2d text,
             t_2d_p text,
             t_vip_2d text,
             t_vip_2d_p text,
             t_3d text,
             t_3d_p text,
             t_vip_3d text,
             t_vip_3d_p text,
             t_dolby text,
             t_dolby_p text,
             t_child text,
             t_child_p text,
             t_comf text,
             t_comf_p text,
             t_comf_3d text,
             t_comf_3d_p text,
             t_dbox_3d text,
             t_dbox_3d_p text,
             t_imax_3d text,
             t_imax_3d_p text,
             t_vip_dbox text,
             t_vip_dbox_p text,
             t_imax_laser_3d text,
             t_imax_laser_3d_p text,
             t_relax text,
             t_relax_p text,
             t_relax_3d text,
             t_relax_3d_p text
             )""")
con.commit()

for i in kinomax_theatres:
    dataid = kinomax_theatres[i]['data-id']
    address = kinomax_theatres[i]['address']
    metro = kinomax_theatres[i]['metro']
    address = re.sub('"', ' ', address)
    for film_name in kinomax_theaters_films[dataid]:  # ДОПИСАТЬ

        t_2d = kinomax_theaters_films[dataid][film_name]['2D']['time']
        t_vip_2d = kinomax_theaters_films[dataid][film_name]['VIP 2D']['time']
        t_3d = kinomax_theaters_films[dataid][film_name]['3D']['time']
        t_vip_3d = kinomax_theaters_films[dataid][film_name]['VIP 3D']['time']
        t_dolby = kinomax_theaters_films[dataid][film_name]['DolbyAtmos 3D']['time']
        t_child = kinomax_theaters_films[dataid][film_name]['Детский зал']['time']
        t_comf = kinomax_theaters_films[dataid][film_name]['Комфорт']['time']
        t_comf_3d = kinomax_theaters_films[dataid][film_name]['Комфорт 3D']['time']
        t_dbox_3d = kinomax_theaters_films[dataid][film_name]['D-BOX 3D']['time']
        t_imax_3d = kinomax_theaters_films[dataid][film_name]['IMAX 3D']['time']
        t_vip_dbox = kinomax_theaters_films[dataid][film_name]['VIP D-BOX']['time']
        t_imax_laser_3d = kinomax_theaters_films[dataid][film_name]['IMAX Лазер 3D']['time']
        t_relax = kinomax_theaters_films[dataid][film_name]['Релакс']['time']
        t_relax_3d = kinomax_theaters_films[dataid][film_name]['Релакс 3D']['time']

        t_2d_p = kinomax_theaters_films[dataid][film_name]['2D']['price']
        t_vip_2d_p = kinomax_theaters_films[dataid][film_name]['VIP 2D']['price']
        t_3d_p = kinomax_theaters_films[dataid][film_name]['3D']['price']
        t_vip_3d_p = kinomax_theaters_films[dataid][film_name]['VIP 3D']['price']
        t_dolby_p = kinomax_theaters_films[dataid][film_name]['DolbyAtmos 3D']['price']
        t_child_p = kinomax_theaters_films[dataid][film_name]['Детский зал']['price']
        t_comf_p = kinomax_theaters_films[dataid][film_name]['Комфорт']['price']
        t_comf_3d_p = kinomax_theaters_films[dataid][film_name]['Комфорт 3D']['price']
        t_dbox_3d_p = kinomax_theaters_films[dataid][film_name]['D-BOX 3D']['price']
        t_imax_3d_p = kinomax_theaters_films[dataid][film_name]['IMAX 3D']['price']
        t_vip_dbox_p = kinomax_theaters_films[dataid][film_name]['VIP D-BOX']['price']
        t_imax_laser_3d_p = kinomax_theaters_films[dataid][film_name]['IMAX Лазер 3D']['price']
        t_relax_p = kinomax_theaters_films[dataid][film_name]['Релакс']['price']
        t_relax_3d_p = kinomax_theaters_films[dataid][film_name]['Релакс 3D']['price']

        cur.execute(f'insert into cinemas_kinomax(cinema_id, cinema_name, cinema_address, cinema_metro, film_name, t_2d,'
                    f' t_2d_p, t_vip_2d, t_vip_2d_p, t_3d,t_3d_p, t_vip_3d,t_vip_3d_p, t_dolby,t_dolby_p, t_child,'
                    f't_child_p, t_comf,t_comf_p, t_comf_3d,t_comf_3d_p, t_dbox_3d,t_dbox_3d_p, t_imax_3d,t_imax_3d_p,'
                    f't_vip_dbox,t_vip_dbox_p, t_imax_laser_3d,t_imax_laser_3d_p, t_relax,t_relax_p, t_relax_3d,'
                    f't_relax_3d_p) values("{dataid}", "{i}", "{address}", "{metro}", "{film_name}", "{t_2d}", '
                    f'"{t_2d_p}", "{t_vip_2d}", "{t_vip_2d_p}", "{t_3d}","{t_3d_p}", "{t_vip_3d}","{t_vip_3d_p}", '
                    f'"{t_dolby}","{t_dolby_p}", "{t_child}","{t_child_p}", "{t_comf}","{t_comf_p}", "{t_comf_3d}",'
                    f'"{t_comf_3d_p}", "{t_dbox_3d}","{t_dbox_3d_p}", "{t_imax_3d}","{t_imax_3d_p}", "{t_vip_dbox}",'
                    f'"{t_vip_dbox_p}", "{t_imax_laser_3d}","{t_imax_laser_3d_p}", "{t_relax}","{t_relax_p}", '
                    f'"{t_relax_3d}","{t_relax_3d_p}")')

con.commit()

print('finish')