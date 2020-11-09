import copy


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


# --------------- Constants ---------------
TOP_LEFT_CORNER = "0 0"
TOP_RIGHT_CORNER = "0 3"
BOTTOM_LEFT_CORNER = "1 0"
BOTTOM_RIGHT_CORNER = "1 3"

# --------------- Global Variables ---------------
_openList = []
_closedList = []
# Initializing the goal node object, to be used later.
_goalNode = Node(0, 0, 0, [[]], None)
# This variable defines if we have found the solution or not.
_end = False

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
    _openList.append(node)

    # For as long as we don't have a solution, pop the first node of the open list.
    while not _end and len(_openList) != 0:
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

    # If we are here, we either have a solution or we failed to find one.
    if _end:
        print("Solution found.")
        print(_goalNode)
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
        goalNode = node
        end = True
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
        wrappingNode.stateWhenAtNode[0][0] = wrappingNode.stateWhenAtNode[0][3]
        wrappingNode.stateWhenAtNode[0][3] = "0"
        wrappingNode.cost += 1
        wrappingNode.totalCost += 1

        # Diagonal move
        diagonalNode = copy.copy(nodeToCopy)
        diagonalNode.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        diagonalNode.cost += 2
        diagonalNode.totalCost += 2
        diagonalNode.stateWhenAtNode[0][0] = diagonalNode.stateWhenAtNode[1][1]
        diagonalNode.stateWhenAtNode[1][1] = "0"

        # OpposedCorner move
        opposedCorner = copy.copy(nodeToCopy)
        opposedCorner.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        opposedCorner.cost += 2
        opposedCorner.totalCost += 2
        opposedCorner.stateWhenAtNode[0][0] = opposedCorner.stateWhenAtNode[1][3]
        opposedCorner.stateWhenAtNode[1][3] = "0"

        # Normal move, one step right
        oneStepRight = copy.copy(nodeToCopy)
        oneStepRight.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepRight.stateWhenAtNode[0][0] = oneStepRight.stateWhenAtNode[0][1]
        oneStepRight.stateWhenAtNode[0][1] = "0"

        # Normal move, one step down
        oneStepDown = copy.copy(nodeToCopy)
        oneStepDown.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepDown.stateWhenAtNode[0][0] = oneStepDown.stateWhenAtNode[1][0]
        oneStepDown.stateWhenAtNode[1][0] = "0"

        generated.extend((wrappingNode, diagonalNode, opposedCorner, oneStepRight, oneStepDown))
    elif indexOfEmpty == TOP_RIGHT_CORNER:
        # Wrapping move
        wrappingNode = copy.copy(nodeToCopy)
        wrappingNode.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        wrappingNode.stateWhenAtNode[0][3] = wrappingNode.stateWhenAtNode[0][0]
        wrappingNode.stateWhenAtNode[0][0] = "0"
        wrappingNode.cost += 1
        wrappingNode.totalCost += 1

        # Diagonal move
        diagonalNode = copy.copy(nodeToCopy)
        diagonalNode.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        diagonalNode.cost += 2
        diagonalNode.totalCost += 2
        diagonalNode.stateWhenAtNode[0][3] = diagonalNode.stateWhenAtNode[1][2]
        diagonalNode.stateWhenAtNode[1][2] = "0"

        # OpposedCorner move
        opposedCorner = copy.copy(nodeToCopy)
        opposedCorner.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        opposedCorner.cost += 2
        opposedCorner.totalCost += 2
        opposedCorner.stateWhenAtNode[0][3] = opposedCorner.stateWhenAtNode[1][0]
        opposedCorner.stateWhenAtNode[1][0] = "0"

        # Normal move, one step left
        oneStepLeft = copy.copy(nodeToCopy)
        oneStepLeft.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
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
        wrappingNode.stateWhenAtNode[1][0] = wrappingNode.stateWhenAtNode[1][3]
        wrappingNode.stateWhenAtNode[1][3] = "0"
        wrappingNode.cost += 1
        wrappingNode.totalCost += 1

        # Diagonal move
        diagonalNode = copy.copy(nodeToCopy)
        diagonalNode.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        diagonalNode.cost += 2
        diagonalNode.totalCost += 2
        diagonalNode.stateWhenAtNode[1][0] = diagonalNode.stateWhenAtNode[0][1]
        diagonalNode.stateWhenAtNode[0][1] = "0"

        # OpposedCorner move
        opposedCorner = copy.copy(nodeToCopy)
        opposedCorner.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        opposedCorner.cost += 2
        opposedCorner.totalCost += 2
        opposedCorner.stateWhenAtNode[1][0] = opposedCorner.stateWhenAtNode[0][3]
        opposedCorner.stateWhenAtNode[0][3] = "0"

        # Normal move, one step right
        oneStepRight = copy.copy(nodeToCopy)
        oneStepRight.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepRight.stateWhenAtNode[1][0] = oneStepRight.stateWhenAtNode[1][1]
        oneStepRight.stateWhenAtNode[1][1] = "0"

        # Normal move, one step up
        oneStepUp = copy.copy(nodeToCopy)
        oneStepUp.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepUp.stateWhenAtNode[1][0] = oneStepUp.stateWhenAtNode[0][0]
        oneStepUp.stateWhenAtNode[0][0] = "0"

        generated.extend((wrappingNode, diagonalNode, opposedCorner, oneStepRight, oneStepUp))
    elif indexOfEmpty == BOTTOM_RIGHT_CORNER:
        # Wrapping move
        wrappingNode = copy.copy(nodeToCopy)
        wrappingNode.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        wrappingNode.stateWhenAtNode[1][3] = wrappingNode.stateWhenAtNode[1][0]
        wrappingNode.stateWhenAtNode[1][0] = "0"
        wrappingNode.cost += 1
        wrappingNode.totalCost += 1

        # Diagonal move
        diagonalNode = copy.copy(nodeToCopy)
        diagonalNode.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        diagonalNode.cost += 2
        diagonalNode.totalCost += 2
        diagonalNode.stateWhenAtNode[1][3] = diagonalNode.stateWhenAtNode[0][2]
        diagonalNode.stateWhenAtNode[0][2] = "0"

        # OpposedCorner move
        opposedCorner = copy.copy(nodeToCopy)
        opposedCorner.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        opposedCorner.cost += 2
        opposedCorner.totalCost += 2
        opposedCorner.stateWhenAtNode[1][3] = opposedCorner.stateWhenAtNode[0][0]
        opposedCorner.stateWhenAtNode[0][0] = "0"

        # Normal move, one step left
        oneStepLeft = copy.copy(nodeToCopy)
        oneStepLeft.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepLeft.stateWhenAtNode[1][3] = oneStepLeft.stateWhenAtNode[1][2]
        oneStepLeft.stateWhenAtNode[1][2] = "0"

        # Normal move, one step up
        oneStepUp = copy.copy(nodeToCopy)
        oneStepUp.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepUp.stateWhenAtNode[1][3] = oneStepUp.stateWhenAtNode[0][3]
        oneStepUp.stateWhenAtNode[0][3] = "0"

        generated.extend((wrappingNode, diagonalNode, opposedCorner, oneStepLeft, oneStepUp))
    elif indexOfEmpty == "0 1":
        # Normal move, one step left
        oneStepLeft = copy.copy(nodeToCopy)
        oneStepLeft.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepLeft.stateWhenAtNode[0][1] = oneStepLeft.stateWhenAtNode[0][0]
        oneStepLeft.stateWhenAtNode[0][0] = "0"

        # Normal move, one step right
        oneStepRight = copy.copy(nodeToCopy)
        oneStepRight.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepRight.stateWhenAtNode[0][1] = oneStepRight.stateWhenAtNode[0][2]
        oneStepRight.stateWhenAtNode[0][2] = "0"

        # Normal move, one step down
        oneStepDown = copy.copy(nodeToCopy)
        oneStepDown.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepDown.stateWhenAtNode[0][1] = oneStepDown.stateWhenAtNode[1][1]
        oneStepDown.stateWhenAtNode[1][1] = "0"

        generated.extend((oneStepRight, oneStepLeft, oneStepDown))

    elif indexOfEmpty == "0 2":
        # Normal move, one step left
        oneStepLeft = copy.copy(nodeToCopy)
        oneStepLeft.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepLeft.stateWhenAtNode[0][2] = oneStepLeft.stateWhenAtNode[0][1]
        oneStepLeft.stateWhenAtNode[0][1] = "0"

        # Normal move, one step right
        oneStepRight = copy.copy(nodeToCopy)
        oneStepRight.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepRight.stateWhenAtNode[0][2] = oneStepRight.stateWhenAtNode[0][3]
        oneStepRight.stateWhenAtNode[0][3] = "0"

        # Normal move, one step down
        oneStepDown = copy.copy(nodeToCopy)
        oneStepDown.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepDown.stateWhenAtNode[0][2] = oneStepDown.stateWhenAtNode[1][2]
        oneStepDown.stateWhenAtNode[1][2] = "0"

        generated.extend((oneStepRight, oneStepLeft, oneStepDown))
    elif indexOfEmpty == "1 1":
        # Normal move, one step left
        oneStepLeft = copy.copy(nodeToCopy)
        oneStepLeft.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepLeft.stateWhenAtNode[1][1] = oneStepLeft.stateWhenAtNode[1][0]
        oneStepLeft.stateWhenAtNode[1][0] = "0"

        # Normal move, one step right
        oneStepRight = copy.copy(nodeToCopy)
        oneStepRight.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepRight.stateWhenAtNode[1][1] = oneStepRight.stateWhenAtNode[1][2]
        oneStepRight.stateWhenAtNode[1][2] = "0"

        # Normal move, one step up
        oneStepUp = copy.copy(nodeToCopy)
        oneStepUp.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepUp.stateWhenAtNode[1][1] = oneStepUp.stateWhenAtNode[0][1]
        oneStepUp.stateWhenAtNode[0][1] = "0"

        generated.extend((oneStepRight, oneStepLeft, oneStepUp))
    else:
        # Normal move, one step left
        oneStepLeft = copy.copy(nodeToCopy)
        oneStepLeft.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepLeft.stateWhenAtNode[1][2] = oneStepLeft.stateWhenAtNode[1][1]
        oneStepLeft.stateWhenAtNode[1][1] = "0"

        # Normal move, one step right
        oneStepRight = copy.copy(nodeToCopy)
        oneStepRight.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepRight.stateWhenAtNode[1][2] = oneStepRight.stateWhenAtNode[1][3]
        oneStepRight.stateWhenAtNode[1][3] = "0"

        # Normal move, one step up
        oneStepUp = copy.copy(nodeToCopy)
        oneStepUp.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
        oneStepUp.stateWhenAtNode[1][2] = oneStepUp.stateWhenAtNode[0][2]
        oneStepUp.stateWhenAtNode[0][2] = "0"

        generated.extend((oneStepRight, oneStepLeft, oneStepUp))

    for newNode in generated:
        if goalState(newNode):
            _end = True
            _goalNode = newNode
            return generated

    return generated


