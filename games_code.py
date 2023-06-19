from random import randrange, randint
import json

with open('russian_nouns copy.json', 'r') as f:
    text = f.read()
with open('cities_list', 'r') as c_f:
    cities_list = json.load(c_f)


result_file = ''
for line in text:
    result_file += str(line)
final_result = result_file.split()


def find_small(small_word, dictionary):
    result = []
    for word in range(len(dictionary)):
        random = randint(0, len(dictionary) - 1)
        if small_word in dictionary[random]:
            result.append(dictionary[random])
            if len(result) > 199:
                break
    return result


def from_big(example, dictionary):
    words_counter = 0
    result = []
    for word in dictionary:
        if len(example) < len(word):
            continue
        check = 0
        copy = list(example).copy()
        for i in word:
            if i in copy:
                check += 1
                copy.remove(i)
        if check == len(word) and word != example:
            words_counter += 1
            result.append(word)
    return result


banned_letters = ["й", "ы", "ь", "ъ"]


def words_sequence(user_word, dictionary, used):
    words_list = []
    str(user_word).replace('ё', 'е')
    for word in dictionary:
        str(word).replace('ё', 'е')
        if word in used:
            continue
        elif str(user_word.lower()[-1]) in banned_letters:
            if str(word[0]).lower() == str(user_word[-2]).lower():
                words_list.append(word)
        else:
            if str(word[0]).lower() == str(user_word.lower()[-1]):
                str(word).replace('ё', 'е')
                words_list.append(word)
    return words_list[randrange(0, len(words_list))]


# def check_city(dictionary, user_word):
#     counter = 0
#     for word in dictionary:
#         if str(word[0]).lower() == str(user_word.lower()[-1]):
#             counter += 1
#     return counter


# print(check_city(cities_list, 'Человек'))
print(words_sequence('марсель', cities_list, []))
# print(len(cities_list))


