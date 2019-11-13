# This is the Game State class, which takes in the game and can describe the information in that state

import copy
import math

'''
Agent = {'Pokemon': [], 'currPoke': 0}
Opp = {'Pokemon': [], 'currPoke': 0}

pikachu = {'name': 'pikachu', 'moves': {'thunderbolt': (95, 'electric', 'special'), 'quick attack': (40, 'normal', 'physical')}, 'stats' : {'hp': 35, 'atk': 55, 'def': 30, 'spe': 90, 'spc': 50}, 'type': ('electric', None)}

charizard = {'name': 'charizard', 'moves':{'fire blast':(120, 'fire', 'special'), 'flamethrower':(90, 'fire', 'special')}, 'stats':{'hp':78, 'atk':84, 'def':78, 'spe':100, 'spc':85}, 'type':('fire', 'flying')}

Agent['Pokemon'] = [pikachu, charizard]
Opp['Pokemon'] = [charizard, pikachu]
'''
import math

LEVEL = 100

class BattleState:
    #state includes an agent list, opponent list, agent current pokemon(denoted by integer), and opponent current pokemon
    #(denoted by integer)
    def __init__(self, agent, opp, currAgent=0, currOpp=0):
        self.agent = agent
        self.opp = opp
        self.currAgent = currAgent
        self.currOpp = currOpp
        self.effectiveness = {
            'normal':{'rock':0.5, 'ghost':0.0},
            'fire':{'rock':0.5, 'fire':0.5, 'water':0.5, 'grass':2.0, 'ice':2.0, 'bug':2.0, 'dragon':0.5},
            'water':{'fire':2.0, 'water':0.5, 'grass':0.5, 'ground':2.0, 'rock':2.0, 'dragon':0.5},
            'electric':{'water':2.0, 'electric':0.5, 'grass':0.5, 'ground':0.0, 'flying':2.0, 'dragon':0.5},
            'grass':{'fire':0.5, 'water':2.0, 'grass':0.5, 'poison':0.5, 'ground':2.0, 'flying':0.5, 'bug':0.5, 'rock':2.0, 'dragon':0.5},
            'ice':{'water':0.5, 'grass':2.0, 'ice':0.5, 'ground':2.0, 'flying':2.0, 'dragon':2.0},
            'fighting':{'normal':2.0, 'ice':2.0, 'poison':0.5, 'flying':0.5, 'psychic':0.5, 'bug':0.5, 'rock':2.0, 'ghost':0.0},
            'poison':{'grass':2.0, 'poison':0.5, 'ground':0.5, 'bug':2.0, 'rock':0.5, 'ghost':0.5},
            'ground':{'fire':2.0, 'electric':2.0, 'grass':0.5, 'poison':2.0, 'flying':0.0, 'bug':0.5, 'rock':2.0},
            'flying':{'electric':0.5, 'grass':2.0, 'fighting':2.0, 'bug':2.0, 'rock':0.5},
            'psychic':{'fighting':2.0, 'poison':2.0, 'psychic':0.5},
            'bug':{'fire':0.5, 'grass':2.0, 'fighting':0.5, 'poison':2.0, 'flying':0.5, 'psychic':2.0},
            'rock':{'fire':2.0, 'ice':2.0, 'fighting':0.5, 'ground':0.5, 'flying':2.0, 'bug':2.0},
            'ghost':{'normal':0.0, 'psychic':0.0, 'ghost':2.0},
            'dragon':{'dragon':2.0}
        }

    
    #determines if any player (agent or opp) has all their pokemon at 0 health
    def isEnd(self):
        agent = True
        opp = True
        for i in range(len(self.agent['Pokemon'])):
            if self.agent['Pokemon'][i]['stats']['hp'] > 0:
                agent = False
                break
        for i in range(len(self.opp['Pokemon'])):
            if self.opp['Pokemon'][i]['stats']['hp'] > 0:
                opp = False
                break
        if not agent and not opp:
            return False
        else: 
            #print('Game Over')
            return True
    
    def getDmgMult(self, moveType, defType):
        mult = 1
        if defType[0] in self.effectiveness[moveType]:
            mult *= self.effectiveness[moveType][defType[0]]
        if defType[1] is not None and defType[1] in self.effectiveness[moveType]:
            mult *= self.effectiveness[moveType][defType[1]]
        return mult
    
    #gets the legal Actions of a state 
    ##### STILL NEED TO DO THE CASE WHERE THE INDEX'S CURRENT POKEMON HAS 0 HEALTH
    def getLegalActions(self, agentIndex = 1):
        if agentIndex == 1:
            #Our turn
            #only add moves to legal actions if currPoke is alive
            if self.agent['Pokemon'][self.currAgent]['stats']['hp'] <= 0:
                moves = []
            else:
                moves = self.agent['Pokemon'][self.currAgent]['moves'].keys()
            switch = []
            for i in range(len(self.agent['Pokemon'])):
                if i != self.currAgent and self.agent['Pokemon'][i]['stats']['hp'] > 0:
                    switch.append(i)
        else:
            #Opponent's turn
            #only add moves to legal actions if currPoke is alive
            moves = []
            if self.opp['Pokemon'][self.currOpp]['stats']['hp'] > 0:
                moves = self.opp['Pokemon'][self.currOpp]['moves'].keys()

            switch = []
            for i, pokemon in enumerate(self.opp['Pokemon']):
                if i != self.currOpp and pokemon['stats']['hp'] > 0:
                    switch.append(i)
        legalActions = {'moves': moves, 'switch': switch}
        return legalActions

    #basic damage calculator (doesn't take into account types)
    '''
    def damageCalc(self, index, move):
        if index == 1:
            power = self.agent['Pokemon'][self.currAgent]['moves'][move][0]
            moveType = self.agent['Pokemon'][self.currAgent]['moves'][move][2]
            atk = self.agent['Pokemon'][self.currAgent]['stats']['atk'] if moveType == 'physical' else self.agent['Pokemon'][self.currAgent]['stats']['spc']
            defense = self.opp['Pokemon'][self.currOpp]['stats']['def'] if moveType == 'physical' else self.opp['Pokemon'][self.currOpp]['stats']['spc']
        else:
            power = self.opp['Pokemon'][self.currOpp]['moves'][move][0]
            moveType = self.opp['Pokemon'][self.currOpp]['moves'][move][2]
            atk = self.opp['Pokemon'][self.currOpp]['stats']['atk'] if moveType == 'physical' else self.opp['Pokemon'][self.currOpp]['stats']['spc']
            defense = self.agent['Pokemon'][self.currAgent]['stats']['def'] if moveType == 'physical' else self.agent['Pokemon'][self.currAgent]['stats']['spc']


        damage = (((2 * LEVEL)/5 + 2) * power * atk / defense)/50 + 2
        return math.floor(damage)
    '''
    def damageCalc(self, index, move):
        if index == 1:
            power = self.agent['Pokemon'][self.currAgent]['moves'][move][0]
            moveType = self.agent['Pokemon'][self.currAgent]['moves'][move][2]
            
            atkType = self.agent['Pokemon'][self.currAgent]['type']
            atk = self.agent['Pokemon'][self.currAgent]['stats']['atk'] if moveType == 'physical' else self.agent['Pokemon'][self.currAgent]['stats']['spc']
            
            defType = self.opp['Pokemon'][self.currOpp]['type']
            defense = self.opp['Pokemon'][self.currOpp]['stats']['def'] if moveType == 'physical' else self.opp['Pokemon'][self.currOpp]['stats']['spc']
            moveAtt  = self.agent['Pokemon'][self.currAgent]['moves'][move][1]
        else:
            power = self.opp['Pokemon'][self.currOpp]['moves'][move][0]
            moveType = self.opp['Pokemon'][self.currOpp]['moves'][move][2]
            moveAtt = self.opp['Pokemon'][self.currOpp]['moves'][move][1]

            atkType = self.opp['Pokemon'][self.currOpp]['type']
            atk = self.opp['Pokemon'][self.currOpp]['stats']['atk'] if moveType == 'physical' else self.opp['Pokemon'][self.currOpp]['stats']['spc']
            
            defType = self.agent['Pokemon'][self.currAgent]['type']
            defense = self.agent['Pokemon'][self.currAgent]['stats']['def'] if moveType == 'physical' else self.agent['Pokemon'][self.currAgent]['stats']['spc']

        stab = 1.5 if moveAtt in atkType else 1
        dmgMult = self.getDmgMult(moveAtt, defType)
        damage = ((((2 * LEVEL)/5 + 2) * power * atk / defense)/50 + 2) * stab * dmgMult
        return math.floor(damage)

    #Given the actor, action, and action Type, give a new state with is the successor state
    def generateSuccessor(self, index, action, actType):
        agent = copy.deepcopy(self.agent)
        opp = copy.deepcopy(self.opp)
        state = BattleState(agent, opp, self.currAgent, self.currOpp)
        if actType == 'moves':
            dmg = self.damageCalc(index, action)
            if index == 1:
                #print('Player 1 is inflicting ', damage, ' damage to Player 2 with ', action)
                state.opp['Pokemon'][self.currOpp]['stats']['hp'] = max(self.opp['Pokemon'][self.currOpp]['stats']['hp'] - dmg, 0)
            else:
                #print('Player 2 is inflicting ', damage, ' damage to Player 1 with ', action)
                state.agent['Pokemon'][self.currAgent]['stats']['hp'] = max(self.agent['Pokemon'][self.currAgent]['stats']['hp'] - dmg, 0)
        if actType == 'switch':
            if index == 1:
                #print("Player 1 is switching to: ", action)
                state.currAgent = action
            else:
                #print("Player 1 is switching to: ", action)
                state.currOpp = action
        return state

    
    #heuristic function for when depth exceeds set depth
    def eval(self):
        agentHP = 0
        oppHP = 0
        for i in range(len(self.agent['Pokemon'])):
            agentHP += self.agent['Pokemon'][i]['stats']['hp']
            oppHP += self.opp['Pokemon'][i]['stats']['hp']
        return agentHP - oppHP

    #reward received after game ends
    def utility(self, index):
        assert self.isEnd() == True
        return float('inf') * index * -1
