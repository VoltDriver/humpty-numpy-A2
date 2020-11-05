import copy

# --------------- Constants ---------------
TOP_LEFT_CORNER = "0 0"
TOP_RIGHT_CORNER = "0 3"
BOTTOM_LEFT_CORNER = "1 0"
BOTTOM_RIGHT_CORNER = "1 3"

# --------------- Global Variables ---------------
_openList = []
_closedList = []
# Initializing the goal node object, to be used later.
_goalNode = None
# This variable defines if we have found the solution or not.
_end = False

# Building the goalList
_goalList = [[]]
row1 = []
row2 = []
for num in range(4):
    row1.append(str(num + 1))
for num in range(3):
    row2.append(str(num + 5))
row2.append("0")
_goalList.append(row1)
_goalList.append(row2)


# --------------- Custom classes ---------------

class Node:
    def __init__(self, heuristicCost, cost, totalCost, stateWhenAtNode, parent):
        self.heuristicCost = heuristicCost
        self.cost = cost
        self.totalCost = totalCost
        self.stateWhenAtNode = stateWhenAtNode
        self.parent = parent

    def __cmp__(self, other):
        return __cmp__(self.totalCost, other.totalCost)

    def getEmptySpaceIndex(self):
        row = 0
        col = 0
        for rows in self.stateWhenAtNode:
            for cols in rows:
                if cols == '0':
                    return str(row) + " " + str(col)
                else:
                    col += 1
            row += 1


# --------------- Functions ---------------

def load_input(filename):
    '''
    Function for loading the initial puzzles, in format 2x4, from a text file.
    '''
    file = open(filename, "r")
    data = file.readlines()

    puzzleList = []
    for puzzle in data:
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
    if node.stateWhenAtNode == _goalList:
        return True
    return False


def findSolution(node):
    possibleMoves = findMoves(node)

    # For each of our node, check the closed list to see if it's there. If it's there, we don't want it.
    for newNode in possibleMoves:
        found = next((n for n in _closedList if n.stateWhenAtNode == newNode.stateWhenAtNode), None)
        if found is None:
            # We now check if it's in our open list. If it's there, we update the cost if we have a lower total cost.
            # If not, we add it to the open list.
            found = next((n for n in _openList if n.stateWhenAtNode == newNode.stateWhenAtNode), None)
            if found is None:
                _openList.append(newNode)
            else:
                if found.totalCost > newNode.totalCost:
                    _openList.remove(found)
                    _openList.append(newNode)

    _openList.sort()

    # For as long as we don't have a solution, pop the first node of the open list.
    while not _end and len(_openList) != 0:
        findSolution(_openList.pop(0))

    # If we are here, we either have a solution or we failed to find one.
    if _end:
        print("Solution found.")
        print(_goalNode)
    else:
        print("Failed to find a solution to the puzzle.")


