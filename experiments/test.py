def recursive(num: int):
	if num <= 10:
		recursive(num+1)
	else:
		print(num)

recursive(0)
