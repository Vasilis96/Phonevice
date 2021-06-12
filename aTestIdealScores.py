def videoStreamingGoals():
	return {'w2_0_score':5500,
			'ppi':480,
			'w2_0_battery':11,
			'stb':82.0,
			'weight':150,
			'ram':6,
			'cap':64,
			'grafix':900
			}


def gamingGoals():
	return {'w2_0_score':5500,
			'ppi':500,
			'w2_0_battery':11,
			'stb':74,
			'weight':175,
			'ram':8,
			'cap':128,
			'grafix':4000
			}

def socialNetworkingGoals():
	return {'w2_0_score':6500,
			'ppi':430,
			'w2_0_battery':11,
			'stb':82.0,
			'weight':150,
			'ram':8,
			'cap':64,
			'grafix':800
			}

def basicUseGoals():
	return {'w2_0_score':6000,
			'ppi':380,
			'w2_0_battery':12,
			'stb':80.0,
			'weight':150,
			'ram':6,
			'cap':64,
			'grafix':700
			}

def getTypesOfUse(check=0):
	#when check=1, the function returns every type of use with 0 user weight in order for
	#sum_1_counter to check that each type of use total sum of weights equals to 1
	#The particular check should not be included in the final product, it is only meant for testing purposes

	vs,sn,g,b=0,0,0,0
	if not check:
		ans=input('Basic or custome use?\nInput (B or C): ')
		if ans.lower()=='c':
			vs=int(input('Video streaming weight\nInput (0-4): '))
			sn=int(input('Social Networking weight\nInput (0-4): '))
			g=int(input('Gaming weight\nInput (0-4): '))
			print('\n')
		else:
			b=4
	
	#Weights: 0:Unimportant 1: Slightly important 2:Relatively important 3:Very important 4:Top importance!
	return [
			{'name':'Video Streaming','tou_goals':videoStreamingGoals, 'weight':vs},
			{'name':'Social Networking','tou_goals':socialNetworkingGoals, 'weight':sn},
			{'name':'Gaming','tou_goals':gamingGoals, 'weight':g},
			
			{'name':'Basic','tou_goals':basicUseGoals, 'weight':b}
		]