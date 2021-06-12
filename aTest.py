import sys 
sys.path.append('C:/Users/Orestes/Desktop/pv/Code/My_Python_Library/')
from saveandgrab import *
from mongoFunctions import getLocalHostDB
from toolGetters import *
from aTestFunctions import *
from stage3Weights import checkSumOfWeights
import aTestIdealScores


def start(families):
	typesOfUse=aTestIdealScores.getTypesOfUse()
	sumOfWeights=checkSumOfWeights(sum(aTypeOfUse['weight'] for aTypeOfUse in typesOfUse))
	
	for aDevice in families:
		aDevice['totalScore']=calcTotalScore(aDevice,typesOfUse,sumOfWeights)

	families=sorted(families,key=lambda aDevice: aDevice['totalPoints'],reverse=True)


	printDevices(families)
if __name__ == '__main__':
	print('aTest.py')