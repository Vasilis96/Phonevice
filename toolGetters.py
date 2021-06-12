import numpy as np
from stage3Weights import *
import sys 
sys.path.append('C:/Users/Orestes/Desktop/pv/Code/My_Python_Library/')
import photosManager
#getters for everything used in the tool

#STAGE 1

def getFamilies(prices,budget,fishnetFloor,fishnetRoof,magicNumber,minimumDeviceCountFromStage1ToStage2):
	maxBudget, minBudget=budget+fishnetRoof, fishnetFloor
	
	while True:
		query={"allFamilyPrices":{'$elemMatch': {'$gte': minBudget,'$lte': maxBudget}}}
		families=list(prices.find(query))
		
		if len(families)>=minimumDeviceCountFromStage1ToStage2:
			return families,maxBudget,minBudget

		maxBudget+=budget/magicNumber
		if minBudget>0:
			minBudget-=budget/magicNumber if minBudget-budget/magicNumber>=0 else 0

def getAvailableSibling(aFamily,maxBudget):
	for aSibling in aFamily['siblings'][-1::-1]: #traversing siblings array from the strongest to the weakest, [weakestSibling, ... ,strongestSibling]
			if aSibling['prices'][0]<=maxBudget:
				return aSibling['siblingID']
	
	return -1 #if -1 is returned, then something is definitely wrong


#//////////////////////
def getDisplaySizeScore(familyID,displaySizeScores):
	for aDict in displaySizeScores:
		if aDict['familyID']==familyID:
			return aDict['displaySizeScore']


def getSiblingIndex(devicesDocuments,availabilityTable):
	for aDevice in devicesDocuments:
		for aTuple in availabilityTable:
			if aTuple[0]==aDevice['familyID']:
				aDevice['siblingIndex']=aTuple[-1]
	
def get_ram(adevice):
	return adevice['storage_ram_editions_gbs'][adevice['siblingIndex']][-1]

def get_capacity(adevice):
	return adevice['storage_ram_editions_gbs'][adevice['siblingIndex']][0]
	

def get_w2_0_score(adevice): 
	return adevice['benchmarks']['PCMA_WORK_V2_DEFAULT']['score']

def get2_0_battery(adevice,print_=0):
	benchmark=adevice['benchmarks']['PCMA_WORK_V2_DEFAULT']['work_2_0_battery_life']
	if not print_:
		return benchmark
	hours,minutes=float(str(benchmark).split('.')[0]),float(f"0.{str(benchmark).split('.')[-1]}")
	minutesAsAPerc=minutes/0.60
	batteryWithMinutesNormalized=hours+minutesAsAPerc
	return batteryWithMinutesNormalized


def get_ppi(adevice):
	return adevice['display']['ppi']

def get_grafix(adevice):
	return adevice['benchmarks']['SLING_SHOT_ES_31']['score']
		

def get_display_size(adevice):
	return adevice['display']['diagonal']

def get_weight(adevice):
	return adevice['weight']

def get_stb(adevice):
	return adevice['display']['StB']

def get_dev_name(adevice):
	return adevice['fullname']

def get_year(adevice):
	return adevice['year']

#\\\\\\\ features getters

def hasStorageExpansion(aDevice):
	return 1 if aDevice['storage']['expansion'] else 0


#\\\\\\\\\
#get_avg functions return respective feature's average and standard deviation for a given device sample

def get_avg_battery_life(devicesTable):
	return sum(get2_0_battery(adevice) for adevice in devicesTable)/len(devicesTable),np.std(tuple(get2_0_battery(adevice)for adevice in devicesTable),dtype=np.float64)

def get_avg_slingshot(devicesTable):
	return sum(get_grafix(adevice) for adevice in devicesTable)/len(devicesTable),np.std(tuple(get_grafix(adevice)for adevice in devicesTable),dtype=np.float64)

def get_avg_performance(devicesTable):
	return sum(get_w2_0_score(adevice) for adevice in devicesTable)/len(devicesTable),np.std(tuple(get_w2_0_score(adevice)for adevice in devicesTable),dtype=np.float64)

def get_avg_ppi(devicesTable):
	return sum(get_ppi(adevice) for adevice in devicesTable)/len(devicesTable),np.std(tuple(get_ppi(adevice)for adevice in devicesTable),dtype=np.float64)

def get_avg_dis(devicesTable):
	return sum(get_display_size(adevice) for adevice in devicesTable)/len(devicesTable),np.std(tuple(get_display_size(adevice)for adevice in devicesTable),dtype=np.float64)

def get_avg_weight(devicesTable):
	return sum(get_weight(adevice) for adevice in devicesTable)/len(devicesTable),np.std(tuple(get_weight(adevice)for adevice in devicesTable),dtype=np.float64)

def get_avg_stb(devicesTable):
	return sum(get_stb(adevice) for adevice in devicesTable)/len(devicesTable),np.std(tuple(get_stb(adevice)for adevice in devicesTable),dtype=np.float64)

def get_avg_ram(devicesTable):
	return sum(get_ram(adevice) for adevice in devicesTable)/len(devicesTable),np.std(tuple(get_ram(adevice)for adevice in devicesTable),dtype=np.float64)

