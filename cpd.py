import ruptures as rpt
import numpy as np
from datetime import datetime, time


def date_str_to_sec(date_str):
    return (datetime.fromisoformat(date_str) - datetime(1970,1,1)).total_seconds()


def time_str_to_sec(time_str):
    t = time.fromisoformat(time_str)
    return t.hour*60*60 + t.minute*60 + t.second + t.microsecond/1000000


def cpd_count(samples, schema, name):
    result = []
    if name == "item":
        numbers = []
        for sample in samples:
            numbers.append(len(sample.keys()))
        numbers = np.array(numbers)
        model = "l1"
        algo = rpt.Pelt(model=model, min_size=1, jump=1).fit(numbers)
        result = algo.predict(pen=5) + ['item']
        return result
    keys = []
    for key in schema["properties"].keys():
        if schema["properties"][key]["type"] == name:
            keys.append(key)
    for key in keys:
        numbers = []
        for sample in samples:
            if key in sample.keys():
                if name == "number" or name == "integer":
                    numbers.append(sample[key])
                else:
                    try:
                        numbers.append(date_str_to_sec(sample[key]))
                    except ValueError:
                        try:
                            numbers.append(time_str_to_sec(sample[key]))
                        except ValueError:
                            numbers.append(len(sample[key]))
            else:
                return result
        numbers = np.array(numbers)
        if (numbers.min() == numbers.max()) or (key == "phone number"):
            model = "l1"
            algo = rpt.Pelt(model=model, min_size=1, jump=1).fit(numbers)
            result.append(algo.predict(pen=5) + [key])
        else:
            model = "rbf"
            algo = rpt.Pelt(model=model, min_size=1, jump=1).fit(numbers)
            result.append(algo.predict(pen=5) + [key])
    return result

