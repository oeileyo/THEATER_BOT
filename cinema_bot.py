import vk_api
import sqlite3
import time
import random

con = sqlite3.connect('karodima.db')
cur = con.cursor()

con_ = sqlite3.connect('kinomaxx.db')
cur_ = con_.cursor()

vk = vk_api.VkApi(token = 'fe6c18f7a5fc3dfd5701444f429f312b914610a48c7369782681b4b9db5a1de6c994ad02410321d992a03')
vk._auth_token()

chosen_theaters = 0
real_id = ''
cinema_films_ = []

dim_names = dict(t_2d = '2D', t_vip_2d = 'VIP 2D', t_3d = '3D', t_vip_3d = 'VIP 3D', t_dolby = 'DolbyAtmos 3D', \
        t_child = 'Детский зал', t_comf = 'Комфорт', t_comf_3d = 'Комфорт 3D', t_dbox_3d = 'D-BOX 3D', \
        t_imax_3d = 'IMAX 3D', t_vip_dbox = 'VIP D-BOX', t_imax_laser_3d = 'IMAX Лазер 3D', t_relax = 'Релакс', \
        t_relax_3d = 'Релакс 3D', t_black_2d = 'BLACK 2D', t_imax3d = 'IMAX 3D', t_karosale = 'КАРОакция', t_luxe3d = 'Luxe 3D')

