import copy
import time

# --------------- Custom classes ---------------

class Node:
    def __init__(self, functionCost, heuristicCost, cost, totalCost, stateWhenAtNode, parent, numberMoved):
        self.functionCost = functionCost
        self.heuristicCost = heuristicCost
        self.cost = cost
        self.totalCost = totalCost
        self.stateWhenAtNode = stateWhenAtNode
        self.parent = parent
        self.numberMoved = numberMoved

    def __cmp__(self, other):
        return __cmp__(self.totalCost, other.totalCost)

    def getEmptySpaceIndex(self):
        rowNum = 0
        colNum = 0
        for rows in self.stateWhenAtNode:
            for cols in rows:
                if cols == '0':
                    return str(rowNum) + " " + str(colNum)
                else:
                    colNum += 1
            colNum = 0
            rowNum += 1

    def toString(self):
        line = ""
        for row in self.stateWhenAtNode:
            line += "[ "
            for col in row:
                line += col + " "
            line += "] \n"
        return line

    def toOneLineString(self):
        oneLine = ""
        for row in self.stateWhenAtNode:
            for col in row:
                oneLine += col + " "
        oneLine.rstrip()
        return oneLine


# --------------- Constants ---------------
TOP_LEFT_CORNER = "0 0"
TOP_RIGHT_CORNER = "0 3"
BOTTOM_LEFT_CORNER = "1 0"
BOTTOM_RIGHT_CORNER = "1 3"
TIMEOUT_TIME_IN_SECONDS = 60

# --------------- Global Variables ---------------
_openList = []
_closedList = []
# Initializing the goal node object, to be used later.
_goalNode = Node(0, 0, 0, 0, [[]], None, -1)
# This variable defines if we have found the solution or not.
_end = False
# This variable defines if there was a timeout or not. True for timeout, false for not.
_timeout = False

# Building the goalLists, one for each goal state.
_goalList1 = []
row1 = []
row2 = []
for num in range(4):
    row1.append(str(num + 1))
for num in range(3):
    row2.append(str(num + 5))
row2.append("0")
_goalList1.append(row1)
_goalList1.append(row2)

_goalList2 = []
row1 = []
row2 = []
count = 0
for num in range(4):
    row1.append(str((1 + (count * 2))))
    count += 1
count = 0
for num in range(3):
    row2.append(str((2 + (count * 2))))
    count += 1
row2.append("0")
_goalList2.append(row1)
_goalList2.append(row2)

# Initializing start time. Will be overridden when we actually start.
_startTime = 0

# Initializing a global variable to hold all searched nodes
_searchedNodes = []


# --------------- Functions ---------------
def timeFormat(seconds):
    minutes = seconds // 60
    sec = seconds % 60
    hours = minutes // 60
    minutes = minutes % 60
    return "{0}:{1}:{2}".format(int(hours), int(minutes), sec)


def timeout():
    seconds = time.time() - _startTime
    if seconds > TIMEOUT_TIME_IN_SECONDS:
        return True
    else:
        return False


def load_input(filename):
    """
    Function for loading the initial puzzles, in format 2x4, from a text file.
    """
    file = open(filename, "r")
    dataRead = file.readlines()

    puzzleList = []
    for puzzle in dataRead:
        puzzle = puzzle.replace(' ', '')
        puzzle = puzzle.replace('\n', '')
        puzzleArray = [[], []]
        for char in puzzle[:4]:
            puzzleArray[0].append(char)
        for char in puzzle[4:]:
            puzzleArray[1].append(char)
        puzzleList.append(puzzleArray)

    return puzzleList


# Verifies if a node is in a goal state. If it is, returns true. If not, returns false.
def goalState(node):
    # Testing for the first way the node can be a goal (1,2,3,4 - 5,6,7,0)
    isSame = True

    colNum = 0
    rowNum = 0
    for stateRow in node.stateWhenAtNode:
        for stateCol in stateRow:
            if stateCol != _goalList1[rowNum][colNum]:
                isSame = False
                break
            colNum += 1
        rowNum += 1
        colNum = 0
        if not isSame:
            break

    # If we found a goal, we return true.
    if isSame:
        return isSame

    # If not, we test for the second way the node can be a goal (1,3,5,7 - 2,4,6,0)
    isSame = True
    colNum = 0
    rowNum = 0
    for stateRow in node.stateWhenAtNode:
        for stateCol in stateRow:
            if stateCol != _goalList2[rowNum][colNum]:
                isSame = False
                break
            colNum += 1
        rowNum += 1
        colNum = 0
        if not isSame:
            break

    return isSame