def findMoves(node):
    global _end
    global _goalNode

    if _end:
        return

    _closedList.append(node)
    _openList.remove(node)

    # Check if we are at goalState
    if goalState(node):
        goalNode = node
        end = True
        return

    # find where the empty space is in node's gamestate
    indexOfEmpty = node.getEmptySpaceIndex()

    generated = []

    # Initializing Node to copy
    costOfMove = 1
    nodeToCopy = copy.deepcopy(node)
    nodeToCopy.totalCost += costOfMove
    nodeToCopy.cost = costOfMove
    nodeToCopy.parent = node

    if indexOfEmpty == TOP_LEFT_CORNER:
        # Wrapping move
        wrappingNode = copy.deepcopy(nodeToCopy)
        wrappingNode.stateWhenAtNode[0][0] = wrappingNode.stateWhenAtNode[0][3]
        wrappingNode.stateWhenAtNode[0][3] = "0"
        wrappingNode.cost += 1
        wrappingNode.totalCost += 1

        # Diagonal move
        diagonalNode = copy.deepcopy(nodeToCopy)
        diagonalNode.cost += 2
        diagonalNode.totalCost += 2
        diagonalNode.stateWhenAtNode[0][0] = diagonalNode.stateWhenAtNode[1][1]
        diagonalNode.stateWhenAtNode[1][1] = "0"

        # OpposedCorner move
        opposedCorner = copy.deepcopy(nodeToCopy)
        opposedCorner.cost += 2
        opposedCorner.totalCost += 2
        opposedCorner.stateWhenAtNode[0][0] = opposedCorner.stateWhenAtNode[1][3]
        opposedCorner.stateWhenAtNode[1][3] = "0"

        # Normal move, one step right
        oneStepRight = copy.deepcopy(nodeToCopy)
        oneStepRight.stateWhenAtNode[0][0] = oneStepRight.stateWhenAtNode[0][1]
        oneStepRight.stateWhenAtNode[0][1] = "0"

        # Normal move, one step down
        oneStepDown = copy.deepcopy(nodeToCopy)
        oneStepDown.stateWhenAtNode[0][0] = oneStepDown.stateWhenAtNode[1][0]
        oneStepDown.stateWhenAtNode[1][0] = "0"

        generated.extend((wrappingNode, diagonalNode, opposedCorner, oneStepRight, oneStepDown))
    elif indexOfEmpty == TOP_RIGHT_CORNER:
        # Wrapping move
        wrappingNode = copy.deepcopy(nodeToCopy)
        wrappingNode.stateWhenAtNode[0][3] = wrappingNode.stateWhenAtNode[0][0]
        wrappingNode.stateWhenAtNode[0][0] = "0"
        wrappingNode.cost += 1
        wrappingNode.totalCost += 1

        # Diagonal move
        diagonalNode = copy.deepcopy(nodeToCopy)
        diagonalNode.cost += 2
        diagonalNode.totalCost += 2
        diagonalNode.stateWhenAtNode[0][3] = diagonalNode.stateWhenAtNode[1][2]
        diagonalNode.stateWhenAtNode[1][2] = "0"

        # OpposedCorner move
        opposedCorner = copy.deepcopy(nodeToCopy)
        opposedCorner.cost += 2
        opposedCorner.totalCost += 2
        opposedCorner.stateWhenAtNode[0][3] = opposedCorner.stateWhenAtNode[1][0]
        opposedCorner.stateWhenAtNode[1][0] = "0"

        # Normal move, one step left
        oneStepLeft = copy.deepcopy(nodeToCopy)
        oneStepLeft.stateWhenAtNode[0][3] = oneStepLeft.stateWhenAtNode[0][2]
        oneStepLeft.stateWhenAtNode[0][2] = "0"

        # Normal move, one step down
        oneStepDown = copy.deepcopy(nodeToCopy)
        oneStepDown.stateWhenAtNode[0][3] = oneStepDown.stateWhenAtNode[1][3]
        oneStepDown.stateWhenAtNode[1][3] = "0"

        generated.extend((wrappingNode, diagonalNode, opposedCorner, oneStepLeft, oneStepDown))

    elif indexOfEmpty == BOTTOM_LEFT_CORNER:
        # Wrapping move
        wrappingNode = copy.deepcopy(nodeToCopy)
        wrappingNode.stateWhenAtNode[1][0] = wrappingNode.stateWhenAtNode[1][3]
        wrappingNode.stateWhenAtNode[1][3] = "0"
        wrappingNode.cost += 1
        wrappingNode.totalCost += 1

        # Diagonal move
        diagonalNode = copy.deepcopy(nodeToCopy)
        diagonalNode.cost += 2
        diagonalNode.totalCost += 2
        diagonalNode.stateWhenAtNode[1][0] = diagonalNode.stateWhenAtNode[0][1]
        diagonalNode.stateWhenAtNode[0][1] = "0"

        # OpposedCorner move
        opposedCorner = copy.deepcopy(nodeToCopy)
        opposedCorner.cost += 2
        opposedCorner.totalCost += 2
        opposedCorner.stateWhenAtNode[1][0] = opposedCorner.stateWhenAtNode[0][3]
        opposedCorner.stateWhenAtNode[0][3] = "0"

        # Normal move, one step right
        oneStepRight = copy.deepcopy(nodeToCopy)
        oneStepRight.stateWhenAtNode[1][0] = oneStepRight.stateWhenAtNode[1][1]
        oneStepRight.stateWhenAtNode[1][1] = "0"

        # Normal move, one step up
        oneStepUp = copy.deepcopy(nodeToCopy)
        oneStepUp.stateWhenAtNode[1][0] = oneStepUp.stateWhenAtNode[0][0]
        oneStepUp.stateWhenAtNode[0][0] = "0"

        generated.extend((wrappingNode, diagonalNode, opposedCorner, oneStepRight, oneStepUp))
    elif indexOfEmpty == BOTTOM_RIGHT_CORNER:
        # Wrapping move
        wrappingNode = copy.deepcopy(nodeToCopy)
        wrappingNode.stateWhenAtNode[1][3] = wrappingNode.stateWhenAtNode[1][0]
        wrappingNode.stateWhenAtNode[1][0] = "0"
        wrappingNode.cost += 1
        wrappingNode.totalCost += 1

        # Diagonal move
        diagonalNode = copy.deepcopy(nodeToCopy)
        diagonalNode.cost += 2
        diagonalNode.totalCost += 2
        diagonalNode.stateWhenAtNode[1][3] = diagonalNode.stateWhenAtNode[0][2]
        diagonalNode.stateWhenAtNode[0][2] = "0"

        # OpposedCorner move
        opposedCorner = copy.deepcopy(nodeToCopy)
        opposedCorner.cost += 2
        opposedCorner.totalCost += 2
        opposedCorner.stateWhenAtNode[1][3] = opposedCorner.stateWhenAtNode[0][0]
        opposedCorner.stateWhenAtNode[0][0] = "0"

        # Normal move, one step left
        oneStepLeft = copy.deepcopy(nodeToCopy)
        oneStepLeft.stateWhenAtNode[1][3] = oneStepLeft.stateWhenAtNode[1][2]
        oneStepLeft.stateWhenAtNode[1][2] = "0"

        # Normal move, one step up
        oneStepUp = copy.deepcopy(nodeToCopy)
        oneStepUp.stateWhenAtNode[1][3] = oneStepUp.stateWhenAtNode[0][3]
        oneStepUp.stateWhenAtNode[0][3] = "0"

        generated.extend((wrappingNode, diagonalNode, opposedCorner, oneStepLeft, oneStepUp))
    elif indexOfEmpty == "0 1":
        # Normal move, one step left
        oneStepLeft = copy.deepcopy(nodeToCopy)
        oneStepLeft.stateWhenAtNode[0][1] = oneStepLeft.stateWhenAtNode[0][0]
        oneStepLeft.stateWhenAtNode[0][0] = "0"

        # Normal move, one step right
        oneStepRight = copy.deepcopy(nodeToCopy)
        oneStepRight.stateWhenAtNode[0][1] = oneStepRight.stateWhenAtNode[0][2]
        oneStepRight.stateWhenAtNode[0][2] = "0"

        # Normal move, one step down
        oneStepDown = copy.deepcopy(nodeToCopy)
        oneStepDown.stateWhenAtNode[0][1] = oneStepDown.stateWhenAtNode[1][1]
        oneStepDown.stateWhenAtNode[1][1] = "0"

        generated.extend((oneStepRight, oneStepLeft, oneStepDown))

    elif indexOfEmpty == "0 2":
        # Normal move, one step left
        oneStepLeft = copy.deepcopy(nodeToCopy)
        oneStepLeft.stateWhenAtNode[0][2] = oneStepLeft.stateWhenAtNode[0][1]
        oneStepLeft.stateWhenAtNode[0][1] = "0"

        # Normal move, one step right
        oneStepRight = copy.deepcopy(nodeToCopy)
        oneStepRight.stateWhenAtNode[0][2] = oneStepRight.stateWhenAtNode[0][3]
        oneStepRight.stateWhenAtNode[0][3] = "0"

        # Normal move, one step down
        oneStepDown = copy.deepcopy(nodeToCopy)
        oneStepDown.stateWhenAtNode[0][2] = oneStepDown.stateWhenAtNode[1][2]
        oneStepDown.stateWhenAtNode[1][2] = "0"

        generated.extend((oneStepRight, oneStepLeft, oneStepDown))
    elif indexOfEmpty == "1 1":
        # Normal move, one step left
        oneStepLeft = copy.deepcopy(nodeToCopy)
        oneStepLeft.stateWhenAtNode[1][1] = oneStepLeft.stateWhenAtNode[1][0]
        oneStepLeft.stateWhenAtNode[1][0] = "0"

        # Normal move, one step right
        oneStepRight = copy.deepcopy(nodeToCopy)
        oneStepRight.stateWhenAtNode[1][1] = oneStepRight.stateWhenAtNode[1][2]
        oneStepRight.stateWhenAtNode[1][2] = "0"

        # Normal move, one step up
        oneStepUp = copy.deepcopy(nodeToCopy)
        oneStepUp.stateWhenAtNode[1][1] = oneStepUp.stateWhenAtNode[0][1]
        oneStepUp.stateWhenAtNode[0][1] = "0"

        generated.extend((oneStepRight, oneStepLeft, oneStepUp))
    else:
        # Normal move, one step left
        oneStepLeft = copy.deepcopy(nodeToCopy)
        oneStepLeft.stateWhenAtNode[1][2] = oneStepLeft.stateWhenAtNode[1][1]
        oneStepLeft.stateWhenAtNode[1][1] = "0"

        # Normal move, one step right
        oneStepRight = copy.deepcopy(nodeToCopy)
        oneStepRight.stateWhenAtNode[1][2] = oneStepRight.stateWhenAtNode[1][3]
        oneStepRight.stateWhenAtNode[1][3] = "0"

        # Normal move, one step up
        oneStepUp = copy.deepcopy(nodeToCopy)
        oneStepUp.stateWhenAtNode[1][2] = oneStepUp.stateWhenAtNode[0][2]
        oneStepUp.stateWhenAtNode[0][2] = "0"

        generated.extend((oneStepRight, oneStepLeft, oneStepUp))

    for newNode in generated:
        if goalState(newNode):
            _end = True
            _goalNode = newNode

    return generated


# Load puzzles
data = load_input("A2_Input/samplePuzzles.txt")
for line in data:
    for element in line:
        print(element)

# Finding Solution
currentPuzzle = data[0]
startNode = Node(0, 0, 0, currentPuzzle, None)
findSolution(startNode)
