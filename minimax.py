from GameState import BattleState
import random

#almost identical to what we have written for pacman, biggest difference is calling new states using generateSuccessor

class MinimaxAgent():

    def __init__ (self, depth = '2'):
        self.index = 1
        self.depth = int(depth)

    def getAction(self, gameState):
        actions = gameState.getLegalActions(self.index)
        depth = self.depth

        def vminmax(state, d, index):
            if state.isEnd():
                return state.utility(index)
            if d == 0:
                return state.eval()
            if index == 1:
                a = state.getLegalActions(index)

                vs = []
                for act in a['moves']:
                    vs.append(vminmax (state.generateSuccessor(index, act, 'moves'), d, -1))
                for act in a['switch']:
                    vs.append(vminmax(state.generateSuccessor(index, act, 'switch'), d, -1))

                return max(vs)

            if index == -1:
                a = state.getLegalActions(index)

                vs = []
                for act in a['moves']:
                    vs.append(vminmax(state.generateSuccessor(index, act, 'moves'), d-1, 1))
                for act in a['switch']:
                    vs.append(vminmax(state.generateSuccessor(index, act, 'switch'), d-1, 1))
                return min(vs)
        v = []
        for action in actions['moves']:
            v.append(vminmax(gameState.generateSuccessor(self.index, action, 'moves'), depth, self.index * -1))
        for action in actions['switch']:
            v.append(vminmax(gameState.generateSuccessor(self.index, action, 'switch'), depth, self.index * -1))
        bestscore = max(v)
        bestindex = [index for index in range(len(v)) if v[index] == bestscore]
        chosenindex = random.choice(bestindex)
        if chosenindex < len(actions['moves']):
            return list(actions['moves'])[chosenindex], 'moves'
        else:
            return actions['switch'][chosenindex - len(actions['moves'])], 'switch'




