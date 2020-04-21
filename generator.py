import json
import random
import string
import exrex
from datetime import datetime, time
from datetime import timedelta


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


#-------------------------------------------------------------------------------------------------------------------
#for date and time
def add_re_for_formats(schema):
    if schema["properties"]["date"]["format"] == "date" or schema["properties"]["date"]["format"] == "date-time":
        schema["properties"]["date"]["pattern"] = "^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$"

    if schema["properties"]["date"]["format"] == "time":
        schema["properties"]["date"]["pattern"] = "([0-9]{2}:){2}[0-9]{2}"


def get_random_date():
    try:
        date1 = exrex.getone('(0[1-9]|1[0-9]|2[0-9]|3[0-1])-(0[1-9]|1[0-2])-20(1[0-9]|0[1-9])')
        d = datetime.strptime(date1, '%d-%m-%Y').isoformat()
        return d
    except ValueError:
        get_random_date()


def get_random_time():
    time1 = exrex.getone('(0[1-9]|1[0-9]|2[0-3]):(0[1-9]|[1-5][0-9]):(0[1-9]|[1-5][0-9])')
    return time.fromisoformat(time1)


def get_random_datetime():
    try:
        date1 = exrex.getone('(0[1-9]|1[0-9]|2[0-3]):(0[1-9]|[1-5][0-9]):(0[1-9]|[1-5][0-9]) (0[1-9]|1[0-9]|2[0-9]|3[0-1])-(0[1-9]|1[0-2])-20(1[0-9]|0[1-9])')
        d = datetime.strptime(date1, '%H:%M:%S %d-%m-%Y')
        return d.isoformat()
    except ValueError:
        get_random_datetime()


def get_random_bigger_date(start, delta):
    end = start + timedelta(days=delta)
    deltta = end - start
    int_delta = (deltta.days * 24 * 60 * 60) + deltta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def generate_datetime(sch, item, delta, start=''):
    if sch["properties"][item]["format"] == "date":
        if delta == 0:
            return get_random_date()
        else:
            if start != '':
                start = datetime.fromisoformat(start)
                return get_random_bigger_date(start, delta).isoformat()
            else:
                return get_random_date()

    if sch["properties"][item]["format"] == "time":
        return get_random_time().isoformat()

    if sch["properties"][item]["format"] == "date-time":
        if delta == 0:
            return get_random_datetime()
        else:
            if start != '':
                start = datetime.fromisoformat(start)
                return get_random_bigger_date(start, delta).isoformat()
            else:
                return get_random_datetime()


#--------------------------------------------------------------------------------------------------------------


