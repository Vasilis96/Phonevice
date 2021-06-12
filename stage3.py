import pymongo
from toolGetters import *
from scoreFunctions import calcYearScore,calcToUScore,calcTotalScore,normalizeToUScore

def start(db,devicesTable):
	sum_1_counter(getTypesOfUse(1))
	
	typesOfUse=getTypesOfUse()
	sumOfWeights=checkSumOfWeights(sum(aTypeOfUse['weight'] for aTypeOfUse in typesOfUse))
	
	maxes,mins=getMaxesAndMins(devicesTable)
	
	totalToUScoresArray=[]
	for aDevice in devicesTable:
		aDevice['yearScore']=calcYearScore(get_year(aDevice),mins['year'],maxes['year']) #Release year score
		aDevice['everyToUScore']={aTypeOfUse['name']:float(aTypeOfUse['weight']/sumOfWeights)*calcToUScore(aDevice,aTypeOfUse['tou_weights'](),mins,maxes) for aTypeOfUse in typesOfUse}
		aDevice['totalToUScore']=sum(float(aTypeOfUse['weight']/sumOfWeights)*calcToUScore(aDevice,aTypeOfUse['tou_weights'](),mins,maxes) for aTypeOfUse in typesOfUse) #total ToU score
		
		totalToUScoresArray.append(aDevice['totalToUScore'])
	
	
	minTotalToUScores,maxTotalToUScores=getMinAndMaxTotalToUScores(totalToUScoresArray)
	
	for aDevice in devicesTable:
		aDevice['totalToUScore']=normalizeToUScore(aDevice['totalToUScore'],minTotalToUScores,maxTotalToUScores)
		aDevice['totalScore']=calcTotalScore(aDevice['displaySizeScore'],aDevice['totalToUScore'],aDevice['yearScore'])
	
	devicesTable=sorted(devicesTable,key=lambda aDevice: aDevice['totalScore'],reverse=True) #sorts array based on device score in descending order
	printDevs(db,devicesTable)

if __name__ == '__main__':
	print('stage3.py')