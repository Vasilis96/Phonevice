from saveandgrab import *
from toolGetters import getDisplaySizeScore,getSiblingIndex
import stage3
#import aTest, aTestFunctions
from scoreFunctions import calcDisplaySizeScore

def start(db,availabilityTable):
	query={"familyID" : {"$in" : [aTuple[0] for aTuple in availabilityTable]}} #creates a table of familyIDs
	devicesDocuments=list(db.specs.find(query))

	getSiblingIndex(devicesDocuments,availabilityTable)
	
	averageDisplaySize=round(float(sum(map(lambda aDevice:aDevice['display']['diagonal'],devicesDocuments))/len(devicesDocuments)),2)
	displayOption={
				1:round(averageDisplaySize-0.2,1),
				2:round(averageDisplaySize,1),
				3:round(averageDisplaySize+0.2,1),
				4:round(averageDisplaySize+0.4,1)
			  }
	
	inputText=f'--- Display size range---\n1: {displayOption[1]}"\n2: {displayOption[2]}"\n3: {displayOption[3]}"\n4: {displayOption[4]}"\nInput (min max): '
	
	while True:
		displaySizeRange=input(inputText)
		minSizeRange,maxSizeRange=None,None
		try:
			inputs=displaySizeRange.split(' ')
			minSizeRange=displayOption[int(inputs[0].strip(' '))]
			maxSizeRange=displayOption[int(inputs[-1].strip(' '))]
		except Exception:
			print('Wrong input ...')
		else:
			if minSizeRange>=maxSizeRange:
				print('Minimum size range must be greater than maximum size range.')
			else:
				break

	ans=int(input('Which algorithm?\nOLD: 0 NEW: 1 '))
	# if ans:
	# 	aTestFunctions.calcDisplaySizeScore(minSizeRange,maxSizeRange,devicesDocuments)
	# 	aTest.start(devicesDocuments)
	# else:
	calcDisplaySizeScore(minSizeRange,maxSizeRange,devicesDocuments)
	stage3.start(db,devicesDocuments)
	

if __name__ == '__main__':
	print('Stage2.py')