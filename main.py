import zipfile
import os
import hashlib
import requests
import re
import csv
# Задание №1. разархивировать архив в выбранную директорию
directory_to_extract_to = 'C:\\Tiff-4.2.0_lab1'
os.mkdir(directory_to_extract_to)
arch_file = zipfile.ZipFile('C:\\tiff-4.2.0_lab1.zip')
arch_file.extractall(directory_to_extract_to)
arch_file.close()
# Задание №2.1
# Получить список файлов (полный путь) формата txt, находящихся в directory_to_extract_to.
# Сохранить полученный список в txt_files
txt_files = []
for address, d, files in os.walk(directory_to_extract_to):
    for f in files:
        path = os.path.join(address, f)
        if '.txt' in path:
            txt_files.append(path)
for i in txt_files:
    print(i)
# Задание №2.2
# Получить значения MD5 хеша для найденных файлов и вывести полученные данные на экран.
res = " "
for file in txt_files:
    target_file = open(file, "rb").read()
    res = hashlib.md5(target_file).hexdigest()
print(res)
print("\n")
# Задание №3
# Найти файл MD5 хеш которого равен target_hash в directory_to_extract_to
# Отобразить полный путь к искомому файлу и его содержимое на экране
target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
target_file = " "
target_file_data = " "
for address, d, files in os.walk(directory_to_extract_to):
    for f in files:
        path = os.path.join(address, f)
        tmp = open(path, "rb").read()
        tmp_data = hashlib.md5(tmp).hexdigest()
        if tmp_data == target_hash:
            target_file = path
            target_file_data = tmp
print(target_file)
print(target_file_data)
print("\n")
# Задание №4
# Ниже представлен фрагмент кода парсинга HTML страницы с помощью регулярных выражений.
r = requests.get(target_file_data)
result_dct = {}  # словарь для записи содержимого таблицы
counter = 0
headers = " "
# Получение списка строк таблицы
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
# Извлечение заголовков таблицы
for line in lines:
    if counter == 0:
        headers = re.sub("<.*?>", " ", line)
        headers = re.findall("Заболели|Умерли|Вылечились|Активные случаи", headers)
    temp = re.sub("<.*?>", ';', line)
    temp = re.sub(r'\(.*?\)', '', temp)
    temp = re.sub(r'\xa0', '', temp)
    temp = re.sub(r'\s', ';', temp)
    temp = re.sub(r'\;;+', '!', temp)
    temp = re.sub(';', ' ', temp)
    temp = re.sub(r'^\!+|\s+$', '', temp)
    temp = re.sub(r'^\W+', '', temp)
    temp = re.sub(r'^\!', '', temp)
    temp = re.sub('_', '-1', temp)
    temp = re.sub(r'[*]', '', temp)
    tmp_split = re.split(r'\!', temp)
    if tmp_split != headers:
        country_name = tmp_split[0]
        col1_val = tmp_split[1]
        col2_val = tmp_split[2]
        col3_val = tmp_split[3]
        col4_val = tmp_split[4]
        result_dct[country_name] = [0, 0, 0, 0]
        result_dct[country_name][0] = int(col1_val)
        result_dct[country_name][1] = int(col2_val)
        result_dct[country_name][2] = int(col3_val)
        result_dct[country_name][3] = int(col4_val)
    counter += 1
'''
print(headers)
for key, value in result_dct.items():
    print(key, ':', value)
'''
# Задание №5
# Запись данных из полученного словаря в файл
output = open('data.csv', 'w')
file_writer = csv.writer(output, delimiter=";")
file_writer.writerow(headers)
for key in result_dct.keys():
    file_writer.writerow([key, result_dct[key][0], result_dct[key][1], result_dct[key][2], result_dct[key][3]])
output.close()
# p = os.path.abspath('data.csv')
# print(p)
# Задание №6
#Вывод данных на экран для указанного первичного ключа (первый столбец таблицы)
target_country = input("Введите название страны: ")
print(headers)
print(result_dct[target_country])




