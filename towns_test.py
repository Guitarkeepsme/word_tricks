from random import randrange
import json


with open('cities.json', 'r') as file:
    info = json.load(file)

with open('cities_list', 'r') as c_file:
    cities = json.load(c_file)


def cities_sequence(user_word, dictionary, used):
    banned_letters = ["й", "ы", "ь", "ъ"]
    words_list = []
    str(user_word).replace('ё', 'е')
    for word in dictionary:
        if word in used:
            continue
        elif user_word.lower()[-1] in banned_letters:
            if word[0] == user_word[-2]:
                str(word).replace('ё', 'е')
                words_list.append(word)
        else:
            if word[0] == user_word.lower()[-1]:
                str(word).replace('ё', 'е')
                words_list.append(word)
    return words_list[randrange(0, len(words_list))]


# def city_converter(dictionary):
#     cities = []
#     for city in dictionary.get('city'):
#         cities.append(city.get('name'))
#     with open('cities_list', "w") as cities_file:
#         json.dump(cities, cities_file, ensure_ascii=False, indent=4)
# print(city_converter(info))

print(cities_sequence(голос, info, 'Москва'))
