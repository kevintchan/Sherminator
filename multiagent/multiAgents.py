# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util, sys

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
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"
    """
    print scores
    print legalMoves
    print legalMoves[chosenIndex]
    """
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
    newFood = successorGameState.getFood()
    currentNumFood = currentGameState.getNumFood()
    newNumFood = successorGameState.getNumFood()
    newGhostStates = successorGameState.getGhostStates()
    newGhostPositions = [ghostState.getPosition() for ghostState in newGhostStates]
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "determine if in range of ghost"
    distToNearestGhost = self.distToNearestPos(newPos, newGhostPositions)
    if (distToNearestGhost < 2):
      return -1
    
    if (newNumFood < currentNumFood):
      return 1

    if (newFood.asList()):
      distToNearestFood = self.distToNearestPos(newPos, newFood.asList())
      returnVal = float(1) / float(distToNearestFood)
    else:
      returnVal = 2

    return returnVal

  def distToNearestPos(self, pacmanPosition, positions):
    minDist = None
    for position in positions:
      dist = distCalc(pacmanPosition, position)
      if ((minDist == None) or dist < minDist):
        minDist = dist
    
    return minDist

def distCalc(pos1, pos2):
  return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

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

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.
    """
    legalActions = gameState.getLegalActions()
    successorStates = [gameState.generateSuccessor(0, action)
                       for action in legalActions]
    actionScores = [self.getValue(successorState, self.depth, 1)
                    for successorState in successorStates]
    bestScore = max(actionScores)
    bestIndices = [index
                   for index in range(len(actionScores))
                   if actionScores[index] == bestScore]
    chosenIndex = random.choice(bestIndices)
    return legalActions[chosenIndex]

  def getValue(self, gameState, depth, agentIndex):

    legalActions = gameState.getLegalActions(agentIndex)

    if (depth == 0 or (not legalActions)):
      return self.evaluationFunction(gameState)

    "prepare recursive call"
    if (agentIndex == (gameState.getNumAgents() - 1)):
      nextDepth = depth - 1
      nextAgent =  0
    else:
      nextDepth = depth
      nextAgent = agentIndex + 1

    successorStates = [gameState.generateSuccessor(agentIndex, action)
                       for action in legalActions]
    values = [self.getValue(successorState, nextDepth, nextAgent)
              for successorState in successorStates]
    if (agentIndex == 0):
      return max(values)
    else:
      return min(values)

class AlphaBetaAgent(MultiAgentSearchAgent):
  "gotok"

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.
    """
    legalActions = gameState.getLegalActions()
    successorStates = [gameState.generateSuccessor(0, action)
                       for action in legalActions]
    actionScores = [self.getValue(successorState, -100000000, 100000000,
                                  self.depth, 1)
                    for successorState in successorStates]
    bestScore = max(actionScores)
    bestIndices = [index
                   for index in range(len(actionScores))
                   if actionScores[index] == bestScore]
    chosenIndex = random.choice(bestIndices)
    return legalActions[chosenIndex]

  def getValue(self, gameState, alpha, beta, depth, agentIndex):

    legalActions = gameState.getLegalActions(agentIndex)

    if (depth == 0 or (not legalActions)):
      return self.evaluationFunction(gameState)

    "prepare recursive call"
    if (agentIndex == (gameState.getNumAgents() - 1)):
      nextDepth = depth - 1
      nextAgent =  0
    else:
      nextDepth = depth
      nextAgent = agentIndex + 1

    successorStates = [gameState.generateSuccessor(agentIndex, action)
                       for action in legalActions]
    
    if (agentIndex == 0):
      "max-value"
      v = None
      for successorState in successorStates:
        v = max(v, self.getValue(successorState, alpha, beta,
                                 nextDepth, nextAgent))
        if (v >= beta):
          return v
        alpha = max(alpha, v)
      return v
    elif (agentIndex == (gameState.getNumAgents() - 1)):
      "min-value expecting pacman"
      v = None
      for successorState in successorStates:
        v = min(v, self.getValue(successorState, alpha, beta,
                                 nextDepth, nextAgent))
        if (v <= alpha):
          return v
        beta= min(beta, v)
      return v
    else:
      values = [self.getValue(successorState, alpha, beta, nextDepth, nextAgent)
                for successorState in successorStates]
      return min(values)


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
    "*** YOUR CODE HERE ***"
    #find list of possible ghost locations in next step
    #find list of possible pacman action for next step
    #for each possible pacman action, average the evaulated value for each possible ghost location configuration
    #chose action with highestavg

    legalActions = gameState.getLegalActions()
    successorStates = [gameState.generateSuccessor(0, action)
                       for action in legalActions]
    actionScores = [self.getValue(successorState, self.depth, False)
                    for successorState in successorStates]
    bestScore = max(actionScores)
    bestIndices = [index
                   for index in range(len(actionScores))
                   if actionScores[index] == bestScore]
    chosenIndex = random.choice(bestIndices)
    return legalActions[chosenIndex]

  def getValue(self, gameState, depth, isPacman):

    legalActions = True

    if not isPacman:
      legalActions = gameState.getLegalActions(0)
      successorStates = [gameState.generateSuccessor(0, action)
                       for action in legalActions]
      nextDepth = depth - 1
      isPacman = True
    else:
      successorStates = self.expMinMaxHelper(gameState)
      nextDepth = depth
      isPacman = False

    if (depth == 0 or (not legalActions)):
      return self.evaluationFunction(gameState)

    values = [self.getValue(successorState, nextDepth, isPacman)
              for successorState in successorStates]

    if isPacman:
      return max(values)
    else:
      return (sum(values)/len(values))


  def expMinMaxHelper(self, gameState):
    numOfGhosts = gameState.getNumAgents() - 1
    possibleNextGameStates = [gameState]
    newPossibleNextGameStates = []
    for ghostNum in range(1, numOfGhosts + 1):
      for state in possibleNextGameStates:
        ghostLegalActs = state.getLegalActions(ghostNum)
        if len(ghostLegalActs) is not 0:
          for action in ghostLegalActs:
            newState = state.generateSuccessor(ghostNum, action)
            newPossibleNextGameStates.append(newState)
        else:
          newPossibleNextGameStates = possibleNextGameStates[:]
      possibleNextGameStates = newPossibleNextGameStates[:]
      newPossibleNextGameStates = []
    return possibleNextGameStates



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

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

