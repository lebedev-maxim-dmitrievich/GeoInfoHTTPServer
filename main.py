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
data = []

# Чтение и перенос данных о городах в память
with open('RU.txt', 'r', encoding='utf-8') as file:
    for line in file:
        combined_dict = {}
        for i in range(len(keys)):
            combined_dict[keys[i]] = line.split('\t')[i]  # Добавляем элемент в словарь
        data.append(combined_dict)


# Метод возвращает словарь по geonameid в случае нахождения, и None в случае если такого словаря нет
def get_info(geonameid):
    for city in data:
        if city.get('geonameid') == geonameid:
            return city


# Метод возвращает массив словарей с условием пользователя, массив разбивается на "страницы" и выводит все словари
# находящиеся на этой странице
def get_cities(page_number, cities_per_page):
    start_index = (page_number - 1) * cities_per_page
    end_index = start_index + cities_per_page
    cities_on_page = data[start_index:end_index]

    return cities_on_page


# Метод принимает 2 города, выводит их, какой город севернее и одинаковые ли часовые пояса
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
    # Проверка на одинаковые часовые пояса
    is_same_timezone = f_city.get('timezone') == s_city.get('timezone')

    print(f'Самый северный город: {higher_latitude_city}')
    print(f'Одинаковая ли временная зона: {is_same_timezone}')
    print(f'Первый город: {f_city}\nВторой город: {s_city}')


def compare_by_population(city):
    return city['population']


print(get_info(519002))
print(get_cities(10, 20))
print(get_different_by_cities('Пенза', 'Владивосток'))