# Load puzzles
data = load_input("A2_Input/samplePuzzles.txt")
for line in data:
    for element in line:
        print(element)

# Testing goalState

test1 = Node(0, 0, 0, [['1', '2', '3', '4'], ['5', '6', '7', '0']], None)  # is a goal
test2 = Node(0, 0, 0, [['1', '3', '2', '4'], ['5', '6', '7', '0']], None)  # is not a goal
test3 = Node(0, 0, 0, [['1', '2', '6', '4'], ['5', '3', '7', '0']], None)  # is not a goal
test4 = Node(0, 0, 0, [['1', '3', '5', '7'], ['2', '4', '6', '0']], None)  # is a goal, second way

isGoal1 = goalState(test1)
isGoal2 = goalState(test2)
isGoal3 = goalState(test3)
isGoal4 = goalState(test4)

# Finding Solution
currentPuzzle = data[0]
startNode = Node(0, 0, 0, currentPuzzle, None)
findSolution(startNode)

finalNode = _goalNode
print("Total cost is " + str(finalNode.totalCost) + "\n")

if finalNode.parent is not None:
    curNode = finalNode
    while curNode.parent is not None:
        print("-------")
        line = ""
        for row in curNode.stateWhenAtNode:
            line += "[ "
            for col in row:
                line += col + " "
            line += "] \n"
        print(line)
        curNode = curNode.parent