def findSolution(node):
    global _timeout
    global _end
    global _searchedNodes
    global _openList
    global _closedList

    _openList.append(node)

    # For as long as we don't have a solution, pop the first node of the open list.
    while not _end and len(_openList) != 0:
        if timeout():
            _timeout = True
            _end = True
            break

        possibleMoves = findMoves(_openList.pop(0))

        # For each of our node, check the closed list to see if it's there. If it's there, we don't want it.
        for newNode in possibleMoves:
            found = next((n for n in _closedList if n.stateWhenAtNode == newNode.stateWhenAtNode), None)
            if found is None:
                # We now check if it's in our open list. If it's there, we update the cost if we have a lower total
                # cost. If not, we add it to the open list.
                found = next((n for n in _openList if n.stateWhenAtNode == newNode.stateWhenAtNode), None)
                if found is None:
                    _openList.append(newNode)
                else:
                    if found.totalCost > newNode.totalCost:
                        _openList.remove(found)
                        _openList.append(newNode)

        # Sorting the open list by total cost of the nodes.
        sorted(_openList, key=lambda n: n.totalCost)

    _searchedNodes = _closedList

    # If we are here, we either have a solution or we failed to find one.
    if _end and not _timeout:
        print("Solution found.")
    elif _timeout:
        print("Timed out. Longer than " + str(TIMEOUT_TIME_IN_SECONDS) + " seconds passed.")
    else:
        print("Failed to find a solution to the puzzle.")


