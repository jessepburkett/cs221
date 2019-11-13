# definition of players for baseline

Agent = {'Pokemon':[], 'curPoke':{}}
Opponent = {'Pokemon':[], 'curPoke':{}}

pikachu = {'moves':{'thunderbolt':(95, 'electric', 'special'), 'quick attack':(40, 'normal', 'physical')}, 'stats':{'hp':35, 'atk':55, 'def':30, 'spe':90, 'spc':50}, 'type':('electric', None)}

charizard = {'moves':{'fire blast':(120, 'fire', 'special'), 'flamethrower':(90, 'fire', 'special')}, 'stats':{'hp':78, 'atk':84, 'def':78, 'spe':100, 'spc':85}, 'type':('fire', 'flying')}

Agent['Pokemon']=[pikachu, charizard]
Agent['curPoke']=Agent['Pokemon'][0]
Opponent['Pokemon']=[charizard, pikachu]
Opponent['curPoke']=Opponent['Pokemon'][0]


class BattleState(object):
	"""docstring for BattleState"""
	def __init__(self, agent, opp):
		super(BattleState, self).__init__()
		self.agent = agent
		self.opp = opp

	# state = (agent, opponent, whose turn)
	def startState(self):
		player = 0 if self.agent['curPoke'][stats]['spe']  >= self.opp['curPoke'][stats]['spe'] else 1
		return (self.agent, self.opp, player)

	def isEnd(self):
		agent=True
		opp=True
		for i in len(self.agent['Pokemon']):
			if self.agent['Pokemon'][i]['stats']['hp'] > 0:
				agent=False
			if self.opp['Pokemon'][i]['stats']['hp'] > 0:
				opp=False
			if not agent and not opp:
				return False
		return True

	def getLegalActions(self, state):
		player = state[2]
		moves=[move for move in state[player]['curPoke']['moves']]
		switch=[pokemon for pokemon in state[player]['Pokemon'] if pokemon not state[player]['curPoke'] and pokemon['stats']['hp'] > 0]
		legalActions = {'moves':moves, 'switch':switch}
		return legalActions

	def damageCalc(self, state, move):
		level = 50
		curPlayer = state[2]
		atkPlayer = state[curPlayer]
		defPlayer = state[0] if curPlayer == 1 else state[1]
		#move --> (power, type, phys or spec)
		moveType = atkPlayer['curPoke']['moves'][move][2]
		power = atkPlayer['curPoke']['moves'][move][0]
		attack = atkPlayer['curPoke'][stats]['atk'] if moveType == 'physical' else atkPlayer['curPoke'][stats]['spc']
		defense = defPlayer['curPoke'][stats]['def'] if moveType == 'physical' else defPlayer['curPoke'][stats]['spc']

		damage=(((2*level)/5 + 2)*power*attack/defense)/50 + 2

		return damage


	# state = (agent dict, opp dict, whose turn int (0 or 1))
	# action = string (for ex. 'fire blast' or 'charizard')
	# actType = string ('moves' or 'switch')
	def genSuccessor(self, state, action, actType):
		if actType == 'moves':
			damage = damageCalc(state, action)
			curPlayer = state[2]
			atkPlayer = state[curPlayer]
			defPlayer = state[0] if curPlayer == 1 else state[1]
			defPlayer['curPoke']['stats']['hp'] -= damage

			## if our current player is 0 then it is the agent and our attacking player
			if curPlayer==0:
			 	return (atkPlayer, defPlayer, 1)
			 else:
			 	return (defPlayer, atkPlayer, 0)

		if actType == 'switch':
			curPlayer = state[2]
			atkPlayer = state[curPlayer]
			atkPlayer['curPoke'] = atkPlayer['Pokemon'][action]
			defPlayer = state[0] if curPlayer == 1 else state[1]

			if curPlayer==0:
				 	return (atkPlayer, defPlayer, 1)
				 else:
				 	return (defPlayer, atkPlayer, 0)


	def eval(self):
		agentHP = 0
		oppHP = 0
		for i in len(self.agent['Pokemon']):
			agentHP += self.agent['Pokemon'][i]['stats']['hp']
			oppHP += self.opp['Pokemon'][i]['stats']['hp']
		return agentHP-oppHP

	def utility(self, state):	#isEnd returns true on losing player's turn
		assert isEnd() == True
		if state[2] == 0:
			return float('inf')
		else: return -float('inf')

