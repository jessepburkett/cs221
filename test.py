from GameState import BattleState
from minimax import MinimaxAgent
import random

#File tests the MinimaxAgent and BattleState class

Agent = {'Pokemon': [], 'currPoke': 0}
Opp = {'Pokemon': [], 'currPoke': 0}

pikachu = {'name': 'pikachu', 'moves': {'thunderbolt': (95, 'electric', 'special'), 'quick attack': (40, 'normal', 'physical')}, 'stats' : {'hp': 35, 'atk': 55, 'def': 30, 'spe': 90, 'spc': 50}, 'type': ('electric', None)}

charizard = {'name': 'charizard', 'moves':{'fire blast':(120, 'fire', 'special'), 'flamethrower':(90, 'fire', 'special')}, 'stats':{'hp':78, 'atk':84, 'def':78, 'spe':100, 'spc':85}, 'type':('fire', 'flying')}

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
action, movtype = alg.getAction(state)
print(action, movtype)
