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
        # Next game state of a certain action
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        # New position
        newPos = successorGameState.getPacmanPosition()
        # New boolean list of where food is
        newFood = successorGameState.getFood()
        # List of all ghosts
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # use original score to get a baseling
        score = successorGameState.getScore()
        #pseudo code attempt

        #convert food grid to a list
        foodList = newFood.asList();

        # increase score if food is close, use reciprocal

        # iterate thru food list
        # find minimum distance
        # use reciprocal to increase
        if foodList:
            foodDistances = []
            for foodPos in foodList:
                foodDistances .append(manhattanDistance(newPos, foodPos))
            minFoodDistance = min(foodDistances)
            score += 1.0 / minFoodDistance


        # descrease score if ghost is close and not scared
        for ghost in newGhostStates:
            # if ghost is not scared see how far
            if ghost.scaredTimer == 0:
                ghostPos = ghost.getPosition()
                distanceToPacman = manhattanDistance(newPos, ghostPos)
                if distanceToPacman < 2 :
                    # dangerous, decrease score significantly
                    score = score - 100

        return score

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
        # pacman's legal moves
        legalMoves = gameState.getLegalActions(0)
        # initalize best move to the first arbitrarily
        bestAction = legalMoves[0]
        # start at negative infinity so any real score would beat
        bestScore = float('-inf')

        # call minimax on all possible moves and return the highest score
        for move in legalMoves:
            score = self.minimax(gameState.generateSuccessor(0, move), 1, 0)
            if score > bestScore:
                bestScore = score
                bestAction = move

        return bestAction
    # recursively calles minimax for all successor statuses until reaches target depth
    def minimax(self, gameState, agentIndex, currDepth):
        if gameState.isWin() or gameState.isLose() or currDepth == self.depth:
            return self.evaluationFunction(gameState)
        
        legalMoves = gameState.getLegalActions(agentIndex)
        nextAgent = (agentIndex + 1) % gameState.getNumAgents()
            # if next agent is pacman, increase depth
        if nextAgent == 0: 
            nextDepth = currDepth + 1
        else:
            nextDepth = currDepth

        # if pacman agent, return the max of the minimax recursion
        if agentIndex == 0: 
            # get all legal actions
            
            scoresOfMoves = []
            for move in legalMoves:
                scoresOfMoves.append(self.minimax(gameState.generateSuccessor(agentIndex, move), nextAgent, nextDepth))
            return max(scoresOfMoves)
        # return min if its a ghost
        else:
            scoresOfMoves = []
            for move in legalMoves:
                scoresOfMoves.append(self.minimax(gameState.generateSuccessor(agentIndex, move), nextAgent, nextDepth))
            return min(scoresOfMoves)


        


        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
         # pacman's legal moves
        legalMoves = gameState.getLegalActions(0)
        # initalize best move to the first arbitrarily
        bestAction = legalMoves[0]
        # start at negative infinity so any real score would beat
        bestScore = float('-inf')

        # initialize alpha and beta
        alpha = float('-inf')
        beta = float('inf')
        # call alphabeta on all possible moves and return the highest score
        for move in legalMoves:
            score = self.alphaBeta(gameState.generateSuccessor(0, move), 1, 0, alpha, beta)
            if score > bestScore:
                bestScore = score
                bestAction = move
            # update alpha is the score is better than the current alpha
            if score > alpha:
                alpha = score
        return bestAction
    
    def alphaBeta(self, gameState, agentIndex, currDepth, alpha, beta):
        if gameState.isWin() or gameState.isLose() or currDepth == self.depth:
            return self.evaluationFunction(gameState)
        
        legalMoves = gameState.getLegalActions(agentIndex)
        nextAgent = (agentIndex + 1) % gameState.getNumAgents()
        # if next agent is pacman, increase depth
        if nextAgent == 0: 
            nextDepth = currDepth + 1
        else:
            nextDepth = currDepth

        # if pacman agent, return the max of the minimax recursion
        if agentIndex == 0: 
            # get all legal actions
            scoresOfMoves = []
            #initialize value to negative infinity
            value = float('-inf')
            for move in legalMoves:
                score = self.alphaBeta(gameState.generateSuccessor(agentIndex, move), nextAgent, 
                                       nextDepth, alpha, beta)
                if score > value:
                    value = score
                # check if we can prune
                if value > beta:
                    return value
                alpha = max(alpha, value)
            return value
        # return min if its a ghost
        else:
            scoresOfMoves = []
            #initialize value to positive infinity
            value = float('inf')
            for move in legalMoves:
                score = self.alphaBeta(gameState.generateSuccessor(agentIndex, move), nextAgent,
                                        nextDepth, alpha, beta)
                if score < value:
                    value = score
                # check if we can prune
                if value < alpha:
                    return value
                beta = min(beta, value)
            return value


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
        # pacman's legal moves
        legalMoves = gameState.getLegalActions(0)
        # initalize best move to the first arbitrarily
        bestAction = legalMoves[0]
        # start at negative infinity so any real score would beat
        bestScore = float('-inf')

        # call minimax on all possible moves and return the highest score
        for move in legalMoves:
            score = self.expectimax(gameState.generateSuccessor(0, move), 1, 0)
            if score > bestScore:
                bestScore = score
                bestAction = move

        return bestAction
        
    def expectimax(self, gameState,agentIndex, currDepth):
        if gameState.isWin() or gameState.isLose() or currDepth == self.depth:
            return self.evaluationFunction(gameState)
        
        legalMoves = gameState.getLegalActions(agentIndex)
        nextAgent = (agentIndex + 1) % gameState.getNumAgents()
            # if next agent is pacman, increase depth
        if nextAgent == 0: 
            nextDepth = currDepth + 1
        else:
            nextDepth = currDepth

        # if pacman agent, return the max of the expectimax recursion
        if agentIndex == 0: 
            # get all legal actions
            
            scoresOfMoves = []
            for move in legalMoves:
                scoresOfMoves.append(self.expectimax(gameState.generateSuccessor(agentIndex, move), nextAgent, nextDepth))
            return max(scoresOfMoves)
        # return average of move scores considering probability if its a ghost
        else:
            scoresOfMoves = []
            for move in legalMoves:
                scoresOfMoves.append(self.expectimax(gameState.generateSuccessor(agentIndex, move), nextAgent, nextDepth))
            # add up scores
            totalScore = sum(scoresOfMoves)
            valAfterProbability = totalScore / len(legalMoves)
            return valAfterProbability



def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
