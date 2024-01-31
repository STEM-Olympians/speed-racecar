import math as m
def generate_logarithmic_growth():
	asdf = []

	for i in range(100):
		val = float(m.log(i+1))
		asdf.append(val)
	return asdf

print(generate_logarithmic_growth())
