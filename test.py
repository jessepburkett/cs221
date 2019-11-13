from GameState import BattleState
from minimax import MinimaxAgent
import random
import math
import copy

#File tests the MinimaxAgent and BattleState class

MAX_IV = 15
MAX_EV = 65535
LEVEL = 100

def calcStats(baseStats):
	realStats = baseStats
	for stat in baseStats.keys():
		newStat = math.floor(((MAX_IV + baseStats[stat])*2 + math.floor(math.ceil(math.sqrt(MAX_EV))/4))*LEVEL/100) + 5
		if stat == 'hp':
			newStat += LEVEL + 5
		realStats[stat] = newStat
	return realStats

Agent = {'Pokemon': [], 'currPoke': 0}
Opp = {'Pokemon': [], 'currPoke': 0}

pikachu = {'name': 'pikachu', 'moves': {'thunderbolt': (95, 'electric', 'special'), 'quick attack': (40, 'normal', 'physical')}, 'stats' : {'hp': 35, 'atk': 55, 'def': 30, 'spe': 90, 'spc': 50}, 'type': ('electric', None)}
pikachu['stats'] = calcStats(pikachu['stats'])
charizard = {'name': 'charizard', 'moves':{'fire blast':(120, 'fire', 'special'), 'flamethrower':(90, 'fire', 'special')}, 'stats':{'hp':78, 'atk':84, 'def':78, 'spe':100, 'spc':85}, 'type':('fire', 'flying')}
charizard['stats'] = calcStats(charizard['stats'])

Agent['Pokemon'] = [pikachu, charizard]
Opp['Pokemon'] = [charizard, pikachu]

state = BattleState(Agent, Opp)

'''
#test isEnd
if state.isEnd():
    print('hell yeah')
else:
    print('hell no')


#test getLegalActions
print(state.getLegalActions(1))

#test generateSuccessor
newState = state.generateSuccessor(1, 1, 'switch')
print(newState.currAgent)

newState = state.generateSuccessor(1, 'thunderbolt', 'moves')
print(newState.opp)
'''
#test minimax agent
alg = MinimaxAgent(2)
#action, movtype = alg.getAction(state)


while not state.isEnd():
	minimaxState = state
	action, movtype = alg.getAction(minimaxState)
	#print(action, movtype)
	state = state.generateSuccessor(alg.index, action, movtype)
	print(state.agent, state.opp)