def findMoves(node):
    global _end
    global _goalNode
    global _openList
    global _closedList

    if _end:
        return

    _closedList.append(node)

    # Check if we are at goalState
    if goalState(node):
        _goalNode = node
        _end = True
        return

    # find where the empty space is in node's gamestate
    indexOfEmpty = node.getEmptySpaceIndex()

    generated = []

    # Initializing Node to copy
    costOfMove = 1
    nodeToCopy = copy.copy(node)
    nodeToCopy.stateWhenAtNode = copy.deepcopy(node.stateWhenAtNode)
    nodeToCopy.totalCost += costOfMove
    nodeToCopy.cost = costOfMove
    nodeToCopy.parent = node

    if indexOfEmpty == TOP_LEFT_CORNER:
        # Wrapping move
        wrappingNode = copy.copy(nodeToCopy)
        wrappingNode.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        wrappingNode.numberMoved = wrappingNode.stateWhenAtNode[0][3]
        wrappingNode.stateWhenAtNode[0][0] = wrappingNode.stateWhenAtNode[0][3]
        wrappingNode.stateWhenAtNode[0][3] = "0"
        wrappingNode.cost += 1
        wrappingNode.totalCost += 1

        # Diagonal move
        diagonalNode = copy.copy(nodeToCopy)
        diagonalNode.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        diagonalNode.cost += 2
        diagonalNode.totalCost += 2
        diagonalNode.numberMoved = diagonalNode.stateWhenAtNode[1][1]
        diagonalNode.stateWhenAtNode[0][0] = diagonalNode.stateWhenAtNode[1][1]
        diagonalNode.stateWhenAtNode[1][1] = "0"

        # OpposedCorner move
        opposedCorner = copy.copy(nodeToCopy)
        opposedCorner.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        opposedCorner.cost += 2
        opposedCorner.totalCost += 2
        opposedCorner.numberMoved = opposedCorner.stateWhenAtNode[1][3]
        opposedCorner.stateWhenAtNode[0][0] = opposedCorner.stateWhenAtNode[1][3]
        opposedCorner.stateWhenAtNode[1][3] = "0"

        # Normal move, one step right
        oneStepRight = copy.copy(nodeToCopy)
        oneStepRight.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepRight.numberMoved = oneStepRight.stateWhenAtNode[0][1]
        oneStepRight.stateWhenAtNode[0][0] = oneStepRight.stateWhenAtNode[0][1]
        oneStepRight.stateWhenAtNode[0][1] = "0"

        # Normal move, one step down
        oneStepDown = copy.copy(nodeToCopy)
        oneStepDown.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepDown.numberMoved = oneStepDown.stateWhenAtNode[1][0]
        oneStepDown.stateWhenAtNode[0][0] = oneStepDown.stateWhenAtNode[1][0]
        oneStepDown.stateWhenAtNode[1][0] = "0"

        generated.extend((wrappingNode, diagonalNode, opposedCorner, oneStepRight, oneStepDown))
    elif indexOfEmpty == TOP_RIGHT_CORNER:
        # Wrapping move
        wrappingNode = copy.copy(nodeToCopy)
        wrappingNode.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        wrappingNode.numberMoved = wrappingNode.stateWhenAtNode[0][0]
        wrappingNode.stateWhenAtNode[0][3] = wrappingNode.stateWhenAtNode[0][0]
        wrappingNode.stateWhenAtNode[0][0] = "0"
        wrappingNode.cost += 1
        wrappingNode.totalCost += 1

        # Diagonal move
        diagonalNode = copy.copy(nodeToCopy)
        diagonalNode.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        diagonalNode.cost += 2
        diagonalNode.totalCost += 2
        diagonalNode.numberMoved = diagonalNode.stateWhenAtNode[1][2]
        diagonalNode.stateWhenAtNode[0][3] = diagonalNode.stateWhenAtNode[1][2]
        diagonalNode.stateWhenAtNode[1][2] = "0"

        # OpposedCorner move
        opposedCorner = copy.copy(nodeToCopy)
        opposedCorner.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        opposedCorner.cost += 2
        opposedCorner.totalCost += 2
        opposedCorner.numberMoved = opposedCorner.stateWhenAtNode[1][0]
        opposedCorner.stateWhenAtNode[0][3] = opposedCorner.stateWhenAtNode[1][0]
        opposedCorner.stateWhenAtNode[1][0] = "0"

        # Normal move, one step left
        oneStepLeft = copy.copy(nodeToCopy)
        oneStepLeft.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepLeft.numberMoved = oneStepLeft.stateWhenAtNode[0][2]
        oneStepLeft.stateWhenAtNode[0][3] = oneStepLeft.stateWhenAtNode[0][2]
        oneStepLeft.stateWhenAtNode[0][2] = "0"

        # Normal move, one step down
        oneStepDown = copy.copy(nodeToCopy)
        oneStepDown.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepDown.stateWhenAtNode[0][3] = oneStepDown.stateWhenAtNode[1][3]
        oneStepDown.stateWhenAtNode[1][3] = "0"

        generated.extend((wrappingNode, diagonalNode, opposedCorner, oneStepLeft, oneStepDown))

    elif indexOfEmpty == BOTTOM_LEFT_CORNER:
        # Wrapping move
        wrappingNode = copy.copy(nodeToCopy)
        wrappingNode.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        wrappingNode.numberMoved = wrappingNode.stateWhenAtNode[1][3]
        wrappingNode.stateWhenAtNode[1][0] = wrappingNode.stateWhenAtNode[1][3]
        wrappingNode.stateWhenAtNode[1][3] = "0"
        wrappingNode.cost += 1
        wrappingNode.totalCost += 1

        # Diagonal move
        diagonalNode = copy.copy(nodeToCopy)
        diagonalNode.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        diagonalNode.cost += 2
        diagonalNode.totalCost += 2
        diagonalNode.numberMoved = diagonalNode.stateWhenAtNode[0][1]
        diagonalNode.stateWhenAtNode[1][0] = diagonalNode.stateWhenAtNode[0][1]
        diagonalNode.stateWhenAtNode[0][1] = "0"

        # OpposedCorner move
        opposedCorner = copy.copy(nodeToCopy)
        opposedCorner.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        opposedCorner.cost += 2
        opposedCorner.totalCost += 2
        opposedCorner.numberMoved = opposedCorner.stateWhenAtNode[0][3]
        opposedCorner.stateWhenAtNode[1][0] = opposedCorner.stateWhenAtNode[0][3]
        opposedCorner.stateWhenAtNode[0][3] = "0"

        # Normal move, one step right
        oneStepRight = copy.copy(nodeToCopy)
        oneStepRight.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepRight.numberMoved = oneStepRight.stateWhenAtNode[1][1]
        oneStepRight.stateWhenAtNode[1][0] = oneStepRight.stateWhenAtNode[1][1]
        oneStepRight.stateWhenAtNode[1][1] = "0"

        # Normal move, one step up
        oneStepUp = copy.copy(nodeToCopy)
        oneStepUp.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepUp.numberMoved = oneStepUp.stateWhenAtNode[0][0]
        oneStepUp.stateWhenAtNode[1][0] = oneStepUp.stateWhenAtNode[0][0]
        oneStepUp.stateWhenAtNode[0][0] = "0"

        generated.extend((wrappingNode, diagonalNode, opposedCorner, oneStepRight, oneStepUp))
    elif indexOfEmpty == BOTTOM_RIGHT_CORNER:
        # Wrapping move
        wrappingNode = copy.copy(nodeToCopy)
        wrappingNode.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        wrappingNode.numberMoved = wrappingNode.stateWhenAtNode[1][0]
        wrappingNode.stateWhenAtNode[1][3] = wrappingNode.stateWhenAtNode[1][0]
        wrappingNode.stateWhenAtNode[1][0] = "0"
        wrappingNode.cost += 1
        wrappingNode.totalCost += 1

        # Diagonal move
        diagonalNode = copy.copy(nodeToCopy)
        diagonalNode.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        diagonalNode.cost += 2
        diagonalNode.totalCost += 2
        diagonalNode.numberMoved = diagonalNode.stateWhenAtNode[0][2]
        diagonalNode.stateWhenAtNode[1][3] = diagonalNode.stateWhenAtNode[0][2]
        diagonalNode.stateWhenAtNode[0][2] = "0"

        # OpposedCorner move
        opposedCorner = copy.copy(nodeToCopy)
        opposedCorner.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        opposedCorner.cost += 2
        opposedCorner.totalCost += 2
        opposedCorner.numberMoved = opposedCorner.stateWhenAtNode[0][0]
        opposedCorner.stateWhenAtNode[1][3] = opposedCorner.stateWhenAtNode[0][0]
        opposedCorner.stateWhenAtNode[0][0] = "0"

        # Normal move, one step left
        oneStepLeft = copy.copy(nodeToCopy)
        oneStepLeft.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepLeft.numberMoved = oneStepLeft.stateWhenAtNode[1][2]
        oneStepLeft.stateWhenAtNode[1][3] = oneStepLeft.stateWhenAtNode[1][2]
        oneStepLeft.stateWhenAtNode[1][2] = "0"

        # Normal move, one step up
        oneStepUp = copy.copy(nodeToCopy)
        oneStepUp.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepUp.numberMoved = oneStepUp.stateWhenAtNode[0][3]
        oneStepUp.stateWhenAtNode[1][3] = oneStepUp.stateWhenAtNode[0][3]
        oneStepUp.stateWhenAtNode[0][3] = "0"

        generated.extend((wrappingNode, diagonalNode, opposedCorner, oneStepLeft, oneStepUp))
    elif indexOfEmpty == "0 1":
        # Normal move, one step left
        oneStepLeft = copy.copy(nodeToCopy)
        oneStepLeft.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepLeft.numberMoved = oneStepLeft.stateWhenAtNode[0][0]
        oneStepLeft.stateWhenAtNode[0][1] = oneStepLeft.stateWhenAtNode[0][0]
        oneStepLeft.stateWhenAtNode[0][0] = "0"

        # Normal move, one step right
        oneStepRight = copy.copy(nodeToCopy)
        oneStepRight.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepRight.numberMoved = oneStepRight.stateWhenAtNode[0][2]
        oneStepRight.stateWhenAtNode[0][1] = oneStepRight.stateWhenAtNode[0][2]
        oneStepRight.stateWhenAtNode[0][2] = "0"

        # Normal move, one step down
        oneStepDown = copy.copy(nodeToCopy)
        oneStepDown.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepDown.numberMoved = oneStepDown.stateWhenAtNode[1][1]
        oneStepDown.stateWhenAtNode[0][1] = oneStepDown.stateWhenAtNode[1][1]
        oneStepDown.stateWhenAtNode[1][1] = "0"

        generated.extend((oneStepRight, oneStepLeft, oneStepDown))

    elif indexOfEmpty == "0 2":
        # Normal move, one step left
        oneStepLeft = copy.copy(nodeToCopy)
        oneStepLeft.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepLeft.numberMoved = oneStepLeft.stateWhenAtNode[0][1]
        oneStepLeft.stateWhenAtNode[0][2] = oneStepLeft.stateWhenAtNode[0][1]
        oneStepLeft.stateWhenAtNode[0][1] = "0"

        # Normal move, one step right
        oneStepRight = copy.copy(nodeToCopy)
        oneStepRight.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepRight.numberMoved = oneStepRight.stateWhenAtNode[0][3]
        oneStepRight.stateWhenAtNode[0][2] = oneStepRight.stateWhenAtNode[0][3]
        oneStepRight.stateWhenAtNode[0][3] = "0"

        # Normal move, one step down
        oneStepDown = copy.copy(nodeToCopy)
        oneStepDown.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepDown.numberMoved = oneStepDown.stateWhenAtNode[1][2]
        oneStepDown.stateWhenAtNode[0][2] = oneStepDown.stateWhenAtNode[1][2]
        oneStepDown.stateWhenAtNode[1][2] = "0"

        generated.extend((oneStepRight, oneStepLeft, oneStepDown))
    elif indexOfEmpty == "1 1":
        # Normal move, one step left
        oneStepLeft = copy.copy(nodeToCopy)
        oneStepLeft.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepLeft.numberMoved = oneStepLeft.stateWhenAtNode[1][0]
        oneStepLeft.stateWhenAtNode[1][1] = oneStepLeft.stateWhenAtNode[1][0]
        oneStepLeft.stateWhenAtNode[1][0] = "0"

        # Normal move, one step right
        oneStepRight = copy.copy(nodeToCopy)
        oneStepRight.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepRight.numberMoved = oneStepRight.stateWhenAtNode[1][2]
        oneStepRight.stateWhenAtNode[1][1] = oneStepRight.stateWhenAtNode[1][2]
        oneStepRight.stateWhenAtNode[1][2] = "0"

        # Normal move, one step up
        oneStepUp = copy.copy(nodeToCopy)
        oneStepUp.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepUp.numberMoved = oneStepUp.stateWhenAtNode[0][1]
        oneStepUp.stateWhenAtNode[1][1] = oneStepUp.stateWhenAtNode[0][1]
        oneStepUp.stateWhenAtNode[0][1] = "0"

        generated.extend((oneStepRight, oneStepLeft, oneStepUp))
    else:
        # Normal move, one step left
        oneStepLeft = copy.copy(nodeToCopy)
        oneStepLeft.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepLeft.numberMoved = oneStepLeft.stateWhenAtNode[1][1]
        oneStepLeft.stateWhenAtNode[1][2] = oneStepLeft.stateWhenAtNode[1][1]
        oneStepLeft.stateWhenAtNode[1][1] = "0"

        # Normal move, one step right
        oneStepRight = copy.copy(nodeToCopy)
        oneStepRight.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepRight.numberMoved = oneStepRight.stateWhenAtNode[1][3]
        oneStepRight.stateWhenAtNode[1][2] = oneStepRight.stateWhenAtNode[1][3]
        oneStepRight.stateWhenAtNode[1][3] = "0"

        # Normal move, one step up
        oneStepUp = copy.copy(nodeToCopy)
        oneStepUp.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepUp.numberMoved = oneStepUp.stateWhenAtNode[0][2]
        oneStepUp.stateWhenAtNode[1][2] = oneStepUp.stateWhenAtNode[0][2]
        oneStepUp.stateWhenAtNode[0][2] = "0"

        generated.extend((oneStepRight, oneStepLeft, oneStepUp))

    for newNode in generated:
        if goalState(newNode):
            _end = True
            _goalNode = newNode
            return generated

    return generated


