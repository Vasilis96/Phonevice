from toolGetters import *
import aTestIdealScores
#Weighted percentage distances

def calcDisplaySizeScore(minDS,maxDS,devices):
	for aDevice in devices:
		
		deviceDS=get_display_size(aDevice)
		
		if minDS<=deviceDS<=maxDS:
			aDevice['displaySizeScore']=0
		else:
			if deviceDS<minDS:
				aDevice['displaySizeScore']=(deviceDS-minDS)*100*5
			else:
				aDevice['displaySizeScore']=(maxDS-deviceDS)*100*5

def calcPPIScore(devicePPI,touGoal):
	idealMinimum=touGoal
	return ((devicePPI-idealMinimum)/idealMinimum)*100 if devicePPI<touGoal else 0

def calcStBScore(deviceStB,touGoal):
	if touGoal<=75: #Gaming
		idealMaximum=touGoal
		return ((idealMaximum-deviceStB)/idealMaximum)*100*2

	idealMinimum=touGoal
	return ((deviceStB-idealMinimum)/idealMinimum)*100

def calcRAMScore(deviceRAM,touGoal):
	idealMinimum=touGoal
	return ((deviceRAM-idealMinimum)/idealMinimum)*100 if deviceRAM<idealMinimum else 0

def calcCapScore(aDevice,touGoal):
	idealMinimum=touGoal
	deviceCap=get_capacity(aDevice)
	if deviceCap<idealMinimum:
		return 0 if hasStorageExpansion(aDevice) else ((deviceCap-idealMinimum)/idealMinimum)*100
	return 0

def calcYearScore(deviceYear):
	currentYear=2019
	return 0 if deviceYear==currentYear else -((currentYear-deviceYear)/10)*100

def calcWeightScore(deviceWeight,touGoal):
	idealMaximum=touGoal
	
	if touGoal>=170: #Gaming
		return ((idealMaximum-deviceWeight)/idealMaximum)*100 if deviceWeight>idealMaximum else 0

	return -float(deviceWeight-idealMaximum)

def calcW20PScore(deviceW20P,touGoal):
	idealMinimum=touGoal
	return ((deviceW20P-idealMinimum)/idealMinimum)*100 if deviceW20P<idealMinimum else 0

def calcW20BScore(deviceW20B,touGoal):
	idealMinimum=touGoal
	return ((deviceW20B-idealMinimum)/idealMinimum)*100*3 if deviceW20B<idealMinimum else 0

def calcSSEScore(deviceSSE,touGoal):
	idealMinimum=touGoal
	return ((deviceSSE-idealMinimum)/idealMinimum)*100 if deviceSSE<idealMinimum else 0

def calcToUScore(aDevice,ToU):
		aDevice['ppiScore']=calcPPIScore(get_ppi(aDevice),ToU['tou_goals']()['ppi'])
		aDevice['stbScore']=calcStBScore(get_stb(aDevice),ToU['tou_goals']()['stb'])
		aDevice['ramScore']=calcRAMScore(get_ram(aDevice),ToU['tou_goals']()['ram'])
		aDevice['capScore']=calcCapScore(aDevice,ToU['tou_goals']()['cap'])
		aDevice['yearScore']=calcYearScore(get_year(aDevice))
		aDevice['weightScore']=calcWeightScore(get_weight(aDevice),ToU['tou_goals']()['weight'])
		aDevice['w20PScore']=calcW20PScore(get_w2_0_score(aDevice),ToU['tou_goals']()['w2_0_score'])
		aDevice['w20BScore']=calcW20BScore(get2_0_battery(aDevice),ToU['tou_goals']()['w2_0_battery'])
		aDevice['sseScore']=calcSSEScore(get_grafix(aDevice),ToU['tou_goals']()['grafix'])
		aDevice['yearScore']=calcYearScore(get_year(aDevice))
		
		aDevice[ToU["name"]]=float(sum(aDevice[aField] for aField in aDevice if 'Score' in aField))
		
		return aDevice[ToU["name"]]



def calcTotalScore(aDevice,typesOfUse,sumOfWeights):

	aDevice['totalPoints']=sum(float(aToU['weight']/sumOfWeights)*calcToUScore(aDevice,typesOfUse[index]) for index,aToU in enumerate(typesOfUse) if typesOfUse[index]['weight']>0)
			
	return aDevice["totalPoints"]



def printDevices(devices):
	for index,aDevice in enumerate(devices):
		print(f'{index+1}.) {aDevice["fullname"]}')
		for aField in aDevice:
			if 'Score' in aField:
				print(f"{aField}:{aDevice[aField]}")
		print(f'Total points: {aDevice["totalPoints"]}\nWork 2.0: {get_w2_0_score(aDevice)}\nBattery 2.0: {get2_0_battery(aDevice,1)} hours\nSling shot score: {get_grafix(aDevice)}\nCapacity: {get_capacity(aDevice)} GB\nDisplay size: {get_display_size(aDevice)}\nStB: {(get_stb(aDevice))}%\nRAM: {get_ram(aDevice)} GB\nPPI: {get_ppi(aDevice)}\nWeight: {get_weight(aDevice)}\nYear: {get_year(aDevice)}\n')
		if index==5:
			break