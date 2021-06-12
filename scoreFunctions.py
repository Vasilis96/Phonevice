from toolGetters import get_ram,get_capacity,get_w2_0_score,get2_0_battery,get_ppi,get_grafix,get_weight,get_stb,get_year
import numpy as np

def normalize_f(x,min_,max_):
	return float((x-min_)/(max_-min_)) if min_!=max_ else 1

def calcDisplaySizeScore(minSizeRange,maxSizeRange,devicesDocuments):
	scoresTable=[]
	for aDevice in devicesDocuments:
		deviceDisplaySizeScore=0
		if minSizeRange<=aDevice['display']['diagonal']<=maxSizeRange:
			devicedisplaySizeScore=0
		else:
			if aDevice['display']['diagonal']>maxSizeRange:
				deviceDisplaySizeScore=aDevice['display']['diagonal']-maxSizeRange
			else:
				deviceDisplaySizeScore=minSizeRange-aDevice['display']['diagonal']
	
		aDevice['displaySizeScore']=deviceDisplaySizeScore
		scoresTable.append(deviceDisplaySizeScore)
	
	scoresTableSorted=sorted([aScore for aScore in scoresTable])
	maxDisplaySizeScore,minDisplaySizeScore=scoresTableSorted[-1],scoresTableSorted[0]
	
	for aDevice in devicesDocuments:
		aDevice['displaySizeScore']=round(1-normalize_f(aDevice['displaySizeScore'],minDisplaySizeScore,maxDisplaySizeScore),2)

def calcToUScore(aDevice,weights,mins,maxes):

	ram=normalize_f(np.log(get_ram(aDevice)),mins['ram'],maxes['ram']) #RAM score
		
	cap=normalize_f(np.log(get_capacity(aDevice)),mins['cap'],maxes['cap']) #Capacity score
		
	w2_0_score=normalize_f(np.log(get_w2_0_score(aDevice)),mins['w2_0_score'],maxes['w2_0_score']) #Work 2.0 Performance Score
		
	w2_0_battery=normalize_f(np.log(get2_0_battery(aDevice)),mins['w2_0_battery'],maxes['w2_0_battery']) #Work 2.0 Battery Score
			
	ppi=normalize_f(np.log(get_ppi(aDevice)),mins['ppi'],maxes['ppi']) #Pixels per inch score
		
	grafix=normalize_f(np.log(get_grafix(aDevice)),mins['grafix'],maxes['grafix']) #Sling Shot Extreme (OpenGL ES 3.1) Score
		
	weight=normalize_f(np.log(get_weight(aDevice)),mins['weight'],maxes['weight']) #Device weight score, adjusted so that less is better
	
	stb=normalize_f(np.log(get_stb(aDevice)),mins['stb'],maxes['stb']) #Screen to body ratio score
	
	return float(weights['ram']*ram)+float(weights['cap']*cap)+float(weights['w2_0_score']*w2_0_score)+float(weights['w2_0_battery']*w2_0_battery)+float(weights['ppi']*ppi)+float(weights['grafix']*grafix)+float(weights['weight']*weight)+float(weights['stb']*stb)


def normalizeToUScore(aScore,minScore,maxScore): #Normalize Types of Use total score
	return normalize_f(aScore,minScore,maxScore) 


def calcYearScore(aYear,minYear,maxYear):
	return normalize_f(aYear,minYear,maxYear)

def calcTotalScore(displaySizeScore,touScore,yearScore):
	return 0.32*displaySizeScore+0.63*touScore+0.05*yearScore
			#0.30, 0.665, 0.035
if __name__ == '__main__':
	print('stage3ScoreFunctions.py')