def createOutputFile(filePrefix, initialPuzzle, solutionNode, executeTime, searchPath):
    """
    Function for creating an output file for a puzzle. Creates a search file and a solution file.
    Takes as parameter the number of the puzzle and the name of the search, in the following format:
    puzzleNumber_searchName
    as filePrefix.
    """
    # Open solution file
    output = open('A2_Output/' + filePrefix + '_solution.txt', 'w')

    # Writing initial line of the solution file
    toWrite = "0 0 "
    for row in initialPuzzle:
        for col in row:
            toWrite += col + " "
    toWrite.rstrip()

    output.write(toWrite + '\n')

    # Checking if there is a solution
    if solutionNode.parent is not None:
        # ReOrdering the moves, so that the first move is first
        stack = []
        current = solutionNode
        while current.parent is not None:
            stack.append(current)
            current = current.parent
        while stack:
            # Writing the solution, node by node
            current = stack.pop()
            output.write(current.numberMoved + " " + str(current.cost) + " " + current.toOneLineString().rstrip() + '\n')
    else:
        output.write("no solution" + "\n")

    output.write(str(solutionNode.totalCost) + " " + str(executeTime % 60))

    # Close output file
    output.close()

    # Open search file
    output = open('A2_Output/' + filePrefix + '_search.txt', 'w')

    for nodes in searchPath:
        output.write(
            "f(n) = " + str(nodes.functionCost) + "g(n) = " + str(nodes.totalCost) + ",h(n) = " + str(nodes.heuristicCost) + ", state = " + nodes.toOneLineString().rstrip() + "\n")

    # Close output file
    output.close()