while True:
    try:
        messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})

        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            body = messages["items"][0]["last_message"]["text"]

            if body.lower() == "привет":
                vk.method("messages.send",
                          {"peer_id": id, "message": "Привет!\nЯ ВК-бот, отображающий расписание сеансов фильмов\nдля 2 "
                                                     "сетей кинотеатров: KARO и KINOMAX.", "random_id": random.randint(1, 2147483647)})
                vk.method("messages.send",
                          {"peer_id": id, "message": """Чтобы выбрать, напиши \"Сеть кинотеатров\" и номер сети:\n1 - KARO FILMS\n2 - KINOMAX""",
                           "random_id": random.randint(1, 2147483647)})


            elif body[:-2].lower() == "сеть кинотеатров":
                chosen_theaters = body[-1]

                if chosen_theaters == "1": # karo
                    theaters_karo = list(cur.execute('select distinct cinema_name from cinemas'))
                    theaters_karo_ = []
                    theaters_karo_str = ''
                    for i in theaters_karo:
                        theaters_karo_.append(i[0])
                    for n, i in enumerate(theaters_karo_, 1):
                        theaters_karo_str += str(n) + ' - ' + i[1:] + '\n'

                    ids_karo = list(cur.execute('select distinct cinema_id from cinemas'))
                    ids_karo_ = []
                    for i in ids_karo:
                        ids_karo_.append(i[0])

                    vk.method("messages.send",
                              {"peer_id": id, "message": f"Список кинатеатров сети KARO: \n {theaters_karo_str}",
                               "random_id": random.randint(1, 2147483647)})
                    vk.method("messages.send",
                              {"peer_id": id, "message": "Чтобы выбрать, напиши \"Кинотеатр\" и номер кинотеатра", "random_id": random.randint(1, 2147483647)})


                elif chosen_theaters == '2': # kinomax
                    theaters_kinomax = list(cur_.execute('select distinct cinema_name from cinemas_kinomax'))
                    theaters_kinomax_ = []
                    theaters_kinomax_str = ''
                    for i in theaters_kinomax:
                        theaters_kinomax_.append(i[0])
                    for n, i in enumerate(theaters_kinomax_, 1):
                        theaters_kinomax_str += str(n) + ' - ' + i + '\n'

                    ids_kinomax = list(cur_.execute('select distinct cinema_id from cinemas_kinomax'))
                    ids_kinomax_ = []
                    for i in ids_kinomax:
                        ids_kinomax_.append(i[0])

                    vk.method("messages.send",
                              {"peer_id": id, "message": f"Список кинатеатров сети KINOMAX: \n {theaters_kinomax_str}",
                               "random_id": random.randint(1, 2147483647)})
                    vk.method("messages.send",
                              {"peer_id": id, "message": "Чтобы выбрать, напиши \"Кинотеатр\" и номер кинотеатра",
                               "random_id": random.randint(1, 2147483647)})

                else:
                    vk.method("messages.send",
                              {"peer_id": id, "message": "Неверный номер сети кинотетров", "random_id": random.randint(1, 2147483647)})


            elif body.lower().split()[0] == "кинотеатр" and chosen_theaters == '1' and int(body.split()[-1]) <= len(theaters_karo_):
                chosen_cinema = body.split()[-1]
                real_id = ids_karo_[int(chosen_cinema) - 1]

                cinema_name = list(cur.execute(f'select distinct cinema_name from cinemas where cinema_id = {real_id}'))[0][0][1:]
                cinema_address = list(cur.execute(f'select distinct cinema_address from cinemas where cinema_id = {real_id}'))[0][0]
                cinema_metro = list(cur.execute(f'select distinct cinema_metro from cinemas where cinema_id = {real_id}'))[0][0]
                cinema_phone = list(cur.execute(f'select distinct cinema_phone from cinemas where cinema_id = {real_id}'))[0][0]

                cinema_metro = cinema_metro[1: -1].replace('\'', '')

                cinema_films = list(cur.execute(f'select distinct film_name from cinemas where cinema_id = {real_id}'))
                cinema_films_ = []
                cinema_films_str = ''
                for i in cinema_films:
                    cinema_films_.append(i[0])
                for n, i in enumerate(cinema_films_, 1):
                    cinema_films_str += str(n) + ' - ' + i + '\n'
                vk.method("messages.send",
                          {"peer_id": id, "message": f"Кинотеатр {cinema_name}:\n"
                                                     f"Адрес: {cinema_address}\n"
                                                     f"Метро: {cinema_metro}\n"
                                                     f"Телефон: {cinema_phone}",
                           "random_id": random.randint(1, 2147483647)})
                vk.method("messages.send",
                          {"peer_id": id, "message": f"Список фильмов в кинотеатре {cinema_name}:\n {cinema_films_str}",
                           "random_id": random.randint(1, 2147483647)})
                vk.method("messages.send",
                          {"peer_id": id, "message": "Чтобы выбрать, напиши \"Фильм\" и номер фильма",
                           "random_id": random.randint(1, 2147483647)})


            elif body.lower().split()[0] == "кинотеатр" and chosen_theaters == '2' and int(body.split()[-1]) <= len(theaters_kinomax_):
                chosen_cinema = body.split()[-1]
                real_id = ids_kinomax_[int(chosen_cinema) - 1]

                cinema_name_ = list(cur_.execute(f'select distinct cinema_name from cinemas_kinomax where cinema_id = {real_id}'))[0][0]
                cinema_address_ = list(cur_.execute(f'select distinct cinema_address from cinemas_kinomax where cinema_id = {real_id}'))[0][0]
                cinema_metro_ = list(cur_.execute(f'select distinct cinema_metro from cinemas_kinomax where cinema_id = {real_id}'))[0][0]

                cinema_films = list(cur_.execute(f'select distinct film_name from cinemas_kinomax where cinema_id = {real_id}'))
                cinema_films_ = []
                cinema_films_str = ''
                for i in cinema_films:
                    cinema_films_.append(i[0])
                for n, i in enumerate(cinema_films_, 1):
                    cinema_films_str += str(n) + ' - ' + i + '\n'

                vk.method("messages.send",
                          {"peer_id": id, "message": f"Кинотеатр {cinema_name_}:\n"
                                                     f"Адрес: {cinema_address_}\n"
                                                     f"Метро: {cinema_metro_ }\n",
                           "random_id": random.randint(1, 2147483647)})
                vk.method("messages.send",
                          {"peer_id": id, "message": f"Список фильмов в кинотеатре {cinema_name_}:\n {cinema_films_str}",
                           "random_id": random.randint(1, 2147483647)})
                vk.method("messages.send",
                          {"peer_id": id, "message": "Чтобы выбрать, напиши \"Фильм\" и номер фильма",
                           "random_id": random.randint(1, 2147483647)})

            elif body.lower().split()[0] == "кинотеатр":
                vk.method("messages.send",
                          {"peer_id": id, "message": "Неверный номер кинотетра",
                           "random_id": random.randint(1, 2147483647)})

            elif body.lower().split()[0] == "фильм" and chosen_theaters == '1' and body.split()[-1] <= len(cinema_films_):
                film_id = body.split()[-1]
                film_name = cinema_films_[int(film_id) - 1]
                print(real_id)

                film_info = {}
                t_2d = list(cur.execute(f"select distinct t_2d from cinemas where cinema_id = '{real_id}' and film_name = '{film_name}'"))[0][0]
                if t_2d != '':
                    film_info[dim_names['t_2d']] = t_2d
                t_black_2d = list(cur.execute(f"select distinct t_black_2d from cinemas where cinema_id = '{real_id}' and film_name = '{film_name}'"))[0][0]
                if t_black_2d != '':
                    film_info[dim_names['t_black_2d']] = t_black_2d
                t_3d = list(cur.execute(f"select distinct t_3d from cinemas where cinema_id = '{real_id}' and film_name = '{film_name}'"))[0][0]
                if t_3d != '':
                    film_info[dim_names['t_3d']] = t_3d
                t_imax3d = list(cur.execute(f"select distinct t_imax3d from cinemas where cinema_id = '{real_id}' and film_name = '{film_name}'"))[0][0]
                if t_imax3d != '':
                    film_info[dim_names['t_imax3d']] = t_imax3d
                t_luxe3d = list(cur.execute(f"select distinct t_luxe3d from cinemas where cinema_id = '{real_id}' and film_name = '{film_name}'"))[0][0]
                if t_luxe3d != '':
                    film_info[dim_names['t_luxe3d']] = t_luxe3d

                film_info_ = ''
                for d, i in film_info.items():
                    film_info_ += d + ':\nВремя:  ' + i[1:-1][1:-1].replace('\'', '') + '\n\n'

                vk.method("messages.send",
                          {"peer_id": id,
                           "message": f"Список сеансов фильма \"{film_name}\" в кинотеатре {cinema_name}:\n {film_info_}",
                           "random_id": random.randint(1, 2147483647)})


            elif body.lower().split()[0] == "фильм" and chosen_theaters == '2' and body.split()[-1] <= len(cinema_films_):
                film_id = body.split()[-1]
                film_name = cinema_films_[int(film_id) - 1]
                film_info = {}

                t_2d = list(cur_.execute(f"select distinct t_2d from cinemas_kinomax where cinema_id = '{real_id}' and film_name = '{film_name}'"))[0][0]
                t_2d_p = list(cur_.execute(f"select distinct t_2d_p from cinemas_kinomax where cinema_id = '{real_id}' and film_name = '{film_name}'"))[0][0]
                if t_2d != '':
                    film_info[dim_names['t_2d']] = list((t_2d, t_2d_p))
                t_vip_2d = list(cur_.execute(f'select distinct t_vip_2d from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                t_vip_2d_p = list(cur_.execute(f'select distinct t_vip_2d_p from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                if t_vip_2d != '':
                    film_info[dim_names['t_vip_2d']] = list((t_vip_2d, t_vip_2d_p))
                t_3d = list(cur_.execute(f'select distinct t_3d from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                t_3d_p = list(cur_.execute(f'select distinct t_3d_p from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                if t_3d != '':
                    film_info[dim_names['t_3d']] = list((t_3d, t_3d_p))
                t_vip_3d = list(cur_.execute(f'select distinct t_vip_3d from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                t_vip_3d_p = list(cur_.execute(f'select distinct t_vip_3d_p from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                if t_vip_3d != '':
                    film_info[dim_names['t_vip_3d']] = list((t_vip_3d, t_vip_3d_p))
                t_dolby = list(cur_.execute(f'select distinct t_dolby from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                t_dolby_p = list(cur_.execute(f'select distinct t_dolby_p from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                if t_dolby != '':
                    film_info[dim_names['t_dolby']] = list((t_dolby, t_dolby_p))
                t_child = list(cur_.execute(f'select distinct t_child from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                t_child_p = list(cur_.execute(f'select distinct t_child_p from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                if t_child != '':
                    film_info[dim_names['t_child']] = list((t_child, t_child_p))
                t_comf = list(cur_.execute(f'select distinct t_comf from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                t_comf_p = list(cur_.execute(f'select distinct t_comf_p from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                if t_comf != '':
                    film_info[dim_names['t_comf']] = list((t_comf, t_comf_p))
                t_comf_3d = list(cur_.execute(f'select distinct t_comf_3d from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                t_comf_3d_p = list(cur_.execute(f'select distinct t_comf_3d_p from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                if t_comf_3d != '':
                    film_info[dim_names['t_comf_3d']] = list((t_comf_3d, t_comf_3d_p))
                t_dbox_3d = list(cur_.execute(f'select distinct t_dbox_3d from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                t_dbox_3d_p = list(cur_.execute(f'select distinct t_dbox_3d_p from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                if t_dbox_3d != '':
                    film_info[dim_names['t_dbox_3d']] = list((t_dbox_3d, t_dbox_3d_p))
                t_imax_3d = list(cur_.execute(f'select distinct t_imax_3d from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                t_imax_3d_p = list(cur_.execute(f'select distinct t_imax_3d_p from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                if t_imax_3d != '':
                    film_info[dim_names['t_imax_3d']] = list((t_imax_3d, t_imax_3d_p))
                t_vip_dbox = list(cur_.execute(f'select distinct t_vip_dbox from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                t_vip_dbox_p = list(cur_.execute(f'select distinct t_vip_dbox_p from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                if t_vip_dbox != '':
                    film_info[dim_names['t_vip_dbox']] = list((t_vip_dbox, t_vip_dbox_p))
                t_imax_laser_3d = list(cur_.execute(f'select distinct t_imax_laser_3d from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                t_imax_laser_3d_p = list(cur_.execute(f'select distinct t_imax_laser_3d_p from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                if t_imax_laser_3d != '':
                    film_info[dim_names['t_imax_laser_3d']] = list((t_imax_laser_3d, t_imax_laser_3d_p))
                t_relax = list(cur_.execute(f'select distinct t_relax from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                t_relax_p = list(cur_.execute(f'select distinct t_relax_p from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                if t_relax != '':
                    film_info[dim_names['t_relax']] = list((t_relax, t_relax_p))
                t_relax_3d = list(cur_.execute(f'select distinct t_relax_3d from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                t_relax_3d_p = list(cur_.execute(f'select distinct t_relax_3d_p from cinemas_kinomax where cinema_id = {real_id} and film_name = "{film_name}"'))[0][0]
                if t_relax_3d != '':
                    film_info[dim_names['t_relax_3d']] = list((t_relax_3d, t_relax_3d_p))

                film_info_ = ''
                for d, i in film_info.items():
                    film_info_ += d + ':\nВремя:  ' + i[0][1:-1].replace('\'', '') + '\nЦены:  ' + i[1][1:-1].replace('\'', '') + '\n\n'

                vk.method("messages.send",
                          {"peer_id": id,
                           "message": f"Список сеансов фильма \"{film_name}\" в кинотеатре {cinema_name_}:\n {film_info_}",
                           "random_id": random.randint(1, 2147483647)})


            else:
                vk.method("messages.send",
                          {"peer_id": id, "message": "Неизвестная команда", "random_id": random.randint(1, 2147483647)})
    except Exception as E:
        time.sleep(1)



# cinemas_lst = list(cursor.execute("select distinct name_theather from cinemas"))
# cinemas_ids = list(cursor.execute("select distinct id_cinema FROM cinemas"))
# metro = list(cursor.execute(f"select distinct metro from cinemas where id_cinema = {remember_cinema_num}"))[0][0]
# cinemas_lst = list(cursor.execute("select distinct name_theather from cinemas"))
# cinemas_ids = list(cursor.execute("select distinct id_cinema FROM cinemas"))
# time2d = list(cursor.execute(f"select time2d from cinemas where id_cinema = '{remember_cinema_num}' and name = '{film_name}'"))[0][0]

#
# film_info_ += ':\nВремя:  '
# for t in i[0]:
#     t = t[1:-1].replace(',', '').split()
#     print(t, 'abc')
#     film_info_ += t + '  '
# film_info_ += '\nЦены:  '
# for _ in i[1]:
#     for p in _:
#         film_info_ += p + '  '
# film_info_ += '\n\n'