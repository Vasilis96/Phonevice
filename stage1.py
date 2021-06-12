import sys 
sys.path.append('C:/Users/Orestes/Desktop/pv/Code/My_Python_Library/')
from saveandgrab import *
from mongoFunctions import getLocalHostConnection
from toolGetters import getFamilies,getAvailableSibling
import stage2


def start():
	minimumDeviceCountFromStage1ToStage2,magicNumber=10,20

	familiesTable,maxBudget,minBudget=getFamilies(prices,budget,fishnetFloor,fishnetRoof,magicNumber,minimumDeviceCountFromStage1ToStage2)
	
	availabilityTable=list(map(lambda x: -1, (i for i in range(0,len(familiesTable)))))
	#availabilityTable: an array the size of the count of documents returned by the stage 1 query initialized with -1 values
	
	for index,aFamily in enumerate(familiesTable):
		availabilityTable[index]=(aFamily['famID'],getAvailableSibling(aFamily,maxBudget)) #(familyID, available siblingID)

	print(f"Entering stage 2 with {len(availabilityTable)} devices in budget range {int(minBudget)}€-{int(maxBudget)}€")
	stage2.start(client.phonevice,availabilityTable)
	

if __name__ == '__main__':
	client=getLocalHostConnection()
	prices=client.phonevice.prices
	
	while True:
		budget=int(input('What\'s your budget?\nInput (0 to exit): '))
		if not budget:
			print('Thank you for using Phonevice! Hope to see you back soon!')
			break
		fishnetRoof,fishnetFloor=budget*0.055,budget*0.75
		start()
		print('\n'*5)
	
	client.close()