def resetGlobals():
    """
    Resets all the global variables used in the program, to prepare for the re-execution of the algorithm.
    """
    global _openList
    global _closedList
    global _goalNode
    global _end
    global _timeout
    global _startTime
    global _searchedNodes

    _openList = []
    _closedList = []
    _goalNode = Node(0, 0, 0, 0, [[]], None, -1)
    _end = False
    _timeout = False
    _startTime = 0
    _searchedNodes = []


# Finds the solution of the puzzle using GBFS if possible with a given heuristic function
def gbfs(node, h_func):
    global _timeout
    global _end
    global _searchedNodes
    global _openList
    global _closedList
    
    _openList.append(node)

    # For as long as we don't have a solution, pop the first node of the open list.
    while not _end and len(_openList) != 0:
        if timeout():
            _timeout = True
            _end = True
            break

        possibleMoves = findMoves(_openList.pop(0))

        # For each of our node, check the closed list to see if it's there. If it's there, we don't want it.
        for newNode in possibleMoves:
            found = next((n for n in _closedList if n.stateWhenAtNode == newNode.stateWhenAtNode), None)
            if found is None:
                # We now check if it's in our open list. If it's not there, add the node and compute its heuristic value
                found = next((n for n in _openList if n.stateWhenAtNode == newNode.stateWhenAtNode), None)
                if found is None:
                    newNode.heuristicCost = h_func(newNode.stateWhenAtNode)
                    _openList.append(newNode)

        # Sorting the open list by heuristic of the nodes.
        sorted(_openList, key=lambda n: n.heuristicCost)

    _searchedNodes = _closedList
    
    # If we are here, we either have a solution or we failed to find one.
    if _end and not _timeout:
        print("Solution found.")
    elif _timeout:
        print("Timed out. Longer than " + str(TIMEOUT_TIME_IN_SECONDS) + " seconds passed.")
    else:
        print("Failed to find a solution to the puzzle.")

