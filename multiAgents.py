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
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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
        newPos = successorGameState.getPacmanPosition() #This tells you the position that pacman will be in
        newFood = successorGameState.getFood() #What does this do?
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newScore = successorGameState.getScore()
        newGhostPositions = successorGameState.getGhostPositions()

        print(currentGameState.getNumAgents())

        ghostDistanceArray = []
        hitghost = 0

        for pos in newGhostPositions:

            distance = util.manhattanDistance(pos, newPos)
            ghostDistanceArray.append(distance)

            if distance == 1:
                hitghost += 1

        ghostDistanceMax = min(ghostDistanceArray)

        if ghostDistanceMax == 0:
            ghostDistanceMax = 1

        foodList = newFood.asList()

        arrayofFood = [10000000]

        for food in foodList:
            foodDistance = util.manhattanDistance(food, newPos)
            arrayofFood.append(foodDistance)

        foodMin = min(arrayofFood)

        if foodMin == 0:
            foodMin = 1


        total = 1/float(foodMin) - 1/float(ghostDistanceMax) - hitghost + newScore
        return total

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
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

        def minimax(agent, depth, gameState):

            print(depth)

            if depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            elif agent == 0:
                return max_value(agent, depth, gameState)

            else:
                return min_value(agent, depth, gameState)

        def min_value(agent, depth, gameState):
            x = 999
            agentnext = agent + 1

            if gameState.getNumAgents() == agentnext:
                agentnext = 0
            if agentnext == 0:
                depth += 1
            for dir in gameState.getLegalActions(agent):
                child = gameState.generateSuccessor(agent, dir)
                x = min(x, minimax(agentnext, depth, child))

            return x


        def max_value(agent, depth, gameState):

            print('Y')
            x = -999
            for dir in gameState.getLegalActions(agent):
                child = gameState.generateSuccessor(agent, dir)
                x = max(x, minimax(1, depth, child))
            return x


        total = -999
        pacmandirection = gameState.getLegalActions(0)
        direction = Directions.WEST

        for step in pacmandirection:
            utilStep = minimax(1, 0,gameState.generateSuccessor(0, step))
            if utilStep > total:
                total = utilStep
                direction = step

        return direction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alpha_beta(agent, depth, gameState, alpha, beta):

            if depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            elif agent == 0:
                return max_value(agent, depth, gameState, alpha, beta)

            else:
                return min_value(agent, depth, gameState, alpha, beta)

        def max_value(agent, depth, gameState, alpha, beta):
            x = -99999

            for dir in gameState.getLegalActions(agent):
                child = gameState.generateSuccessor(agent, dir)
                x = max(x, alpha_beta(1, depth, child, alpha, beta))
                if x > beta:
                    return x
                alpha = max(alpha, x)

            return x

        def min_value(agent, depth, gameState, alpha, beta):
            x = 99999
            agentNext = agent + 1

            if gameState.getNumAgents() == agentNext:
                agentNext = 0

            if agentNext == 0:
                depth += 1

            for dir in gameState.getLegalActions(agent):
                child = gameState.generateSuccessor(agent, dir)
                x = min(x, alpha_beta(agentNext, depth, child, alpha, beta))
                if x < alpha:
                    return x
                beta = min(beta, x)

            return x

        total = -99999
        pacmanDirection = gameState.getLegalActions(0)
        direction = Directions.WEST
        alpha = -99999
        beta = 99999

        for step in pacmanDirection:
            utilStep = alpha_beta(1, 0,gameState.generateSuccessor(0, step), alpha, beta)

            if utilStep > total:
                total = utilStep
                direction = step

            alpha = max(alpha, total)

        return direction

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

        def expectimax(agent, depth, gameState):
            print(depth)
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            elif agent == 0:
                return max_value(agent, depth, gameState)

            else:
                return exp_value(agent, depth, gameState)

        def max_value(agent, depth, gameState):
            print('Y')
            x = -99999
            for dir in gameState.getLegalActions(agent):
                child = gameState.generateSuccessor(agent, dir)
                x = max(x, expectimax(1, depth, child))

            return x

        def exp_value(agent, depth, gameState):
            x = 0
            agentNext = agent + 1

            if gameState.getNumAgents() == agentNext:
                agentNext = 0

            if agentNext == 0:
                depth += 1

            for dir in gameState.getLegalActions(agent):
                child = gameState.generateSuccessor(agent, dir)
                x += (expectimax(agentNext, depth, child))

            average = x/len(gameState.getLegalActions(agent))

            return average

        total = -99999
        pacmanDirection = gameState.getLegalActions(0)
        direction = Directions.WEST

        for step in pacmanDirection:
            utilStep = expectimax(1, 0, gameState.generateSuccessor(0, step))
            if utilStep > total:
                total = utilStep
                direction = step

        return direction

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    newPos = currentGameState.getPacmanPosition()  # This tells you the position that pacman will be in
    newFood = currentGameState.getFood()  # What does this do?
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newGhostPositions = currentGameState.getGhostPositions()
    newScore = currentGameState.getScore()

    print(currentGameState.getNumAgents())
    ghostArray = []
    hitghost = 0
    for position in newGhostPositions:
        distance = util.manhattanDistance(position, newPos)
        ghostArray.append(distance)
        if distance == 1:
            hitghost += 1

    maxGhost = min(ghostArray)
    if maxGhost == 0:
        maxGhost = 1

    foodList = newFood.asList()
    foodArray = [999999]
    for food in foodList:
        foodDistance = util.manhattanDistance(food, newPos)
        foodArray.append(foodDistance)

    minFood = min(foodArray)
    if minFood == 0:
        minFood = 1

    balls = currentGameState.getCapsules()
    totalBalls = len(balls)
    total = 1 / float(minFood) - 1 / float(maxGhost) - hitghost + newScore - totalBalls
    return total
    
better = betterEvaluationFunction
