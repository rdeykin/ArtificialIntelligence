# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        foodDistance = []
        ghostDistance = []
        for i in newFood:
            foodDistance.append(util.manhattanDistance(newPos, i))
        for i in newGhostStates:
            ghostDistance.append(util.manhattanDistance(newPos, i.getPosition()))
        if len(foodDistance) > 1:
            closest_food_avg = sum(foodDistance)/len(foodDistance)
        else:
            closest_food_avg = 1000

        closest_food = 1/closest_food_avg

        if len(newFood) >= 1:
            food = len(newFood) * -1000000
        else:
            food = float("inf")

        if min(ghostDistance) <= 1:
            ghost = -100000000000
        else:
            ghost = 1
        numPowerPellets = len(currentGameState.getCapsules())
        # return successorGameState.getScore()
        return closest_food + food + ghost



def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        depth = self.depth

        def maxAction(state, level):

            if state.isWin() or state.isLose():  # if the state is a terminal state
                return ("blah", self.evaluationFunction(state))# return a dummy action and the evaluation function
            elif depth == level:
                return ("blah", self.evaluationFunction(state))

            else:
                v = float("-inf")
                action = "blah"
                for i in state.getLegalActions(0):  # for every legal action pacman can take
                    x = minAction(state.generateSuccessor(0, i), level, 1)  # find the maximum action
                    if x[1] > v:
                        v = x[1]
                        action = i
            return (action, v)

        def minAction(state, level, agentIndex):

            if state.isWin() or state.isLose():

                return ("blah", self.evaluationFunction(state))

            if level == depth and agentIndex == numAgents - 1:
                #print(level)
                #print(agentIndex)
                #print(depth)
                return ("blah", self.evaluationFunction(state))

            if agentIndex < numAgents - 1:

                v = float("inf")
                action = "blah"
                for i in state.getLegalActions(agentIndex):
                    x = minAction(state.generateSuccessor(agentIndex, i), level, agentIndex + 1)
                    if x[1] < v:
                        v = x[1]
                        action = i
                return (action, v)

            if agentIndex == numAgents - 1:

                v = float("inf")
                action = "blah"
                for i in state.getLegalActions(agentIndex):
                    x = maxAction(state.generateSuccessor(agentIndex, i), level + 1)
                    if x[1] < v:
                        v = x[1]
                        action = i
                return (action, v)

        return maxAction(gameState, 0)[0]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        numAgents = gameState.getNumAgents()
        depth = self.depth

        def maxAction(state, level, alpha, beta):

            if state.isWin() or state.isLose():

                return "blah", self.evaluationFunction(state)

            elif depth == level:

                return "blah", self.evaluationFunction(state)

            else:
                v = float("-inf")
                action = "blah"
                for i in state.getLegalActions(0):
                    x = minAction(state.generateSuccessor(0, i), level, alpha, beta, 1)
                    if x[1] > v:
                        v = x[1]
                        action = i
                    if v > beta:
                        return action, v
                    alpha = max(v, alpha)
                return action, v

        def minAction(state, level, alpha, beta, agentIndex):

            if state.isWin() or state.isLose():

                return "blah", self.evaluationFunction(state)

            if level == depth and agentIndex == numAgents - 1:

                return "blah", self.evaluationFunction(state)

            if agentIndex < numAgents - 1:

                v = float("inf")
                action = "blah"
                for i in state.getLegalActions(agentIndex):
                    x = minAction(state.generateSuccessor(agentIndex, i), level, alpha, beta, agentIndex + 1)
                    if x[1] < v:
                        v = x[1]
                        action = i
                    if v < alpha:
                        return action, v
                    beta = min(beta, v)
                return action, v

            if agentIndex == numAgents - 1:

                v = float("inf")
                action = "blah"
                for i in state.getLegalActions(agentIndex):
                    x = maxAction(state.generateSuccessor(agentIndex, i), level + 1, alpha, beta)
                    if x[1] < v:
                        v = x[1]
                        action = i
                    if v < alpha:
                        return action, v
                    beta = min(beta, v)
                return action, v


        return maxAction(gameState, 0, float("-inf"), float("inf"))[0]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        numAgents = gameState.getNumAgents()
        depth = self.depth

        def maxAction(state, level):

            if state.isWin() or state.isLose():  # if the state is a terminal state
                return "blah", self.evaluationFunction(state) # return a dummy action and the evaluation function
            elif depth == level:
                return "blah", self.evaluationFunction(state)

            else:
                v = float("-inf")
                action = "blah"
                for i in state.getLegalActions(0):  # for every legal action pacman can take
                    x = expAction(state.generateSuccessor(0, i), level, 1)  # find the maximum action
                    if x[1] > v:
                        v = x[1]
                        action = i
            return action, v

        def expAction(state, level, agentIndex):

            if state.isWin() or state.isLose():

                return "blah", (self.evaluationFunction(state))

            if level == depth and agentIndex == numAgents - 1:

                return "blah", (self.evaluationFunction(state))

            if agentIndex < numAgents - 1:

                v = 0
                action = "blah"
                for i in state.getLegalActions(agentIndex):
                    x = expAction(state.generateSuccessor(agentIndex, i), level, agentIndex + 1)
                    p = 1/len(state.getLegalActions(agentIndex))
                    v += x[1] * p
                    action = i
                return action, v

            if agentIndex == numAgents - 1:
                v = 0
                action = "blah"
                for i in state.getLegalActions(agentIndex):
                    x = maxAction(state.generateSuccessor(agentIndex, i), level + 1)
                    p = 1 / len(state.getLegalActions(agentIndex))
                    v += x[1] * p
                    action = i
                return action, v
        return maxAction(gameState, 0)[0]