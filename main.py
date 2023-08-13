from fastapi import FastAPI

app = FastAPI()
keys = [
    'geonameid',
    'name',
    'asciiname',
    'alternatenames',
    'latitude',
    'longitude',
    'feature class',
    'feature code',
    'country code',
    'cc2',
    'admin1 code',
    'admin2 code',
    'admin3 code',
    'admin4 code',
    'population',
    'elevation',
    'dem',
    'timezone',
    'modification date'
]
keys_timezone = [
    'country code',
    'time zone id',
    'GMT',
    'offset',
    'raw offset'
]

def read_data_from_file(filename, keys):
    lines = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            combined_dict = {}
            for i in range(len(keys)):
                combined_dict[keys[i]] = line.strip('\n').split('\t')[i]  # Добавляем элемент в словарь
            lines.append(combined_dict)
        return lines


data = read_data_from_file('RU.txt', keys)
timezone = read_data_from_file('TimeZone.txt', keys_timezone)


# Метод возвращает словарь по geonameid в случае нахождения, и None в случае если такого словаря нет
@app.get('/city/{geo_name_id}')
def get_info(geo_name_id):
    for city in data:
        if city.get('geonameid') == geo_name_id:
            return city


# Метод возвращает массив словарей с условием пользователя, массив разбивается на "страницы" и выводит все словари
# находящиеся на этой странице
@app.get('/cities')
def get_cities(page_number: int, cities_per_page: int):
    start_index = (page_number - 1) * cities_per_page
    end_index = start_index + cities_per_page
    cities_on_page = data[start_index:end_index]

    return cities_on_page


# Метод принимает 2 города, выводит их, какой город севернее и одинаковые ли часовые пояса
@app.get('/cities/different')
def get_different_by_cities(first_city, second_city):
    f_founded_cities = []
    s_founded_cities = []

    # Находим все города по русскому названию и записываем в массив
    for city in data:
        names = city.get('alternatenames').split(',')
        for name in names:
            if name.lower() == first_city.lower():
                f_founded_cities.append(city)
            elif name.lower() == second_city.lower():
                s_founded_cities.append(city)

    # Проверка на отсутствие одного из городов
    if len(f_founded_cities) == 0 or len(s_founded_cities) == 0:
        print('Один из городов не найден')
        return None

    # Сортировка по населению, в случае если значения будут равны, возьмется первый попавшийся словарь
    f_city = sorted(f_founded_cities, key=lambda city_population: int(city_population['population']), reverse=True)[0]
    s_city = sorted(s_founded_cities, key=lambda city_population: int(city_population['population']), reverse=True)[0]
    # Определение северного города
    higher_latitude_city = f_city if f_city.get('latitude') > s_city.get('latitude') else s_city
    # Проверка на одинаковые часовые пояса и вычисление разницы между ними
    is_same_timezone = f_city.get('timezone') == s_city.get('timezone')
    difference_timezones = abs(float(get_gmt(f_city.get('timezone'))) - float(get_gmt(s_city.get('timezone'))))

    return {'higher_latitude_city': higher_latitude_city,
            'is_same_timezone: ': is_same_timezone,
            'difference_timezones: ': difference_timezones,
            'f_city: ': f_city,
            's_city: ': s_city,
            }


def get_gmt(time_zone_id):
    for zone in timezone:
        if zone.get('time zone id') == time_zone_id:
            return zone.get('GMT')