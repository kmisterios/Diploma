import json
import random
import string
from flask import flash


# items = ['eggs', 'milk', 'cheese', 'bread', 'porridge']
# names = ['Misha', 'Lena', 'Ivan', 'Nikita', 'Aleksandr', 'Fillip']

# есть поле текст n шагов, а после n+1 - нет

def generate_float(sch, field):
    try:
        return random.randrange(sch["properties"][field]["minimum"], sch["properties"][field]["maximum"]) + round(
            random.random(), 3)
    except:
        return random.randrange(1, 20) + round(random.random(), 3)


def generate_string(sch, field):
    letters = string.ascii_lowercase
    try:
        length = random.randint(sch["properties"][field]["minlength"], sch["properties"][field]["maxlength"])
    except:
        length = random.randint(3, 10)
    return ''.join(random.choice(letters) for i in range(length))


def generate_int(sch, field):
    try:
        return random.randint(sch["properties"][field]["minimum"], sch["properties"][field]["maximum"])
    except:
        return random.randint(0, 15)


def generate_phone_number(sch, err):
    if err == 0:
        return "+79" + str(random.randint(111111111, 999999999))
    else:
        return "8(9" + str(random.randint(11, 99)) + ')' + str(random.randint(1111111, 9999999))


def error1(n, schema):
    data_arr = []
    n = int(n)
    is_sample_strange = []
    for i in range(random.randint(n - 5, n + 5)):
        is_sample_strange.append(0)
        data = {}
        data["idOfCrawler"] = schema["idOfCrawler"]
        for key in schema["properties"].keys():
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
        data_arr.append(data)
    for i in range(int(n)):
        is_sample_strange.append(1)
        data = {}
        data["idOfCrawler"] = schema["idOfCrawler"]
        str_keys = []
        for key in schema["properties"].keys():
            if schema["properties"][key]["type"] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    str_keys.append(key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
        if len(str_keys) > 0:
            for j in range(1, len(str_keys)):
                data[str_keys[j]] = generate_string(schema, str_keys[j])
            data[str_keys[0]] = ''
        else:
            return 0,  is_sample_strange
        data_arr.append(data)
    with open('anomaly1_id_' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
        json.dump(data_arr, json_file)
    return str_keys[0], is_sample_strange


# Текст с вероятнстью P = 58,9% есть, а потом его нет
def error2(n, schema):
    data_arr = []
    n = int(n)
    is_sample_strange = []
    for i in range(random.randint(n - 5, n + 5)):
        is_sample_strange.append(0)
        data = {}
        data["idOfCrawler"] = schema["idOfCrawler"]
        str_keys = []
        for key in schema["properties"].keys():
            if schema["properties"][key]["type"] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    str_keys.append(key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
        if len(str_keys) > 0:
            if len(str_keys) > 1:
                for j in range(2, len(str_keys)):
                    data[str_keys[j]] = generate_string(schema, str_keys[j])
                data[str_keys[0]] = generate_string(schema, str_keys[0])
                if random.random() <= 0.58:
                    data[str_keys[1]] = generate_string(schema, str_keys[1])
                else:
                    data[str_keys[1]] = ''
                error_key = str_keys[1]
            else:
                if random.random() <= 0.58:
                    data[str_keys[0]] = generate_string(schema, str_keys[0])
                else:
                    data[str_keys[0]] = ''
                error_key = str_keys[0]
        else:
            return 0, is_sample_strange
        data_arr.append(data)
    for i in range(int(n)):
        data = {}
        is_sample_strange.append(1)
        data["idOfCrawler"] = schema["idOfCrawler"]
        str_keys = []
        for key in schema["properties"].keys():
            if schema["properties"][key]["type"] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    str_keys.append(key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
        if len(str_keys) > 0:
            if len(str_keys) > 1:
                for j in range(2, len(str_keys)):
                    data[str_keys[j]] = generate_string(schema, str_keys[j])
                data[str_keys[0]] = generate_string(schema, str_keys[0])
                data[str_keys[1]] = ''
                error_key = str_keys[1]
            else:
                data[str_keys[0]] = ''
                error_key = str_keys[0]
        else:
            return 0,  is_sample_strange
        data_arr.append(data)
    with open('anomaly2_id_' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
        json.dump(data_arr, json_file)
    return error_key, is_sample_strange


# Число n раз [8,9], а c n + 1 раза [50,70]
def error3(n, schema):
    data_arr = []
    n = int(n)
    is_sample_strange = []
    count = sum([schema["properties"][key]['type'] == "number" for key in schema["properties"].keys()])
    if count == 0:
        return 0,  is_sample_strange
    for i in range(random.randint(n - 5, n + 5)):
        data = {}
        is_sample_strange.append(0)
        data["idOfCrawler"] = schema["idOfCrawler"]
        for key in schema["properties"].keys():
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
        data_arr.append(data)
    for i in range(n):
        data = {}
        is_sample_strange.append(1)
        data["idOfCrawler"] = schema["idOfCrawler"]
        j = 0
        for key in schema["properties"].keys():
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                if j == 0:
                    data[key] = generate_float(schema, key) * 10
                    j += 1
                    err_field = key
                else:
                    data[key] = generate_float(schema, key)
        data_arr.append(data)
    with open('anomaly3_id_' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
        json.dump(data_arr, json_file)
    return err_field, is_sample_strange


# Токены поменялись с +7915... на 8(9...
def error4(n, schema):
    data_arr = []
    n = int(n)
    is_sample_strange = []
    count = sum([key == "phone number" for key in schema["properties"].keys()])
    if count == 0:
        return 0,  is_sample_strange
    for i in range(random.randint(n - 5, n + 5)):
        data = {}
        is_sample_strange.append(0)
        data["idOfCrawler"] = schema["idOfCrawler"]
        for key in schema["properties"].keys():
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
        data_arr.append(data)
    for i in range(n):
        is_sample_strange.append(1)
        data = {}
        data["idOfCrawler"] = schema["idOfCrawler"]
        for key in schema["properties"].keys():
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 1)
                else:
                    data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
        data_arr.append(data)
    with open('anomaly4_id_' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
        json.dump(data_arr, json_file)
    return 'phone number', is_sample_strange


# Изменение числа item-ов для страницы
def error5(n, schema):
    data_arr = []
    n = int(n)
    is_sample_strange = []
    for i in range(random.randint(n - 5, n + 5)):
        data = {}
        is_sample_strange.append(0)
        data["idOfCrawler"] = schema["idOfCrawler"]
        for key in schema["properties"].keys():
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
        data_arr.append(data)
    for i in range(n):
        is_sample_strange.append(1)
        data = {}
        data["idOfCrawler"] = schema["idOfCrawler"]
        keys_count = len(schema["properties"].keys())
        k = 1
        for key in schema["properties"].keys():
            if k > round(keys_count * 0.5):
                break
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
            k += 1
        data_arr.append(data)
    with open('anomaly5_id_' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
        json.dump(data_arr, json_file)
    return is_sample_strange


def noErrors(n, schema):
    data_arr = []
    n = int(n)
    is_sample_strange = []
    for i in range(2 * n):
        is_sample_strange.append(0)
        data = {}
        data["idOfCrawler"] = schema["idOfCrawler"]
        for key in schema["properties"].keys():
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
        data_arr.append(data)
    with open('noAnomalies_id_' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
        json.dump(data_arr, json_file)
    return is_sample_strange