def get_avg_cap(devicesTable):
	return sum(get_capacity(adevice) for adevice in devicesTable)/len(devicesTable),np.std(tuple(get_capacity(adevice)for adevice in devicesTable),dtype=np.float64)

#\\\\\\\\\
#returns two dictionaries: maxes contains each features max values from a given device sample. mins contains...
def getMaxesAndMins(devicesTable):

	ramArray=sorted([get_ram(adevice) for adevice in devicesTable])
	capArray=sorted([get_capacity(adevice) for adevice in devicesTable])
	w2_0_scoreArray=sorted([get_w2_0_score(adevice) for adevice in devicesTable])
	w2_0_batteryArray=sorted([get2_0_battery(adevice) for adevice in devicesTable])
	ppiArray=sorted([get_ppi(adevice) for adevice in devicesTable])
	stbArray=sorted([get_stb(adevice) for adevice in devicesTable])
	grafixArray=sorted([get_grafix(adevice) for adevice in devicesTable])
	weightArray=sorted([get_weight(adevice) for adevice in devicesTable])
	yearArray=sorted([get_year(adevice) for adevice in devicesTable])

	maxes={ 'ram':np.log(ramArray[-1]),
			'cap':np.log(capArray[-1]),
			'w2_0_score':np.log(w2_0_scoreArray[-1]), 
			'w2_0_battery':np.log(w2_0_batteryArray[-1]),
			'ppi':np.log(ppiArray[-1]), 
			'stb':np.log(stbArray[-1]),
			'grafix':np.log(grafixArray[-1]), 
			'weight':np.log(weightArray[-1]),
			'year':yearArray[-1]
			}
	
	mins={ 'ram':np.log(ramArray[0]),
			'cap':np.log(capArray[0]),
			'w2_0_score':np.log(w2_0_scoreArray[0]), 
			'w2_0_battery':np.log(w2_0_batteryArray[0]),
			'ppi':np.log(ppiArray[0]), 
			'stb':np.log(stbArray[0]),
			'grafix':np.log(grafixArray[0]), 
			'weight':np.log(weightArray[0]),
			'year':yearArray[0]
			}

	return maxes,mins

#necessary for the types of use total score normalization process
def getMinAndMaxTotalToUScores(table):
	sortedTable=sorted(table)
	return sortedTable[0],sortedTable[-1]


#\\\\\\\\\


#returns a table containing the dict objects which contain each ToU's necessary information
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
		else:
			b=4
	
	#Weights: 0:Unimportant 1: Slightly important 2:Relatively important 3:Very important 4:Top importance!
	return [
			{'name':'Video Streaming','tou_weights':videostreaming_weights, 'weight':vs},
			{'name':'Social Networking','tou_weights':socialnetworking_weights, 'weight':sn},
			{'name':'Gaming','tou_weights':gaming_weights, 'weight':g},
			
			{'name':'Basic','tou_weights':batteryoriented_weights, 'weight':b}
		]

#\\\\\\\\\\\\

#stage 3 print
def printDevs(db,devicesTable):
	print(f'Average W2.0 Performance: {get_avg_performance(devicesTable)}\nAverage Sling Shot:{get_avg_slingshot(devicesTable)}\nAverage RAM: {get_avg_ram(devicesTable)}\nAverage weight: {get_avg_weight(devicesTable)}\nAverage battery life: {get_avg_battery_life(devicesTable)}\nAverage display size: {get_avg_dis(devicesTable)}\nAverage PPI: {get_avg_ppi(devicesTable)}\nAverage STB {get_avg_stb(devicesTable)}\nAverage capacity: {get_avg_cap(devicesTable)}\n')
	photos=db.photos
	for index,aDevice in enumerate(devicesTable):
		print(f'{index+1}.) {aDevice["fullname"]} Score: {round(aDevice["totalScore"]*100,3)}%\nToU score: {round(aDevice["totalToUScore"]*100,3)}%\nDisplay size score: {round(aDevice["displaySizeScore"]*100,3)}%\nYear score: {round(aDevice["yearScore"]*100,3)}%\nWork 2.0: {get_w2_0_score(aDevice)}\nBattery 2.0: {get2_0_battery(aDevice,1)} hours\nSling shot score: {get_grafix(aDevice)}\nCapacity: {get_capacity(aDevice)} GB\nDisplay size: {get_display_size(aDevice)}\nStB: {(get_stb(aDevice))}%\nRAM: {get_ram(aDevice)} GB\nPPI: {get_ppi(aDevice)}\nWeight: {get_weight(aDevice)}\nYear: {get_year(aDevice)}')	
		for aToU,touScore in aDevice['everyToUScore'].items():
			print(f"{aToU}: {round(touScore*100,3)}%")
		#printPhotos(photos,aDevice)
		if index==8: break #prints first X devices

#Print first photo for each device
def printPhotos(photos,aDevice):
	photoDocument=photos.find_one({'dsID':aDevice['dsURL'].split('/')[-1]})
	if photoDocument:
		photosManager.openWPV(photoDocument['photos'][0]['photo'])
		photosManager.killWPV()
	

if __name__ == '__main__':
	print('Stage 3 getters')