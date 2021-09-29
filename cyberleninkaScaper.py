import requests
import json
import csv
import re

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
        "Accept": "*/*",
        "Accept-Language": "ru,en;q=0.5",
        "Content-Type": "application/json",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Cache-Control": "max-age=0"
    }

#Максимальное количество статей (если столько найдено не будет, то придет, сколько есть)
length = 20

#Что ищем
q = "скрапинг"

#Файл для записи результатов
FILENAME = "articles.csv"

data = {"mode":"articles","q":q,"size":length,"from":0}

response = requests.post('https://cyberleninka.ru/api/search', headers=headers, data=json.dumps(data))

res = json.loads(response.text)

items = ["name", "year", "annotation", "link", "authors"]

#Массив с данными по статьм
rows = []
for article in res["articles"]:
    #Массив данных отдельной статьи
    row = []
    for value in items:
        #Убрать тег и кавычки с скобками у авторов
        article[value] = re.sub(r'(<.+?>)|[\[\]\']', '', str(article[value]))
        #Полная ссылка
        if (value == "link"):
            article[value] = "https://cyberleninka.ru" + article[value]
        row.append(article[value])
    rows.append(row)

#Запись в CSV файл полученных данных
with open(FILENAME, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(rows)
