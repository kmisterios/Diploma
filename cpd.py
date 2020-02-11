import ruptures as rpt
import json
import numpy as np

def cpd_num(samples, schema):
	for key in schema["properties"].keys():
		if schema["properties"][key]["type"] == "number":
			break
	numbers = []
	for sample in samples:
		numbers.append(sample[key])
	numbers = np.array(numbers)
	model="rbf"
	algo = rpt.Pelt(model=model).fit(prices)
	result = algo.predict(pen=0.5)
	return result
	
def cpd_len(samples, schema):
	for key in schema["properties"].keys():
		if schema["properties"][key]["type"] == "string":
			break
	numbers = []
	for sample in samples:
		numbers.append(sample[key])
	numbers = np.array(numbers)
	model="rbf"
	algo = rpt.Pelt(model=model).fit(prices)
	result = algo.predict(pen=0.5)
	return result
	