def error1(n, schema):
    try:
        with open('collection' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
    except FileNotFoundError:
        sampi = noErrors(n, schema)
        with open('noAnomalies_id_' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
        with open('collection' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
            json.dump(samples_collection, json_file)
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
                    try:
                        check = schema["properties"][key]['format']
                        schema1 = schema
                        add_re_for_formats(schema1)
                        try:
                            data[key] = generate_datetime(schema1, key, 2, data_arr[-1][key])
                        except IndexError:
                            data[key] = generate_datetime(schema1, key, 2, samples_collection[-1][key])
                    except KeyError:
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
                try:
                    check = schema["properties"][key]['format']
                    schema1 = schema
                    add_re_for_formats(schema1)
                    try:
                        data[key] = generate_datetime(schema1, str_keys[j], 2, data_arr[-1][str_keys[j]])
                    except IndexError:
                        data[key] = generate_datetime(schema1, key, 2, samples_collection[-1][key])
                except KeyError:
                    data[key] = generate_string(schema, str_keys[j])
            data[str_keys[0]] = ''
        else:
            return 0,  is_sample_strange
        data_arr.append(data)
    with open('anomaly1_id_' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
        json.dump(data_arr, json_file)
    return str_keys[0], is_sample_strange


# Текст с вероятнстью P = 58,9% есть, а потом его нет
def error2(n, schema):
    try:
        with open('collection' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
    except FileNotFoundError:
        sampi = noErrors(n, schema)
        with open('noAnomalies_id_' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
        with open('collection' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
            json.dump(samples_collection, json_file)
    data_arr = []
    n = int(n)
    is_sample_strange = []
    m = random.randint(n - 5, n + 5)
    for i in range(m):
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
                    try:
                        print(schema["properties"][str_keys[j]]['format'])
                        schema1 = schema
                        add_re_for_formats(schema1)
                        try:
                            data[str_keys[j]] = generate_datetime(schema1, str_keys[j], 2, data_arr[-1][str_keys[j]])
                        except IndexError:
                            data[str_keys[j]] = generate_datetime(schema1, str_keys[j], 2, samples_collection[-1][str_keys[j]])
                    except KeyError:
                        data[str_keys[j]] = generate_string(schema, str_keys[j])

                try:
                    print(schema["properties"][str_keys[0]]['format'])
                    schema1 = schema
                    add_re_for_formats(schema1)
                    try:
                        data[str_keys[0]] = generate_datetime(schema1, str_keys[0], 2, data_arr[-1][str_keys[0]])
                    except IndexError:
                        data[str_keys[0]] = generate_datetime(schema1, str_keys[0], 2, samples_collection[-1][str_keys[0]])
                except KeyError:
                    data[str_keys[0]] = generate_string(schema, str_keys[0])

                if random.random() <= 0.58:
                    try:
                        print(schema["properties"][str_keys[1]]['format'])
                        schema1 = schema
                        add_re_for_formats(schema1)
                        try:
                            data[str_keys[1]] = generate_datetime(schema1, str_keys[1], 2, data_arr[-1][str_keys[1]])
                        except IndexError:
                            data[str_keys[1]] = generate_datetime(schema1, str_keys[1], 2, samples_collection[-1][str_keys[1]])
                    except KeyError:
                        data[str_keys[1]] = generate_string(schema, str_keys[1])
                else:
                    data[str_keys[1]] = ''
                error_key = str_keys[1]
            else:
                if random.random() <= 0.58:
                    try:
                        print(schema["properties"][str_keys[0]]['format'])
                        schema1 = schema
                        add_re_for_formats(schema1)
                        try:
                            data[str_keys[0]] = generate_datetime(schema1, str_keys[0], 2, data_arr[-1][str_keys[0]])
                        except IndexError:
                            data[str_keys[0]] = generate_datetime(schema1, str_keys[0], 2, samples_collection[-1][str_keys[0]])
                    except KeyError:
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
                    try:
                        print(schema["properties"][str_keys[j]]['format'])
                        schema1 = schema
                        add_re_for_formats(schema1)
                        try:
                            data[str_keys[j]] = generate_datetime(schema1, str_keys[j], 2, data_arr[-1][str_keys[j]])
                        except IndexError:
                            data[str_keys[j]] = generate_datetime(schema1, str_keys[j], 2, samples_collection[-1][str_keys[j]])
                    except KeyError:
                        data[str_keys[j]] = generate_string(schema, str_keys[j])

                try:
                    print(schema["properties"][str_keys[0]]['format'])
                    schema1 = schema
                    add_re_for_formats(schema1)
                    try:
                        data[str_keys[0]] = generate_datetime(schema1, str_keys[0], 2, data_arr[-1][str_keys[0]])
                    except IndexError:
                        data[str_keys[0]] = generate_datetime(schema1, str_keys[0], 2, samples_collection[-1][str_keys[0]])
                except KeyError:
                    data[str_keys[0]] = generate_string(schema, str_keys[0])
                data[str_keys[1]] = ''
                error_key = str_keys[1]
            else:
                data[str_keys[0]] = ''
                error_key = str_keys[0]
        else:
            return 0,  is_sample_strange
        data_arr.append(data)

    k = m - 1
    while data_arr[k][error_key] == '':
        is_sample_strange[k] = 1
        k = k - 1

    with open('anomaly2_id_' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
        json.dump(data_arr, json_file)
    return error_key, is_sample_strange


# Число n раз [8,9], а c n + 1 раза [50,70]
def error3(n, schema):
    try:
        with open('collection' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
    except FileNotFoundError:
        sampi = noErrors(n, schema)
        with open('noAnomalies_id_' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
        with open('collection' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
            json.dump(samples_collection, json_file)
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
                    try:
                        print(schema["properties"][key]['format'])
                        schema1 = schema
                        add_re_for_formats(schema1)
                        try:
                            data[key] = generate_datetime(schema1, key, 2, data_arr[-1][key])
                        except IndexError:
                            data[key] = generate_datetime(schema1, key, 2, samples_collection[-1][key])
                    except KeyError:
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
                    try:
                        print(schema["properties"][key]['format'])
                        schema1 = schema
                        add_re_for_formats(schema1)
                        try:
                            data[key] = generate_datetime(schema1, key, 2, data_arr[-1][key])
                        except IndexError:
                            data[key] = generate_datetime(schema1, key, 2, samples_collection[-1][key])
                    except KeyError:
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
    try:
        with open('collection' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
    except FileNotFoundError:
        sampi = noErrors(n, schema)
        with open('noAnomalies_id_' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
        with open('collection' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
            json.dump(samples_collection, json_file)
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
                    try:
                        print(schema["properties"][key]['format'])
                        schema1 = schema
                        add_re_for_formats(schema1)
                        try:
                            data[key] = generate_datetime(schema1, key, 2, data_arr[-1][key])
                        except IndexError:
                            data[key] = generate_datetime(schema1, key, 2, samples_collection[-1][key])
                    except KeyError:
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
                    try:
                        print(schema["properties"][key]['format'])
                        schema1 = schema
                        add_re_for_formats(schema1)
                        try:
                            data[key] = generate_datetime(schema1, key, 2, data_arr[-1][key])
                        except IndexError:
                            data[key] = generate_datetime(schema1, key, 2, samples_collection[-1][key])
                    except KeyError:
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
    try:
        with open('collection' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
    except FileNotFoundError:
        sampi = noErrors(n, schema)
        with open('noAnomalies_id_' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
        with open('collection' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
            json.dump(samples_collection, json_file)
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
                    try:
                        print(schema["properties"][key]['format'])
                        schema1 = schema
                        add_re_for_formats(schema1)
                        try:
                            data[key] = generate_datetime(schema1, key, 2, data_arr[-1][key])
                        except IndexError:
                            data[key] = generate_datetime(schema1, key, 2, samples_collection[-1][key])
                    except KeyError:
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
                    try:
                        print(schema["properties"][key]['format'])
                        schema1 = schema
                        add_re_for_formats(schema1)
                        try:
                            data[key] = generate_datetime(schema1, key, 2, data_arr[-1][key])
                        except IndexError:
                            data[key] = generate_datetime(schema1, key, 2, samples_collection[-1][key])
                    except KeyError:
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


def error6(n, schema):
    try:
        with open('collection' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
    except FileNotFoundError:
        sampi = noErrors(n, schema)
        with open('noAnomalies_id_' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
        with open('collection' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
            json.dump(samples_collection, json_file)
    data_arr = []
    n = int(n)
    is_sample_strange = []
    error_key = 0
    for i in range(random.randint(n - 5, n + 5)):
        data = {}
        is_sample_strange.append(0)
        data["idOfCrawler"] = schema["idOfCrawler"]
        for key in schema["properties"].keys():
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    try:
                        print(schema["properties"][key]['format'])
                        schema1 = schema
                        add_re_for_formats(schema1)
                        try:
                            data[key] = generate_datetime(schema1, key, 2, data_arr[-1][key])
                        except IndexError:
                            data[key] = generate_datetime(schema1, key, 2, samples_collection[-1][key])
                    except KeyError:
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
        for key in schema["properties"].keys():
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    try:
                        print(schema["properties"][key]['format'])
                        error_key = key
                        schema1 = schema
                        add_re_for_formats(schema1)
                        while 1:
                            d = generate_datetime(schema1, key, 0)
                            if d is not None:
                                print(d)
                                data[key] = d
                                break
                    except KeyError:
                        data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
        data_arr.append(data)
    with open('anomaly6_id_' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
        json.dump(data_arr, json_file)
    return error_key, is_sample_strange


def noErrors(n, schema):
    no_collection = False
    try:
        with open('collection' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
    except FileNotFoundError:
        no_collection = True
    data_arr = []
    n = int(n)
    n = 25
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
                    try:
                        print(schema["properties"][key]['format'])
                        schema1 = schema
                        add_re_for_formats(schema1)
                        try:
                            data[key] = generate_datetime(schema1, key, 2, data_arr[-1][key])
                        except IndexError:
                            if no_collection:
                                data[key] = generate_datetime(schema1, key, 0)
                            else:
                                data[key] = generate_datetime(schema1, key, 2, samples_collection[-1][key])
                    except KeyError:
                        data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
        data_arr.append(data)
    with open('noAnomalies_id_' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
        json.dump(data_arr, json_file)
    return is_sample_strange
