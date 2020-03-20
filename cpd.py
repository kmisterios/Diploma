import ruptures as rpt
import json
import numpy as np
from flask import flash

	
def cpd_count(samples, schema, name):
	result = []
	if name == "item":
		numbers = []
		for sample in samples:
			numbers.append(len(sample.keys()))
		numbers = np.array(numbers)
		model = "l1"
		algo = rpt.Pelt(model=model, min_size=1, jump = 1).fit(numbers)
		result = algo.predict(pen = 5) + ['item']
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
					numbers.append(len(sample[key]))
			else:
				return result
		numbers = np.array(numbers)
		if (numbers.min() == numbers.max()) or (key == "phone number"):
			model="l1"
			algo = rpt.Pelt(model=model, min_size=1, jump = 1).fit(numbers)
			result.append(algo.predict(pen=5) + [key])
		else:
			model = "rbf"
			algo = rpt.Pelt(model=model, min_size=1, jump = 1).fit(numbers)
			result.append(algo.predict(pen = 5) + [key])
	return result

