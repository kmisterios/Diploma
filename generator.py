import json
import random

items = ['eggs', 'milk', 'cheese', 'bread', 'porridge']
names = ['Misha', 'Lena', 'Ivan', 'Nikita', 'Aleksandr', 'Fillip']

# есть поле текст n шагов, а после n+1 - нет
def error1(n):
    data_arr = []
    n = int(n)
    for i in range(n):
        data = {}
        data["idOfCrawler"] = 1
        data['name'] = random.choice(items)
        data['price'] = random.randrange(8, 9) + round(random.random(), 3)
        data['count'] = random.randint(1,10)
        data['customer name'] = random.choice(names)
        data['phone number'] = "+79" + str(random.randint(111111111,999999999))
        data_arr.append(data)
    for i in range(int(n / 10)):
        data = {}
        data["idOfCrawler"] = 1
        data['name'] = ''
        data['price'] = random.randrange(8, 9) + round(random.random(), 3)
        data['count'] = random.randint(1,10)
        data['customer name'] = random.choice(names)
        data['phone number'] = "+79" + str(random.randint(111111111,999999999))
        data_arr.append(data)
    with open('anomaly1.json', 'w') as json_file:
        json.dump(data_arr, json_file)
        print("file written")

# Текст с вероятнстью P = 58,9% есть, а потом его нет
def error2(n):
    data_arr = []
    n = int(n)
    for i in range(n):
        data = {}
        data["idOfCrawler"] = 1
        data['name'] = random.choice(items)
        data['price'] = random.randrange(8, 9) + round(random.random(), 3)
        data['count'] = random.randint(1,10)
        if random.random() < 0.589:
            data["customer name"] = random.choice(names)
        else:
            data["customer name"] = ''
        data['phone number'] = "+79" + str(random.randint(111111111,999999999))
        data_arr.append(data)
    for i in range(int(n / 5)):
        data = {}
        data["idOfCrawler"] = 1
        data["customer name"] = ''
        data['name'] = random.choice(items)
        data['price'] = random.randrange(8, 9) + round(random.random(), 3)
        data['count'] = random.randint(1,10)
        data['phone number'] = "+79" + str(random.randint(111111111,999999999))
        data_arr.append(data)
    with open('anomaly2.json', 'w') as json_file:
        json.dump(data_arr, json_file)

# Число n раз [1,10], а c n + 1 раза [50,70]
def error3(n):
    data_arr = []
    n = int(n)
    for i in range(n):
        data = {}
        data["idOfCrawler"] = 1
        data['name'] = random.choice(items)
        data['price'] = random.randrange(8, 9) + round(random.random(), 3)
        data['count'] = random.randint(1,10)
        data['customer name'] = random.choice(names)
        data['phone number'] = "+79" + str(random.randint(111111111,999999999))
        data_arr.append(data)
    for i in range(int(n / 10)):
        data = {}
        data["idOfCrawler"] = 1
        data['name'] = random.choice(items)
        data['price'] = random.randrange(50, 70) + round(random.random(), 3)
        data['count'] = random.randint(1,10)
        data['customer name'] = random.choice(names)
        data['phone number'] = "+79" + str(random.randint(111111111,999999999))
        data_arr.append(data)
    with open('anomaly3.json', 'w') as json_file:
        json.dump(data_arr, json_file)

# Токены поменялись с +7915... на 8(9...
def error4(n):
    data_arr = []
    n = int(n)
    for i in range(n):
        data = {}
        data["idOfCrawler"] = 1
        data['name'] = random.choice(items)
        data['price'] = random.randrange(8, 9) + round(random.random(), 3)
        data['count'] = random.randint(1,10)
        data['customer name'] = random.choice(names)
        data['phone number'] = "+79" + str(random.randint(111111111,999999999))
        data_arr.append(data)
    for i in range(int(n)):
        data = {}
        data["idOfCrawler"] = 1
        data['name'] = random.choice(items)
        data['price'] = random.randrange(8, 9) + round(random.random(), 3)
        data['count'] = random.randint(1,10)
        data['customer name'] = random.choice(names)
        data['phone number'] = "8(9" + str(random.randint(11,99))+')' + str(random.randint(1111111,9999999))
        data_arr.append(data)
    with open('anomaly4.json', 'w') as json_file:
        json.dump(data_arr, json_file)

# Изменение числа item-ов для страницы
def error5(n):
    data_arr = []
    n = int(n)
    for i in range(n):
        data = {}
        data["idOfCrawler"] = 1
        data['name'] = random.choice(items)
        data['price'] = random.randrange(8, 9) + round(random.random(), 3)
        data['count'] = random.randint(1,10)
        data["customer name"] = random.choice(names)
        data['phone number'] = "+79" + str(random.randint(111111111,999999999))
        data_arr.append(data)
    for i in range(int(n / 5)):
        data = {}
        data["idOfCrawler"] = 1
        data['name'] = random.choice(items)
        data['price'] = random.randrange(8, 9) + round(random.random(), 3)
        data['phone number'] = "+79" + str(random.randint(111111111,999999999))
        data_arr.append(data)
    with open('anomaly5.json', 'w') as json_file:
        json.dump(data_arr, json_file)


def noErrors(n):
    data_arr = []
    n = int(n)
    for i in range(n):
        data = {}
        data["idOfCrawler"] = 1
        data['name'] = random.choice(items)
        data['price'] = random.randrange(8, 9) + round(random.random(), 3)
        data['count'] = random.randint(1,10)
        data['customer name'] = random.choice(names)
        data['phone number'] = "+79" + str(random.randint(111111111,999999999))
        data_arr.append(data)
    for i in range(int(n)):
        data = {}
        data["idOfCrawler"] = 1
        data['name'] = random.choice(items)
        data['price'] = random.randrange(8, 9) + round(random.random(), 3)
        data['count'] = random.randint(1,10)
        data['customer name'] = random.choice(names)
        data['phone number'] = "+79" + str(random.randint(111111111,999999999))
        data_arr.append(data)
    with open('noAnomalies.json', 'w') as json_file:
        json.dump(data_arr, json_file)