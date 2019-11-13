Agent = {'Pokemon': [], 'currPoke': 0}
Opp = {'Pokemon': [], 'currPoke': 0}

pikachu = {'name': 'pikachu', 'moves': {'thunderbolt': (95, 'electric', 'special'), 'quick attack': (40, 'normal', 'physical')}, 'stats' : {'hp': 35, 'atk': 55, 'def': 30, 'spe': 90, 'spc': 50}, 'type': ('electric', None)}

charizard = {'name': 'charizard', 'moves':{'fire blast':(120, 'fire', 'special'), 'flamethrower':(90, 'fire', 'special')}, 'stats':{'hp':78, 'atk':84, 'def':78, 'spe':100, 'spc':85}, 'type':('fire', 'flying')}

Agent['Pokemon'] = [pikachu, charizard]
Opp['Pokemon'] = [charizard, pikachu]

class BattleState:
    def __init__(self, agent, opp):
        self.agent = agent
        self.opp = opp
        self.currAgent = agent['currPoke']
        self.currOpp = opp['currPoke']

    def isEnd(self):
        agent = True
        opp = True
        for i in range(len(self.agent['Pokemon'])):
            if self.agent['Pokemon'][i]['stats']['hp'] > 0:
                agent = False
            if self.opp['Pokemon'][i]['stats']['hp'] > 0:
                opp = False
            if not agent and not opp:
                return False
        return True

    def getLegalActions(self, agentIndex = 1):
        if agentIndex == 1:
            moves = self.agent['Pokemon'][self.currAgent]['moves'].keys()
            switch = []
            for i in range(len(self.agent['Pokemon'])):
                if i != self.currAgent and self.agent['Pokemon'][i]['stats']['hp'] > 0:
                    switch.append(i)
        else:
            moves = self.opp['Pokemon'][self.currOpp]['moves'].keys()
            switch = []
            for i, pokemon in enumerate(self.opp['Pokemon']):
                if i != self.currOpp and pokemon['stats']['hp'] > 0:
                    switch.append(i)
        legalActions = {'moves': moves, 'switch': switch}
        return legalActions

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

        level = 50
        damage = (((2 * level)/5 + 2) * power * atk / defense)/50 + 2
        return damage

    def generateSuccessor(self, index, action, actType):
        state = BattleState(self.agent, self.opp)
        if actType == 'moves':
            damage = self.damageCalc(index, action)
            if index == 1:
                state.opp['Pokemon'][self.currOpp]['stats']['hp'] -= damage
            else:
                state.agent['Pokemon'][self.currAgent]['stats']['hp'] -= damage
        if actType == 'switch':
            if index == 1:
                state.currAgent = action
            else:
                state.currOpp = action
        return state

    def eval(self):
        agentHP = 0
        oppHP = 0
        for i in range(len(self.agent['Pokemon'])):
            agentHP += self.agent['Pokemon'][i]['stats']['hp']
            oppHP += self.opp['Pokemon'][i]['stats']['hp']
        return agentHP - oppHP

    def utility(self, index):
        assert self.isEnd() == True
        return float('inf') * index * -1
