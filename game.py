from GameState import BattleState
from minimax import MinimaxAgent
import random
import math
import copy
import sys

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
venasaur = {'name': 'venasaur', 'moves': {'solarbeam': (120, 'grass', 'special'), 'razor leaf': (55, 'grass', 'special')}, 'stats' : {'hp': 80, 'atk': 82, 'def': 83, 'spe': 80, 'spc': 100}, 'type': ('grass', None)}
venasaur['stats'] = calcStats(venasaur['stats'])


Agent['Pokemon'] = [pikachu, venasaur, charizard]
Opp['Pokemon'] = [pikachu, charizard, venasaur]

state = BattleState(Agent, Opp)

alg = MinimaxAgent(3)
if sys.argv[1] == 'bot':
    while not state.isEnd():
        action, movType = alg.getAction(state)
        state = state.generateSuccessor(1, action, movType)
        print(action, movType)
        if state.isEnd():
            break
        enemy, movType = alg.getEnemyAction(state)
        state = state.generateSuccessor(-1, enemy, movType)
    print('agent: ', state.agent)
    print('opponent: ', state.opp)

else:
    while not state.isEnd():
        print('Your Pokemon')
        for pokemon in state.agent['Pokemon']:
            print(pokemon['name'], " hp: ", pokemon['stats']['hp'])
        print('Opponents Pokemon')
        for pokemon in state.opp['Pokemon']:
            print(pokemon['name'], " hp: ", pokemon['stats']['hp'])
        print("Your active Pokemon: ", state.agent['Pokemon'][state.currAgent]['name'])
        print("Opponent's active Pokemon: ", state.opp['Pokemon'][state.currOpp]['name'])
        actions = state.getLegalActions(1)
        print("possible actions: ", actions)
        action = input("Pick an action: ")
        if action in actions['moves']:
            state = state.generateSuccessor(1, action, 'moves')
        else:
            state = state.generateSuccessor(1, int(action), 'switch')
        if state.isEnd():
            break
        enemy, movType = alg.getEnemyAction(state)
        state = state.generateSuccessor(-1, enemy, movType)
    win = False
    for pokemon in state.agent['Pokemon']:
        if pokemon['stats']['hp'] > 0:
            win = True
    if win:
        print("You Win!")
    else:
        print("You Lose.")
