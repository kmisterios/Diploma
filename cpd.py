import ruptures as rpt
import json
import numpy as np

	
def cpd_count(samples, schema, name):
	keys = []
	result = []
	ttype = []
	for key in schema["properties"].keys():
		if schema["properties"][key]["type"] == name:
			keys.append(key)
	for key in keys:
		numbers = []
		for sample in samples:
			if name == "number":
				numbers.append(sample[key])
			else:	
				numbers.append(len(sample[key]))
		numbers = np.array(numbers)
		ttype.append(type(numbers[0]))
		if ttype[-1] == np.float64:
			model="rbf"
			algo = rpt.Pelt(model=model).fit(numbers)
			result.append(algo.predict(pen=1))
		if ttype[-1] == np.int64:
			model = "l2"
			algo = rpt.Binseg(model=model).fit(numbers)
			result.append(algo.predict(n_bkps=10))
	if name == "number":
		return result, ttype
	else:
		return result