# h0 given in assignment insructions
def h0(nodeState):
    if (nodeState[len(nodeState)-1][len(nodeState[0])-1] == '0'):
        return 0
    else:
        return 1

# Heuristic function 1: Manhattan distance from passed node state. 
def manhattanDistance(nodeState):
    goals = [_goalList1, _goalList2]
    h = [0] * len(goals)
    
    for i in range(len(h)):
        for j in range(len(goals[i])):
            for k in range(len(goals[i][j])):
                if (nodeState[j][k] != '0'):
                    r, c = index_2d(goals[i], nodeState[j][k])
                    abs(j - r)
                    h[i] += abs(j - r) + abs(k - c)
                    
    return min(h)
  
# Heuristic function 2: Diagonal distance (cost of moving horizontally/vertically is 1, diagonal is 3) from passed node state
def diagonalDistance(nodeState, D=1, D2=3):
    goals = [_goalList1, _goalList2]
    h = [0] * len(goals)
    
    for i in range(len(h)):
        for j in range(len(goals[i])):
            for k in range(len(goals[i][j])):
                if (nodeState[j][k] != '0'):
                    r, c = index_2d(goals[i], nodeState[j][k])
                    dx = abs(j - r)
                    dy = abs(k - c)
                    h[i] += D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
    
    return min(h)

def hamming(nodeState):
    goals = [_goalList1, _goalList2]
    h = [0] * len(goals)
    
    for i in range(len(h)):
        for j in range(len(goals[i])):
            for k in range(len(goals[i][j])):
                if (nodeState[j][k] != '0' and nodeState[j][k] != goals[i][j][k]):
                    h[i] += 1
    
    return min(h)
    
# Helper function to get the indexes of a value in the passed list
def index_2d(someList, value):
    for i, x in enumerate(someList):
        if value in x:
            return (i, x.index(value))
 
# Set the starting time of the algorithm       
def startTimer():
    global _startTime
    _startTime = time.time()
    return _startTime