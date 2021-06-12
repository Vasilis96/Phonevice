#weights change from here
def videostreaming_weights():
	return {'w2_0_score':0.01,
			 'ppi':0.14,
			 'w2_0_battery':0.20,
			 'stb':0.22,
			 'weight':-0.18,
			 'ram':0.07,
			 'cap':0.04,
			 'grafix':0.14
			}


def gaming_weights():
	return {'w2_0_score':0.01,
			'ppi':0.17,
			'w2_0_battery':0.19,
			'stb':-0.13,
			'weight':-0.17,
			'ram':0.08,
			'cap':0.05,
			'grafix':0.20
			}

def socialnetworking_weights():
	return {'w2_0_score':0.03,
			'ppi':0.11,
			'w2_0_battery':0.22,
			'stb':0.17,
			'weight':-0.23,
			'ram':0.11,
			'cap':0.04,
			'grafix':0.10
			}

def batteryoriented_weights():
	return {'w2_0_score':0.07,
			'ppi':0.10,
			'w2_0_battery':0.25,
			'stb':0.18,
			'weight':-0.17,
			'ram':0.10,
			'cap':0.03,
			'grafix':0.10
			}


#tests if sum of function weights is equal to 1 or within the predefined freedom margin 
def sum_1_counter(typesOfUse):
	print('--- SUM OF WEIGHTS <=1 TEST! ---')
	for aTypeOfUse in typesOfUse:
		check=sum(avalue if avalue>0 else -avalue for avalue in aTypeOfUse['tou_weights']().values())

		if check<0.99 or check>1.01:
			raise ValueError(f'Sum of weights must be equal to 1.0. Current sum of {aTypeOfUse["name"]} ToU: {check}')
		print(f'OK! Sum of {aTypeOfUse["name"]} weights: {check}\n')
	print('-'*20)

def checkSumOfWeights(sumOfWeights):
	if sumOfWeights>12 or sumOfWeights<=0:
		raise ValueError(f'Sum of Types of Use weights must be less than or equal to 12 and greater than 0.\nCurrent sum: {sumOfWeights}')
	return sumOfWeights


if __name__ == '__main__':
	print('stage3Weights.py')