import copy
import time
import numpy as np
from random import randrange

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
        self.initialized = False

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

# Building the goalLists, one for each goal state.
def goalList(length, width):
    _goalList1 = []
    for row in range(width):
        _goalList1.append([])
        for num in range(1,length+1):
            if (row == width-1 and num == length):
                _goalList1[row].append('0')
            else:
                _goalList1[row].append(str(num + row * length))

    #_goalList1[width-1].append("0")

    _goalList2 = []
    for row in range(width):
        _goalList2.append([])
        for num in range(1,length*width,width):
            if (num+row*1 == length*width):
                _goalList2[row].append("0")
            else:
                _goalList2[row].append(str(num+row*1))
    return _goalList1, _goalList2

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

def puzzlegenerator(length, width):
    x = np.random.permutation(np.arange(0,length*width)).reshape(width, length)
    l=[]
    for i in x:
        l.append(list(i))
    return l

# Verifies if a node is in a goal state. If it is, returns true. If not, returns false.
def goalState(node, _goalList1, _goalList2):
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

def tileNames(row, column, length, width):
    a = np.arange(1,length*width+1)
    a = a.reshape(width, length)
    for i in range(len(a[0])):
        for k in range(len(a)):
            if k == row and i == column:
                return a[k][i]

def findMoves(node,puzzle, _goalList1, _goalList2):
    global _end
    global _goalNode
    global _openList
    global _closedList

    if _end:
        return

    _closedList.append(node)

    # Check if we are at goalState
    if goalState(node, _goalList1, _goalList2):
        _goalNode = node
        _end = True
        return [node]

    # find where the empty space is in node's gamestate
    indexOfEmpty = node.getEmptySpaceIndex()
    indexOfEmpty = np.fromstring(indexOfEmpty, dtype=int, sep=' ')
    generated = []

    # Initializing Node to copy
    costOfMove = 1
    nodeToCopy = copy.copy(node)
    nodeToCopy.stateWhenAtNode = copy.deepcopy(node.stateWhenAtNode)
    nodeToCopy.totalCost += costOfMove
    nodeToCopy.cost = costOfMove
    nodeToCopy.parent = node
    #print("index %s" %indexOfEmpty)

    # wrapping move left and right
    wrappingNode = copy.copy(nodeToCopy)
    wrappingNode.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
    oneStepRight = copy.copy(nodeToCopy)
    oneStepRight.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
    oneStepLeft = copy.copy(nodeToCopy)
    oneStepLeft.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
    if (indexOfEmpty[1] == (len(puzzle[0])-1) or indexOfEmpty[1] == 0):
        if (indexOfEmpty[1] == 0):
            #0 goes left
            wrappingNode.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]] = wrappingNode.stateWhenAtNode[indexOfEmpty[0]][len(puzzle)-1]
            wrappingNode.stateWhenAtNode[indexOfEmpty[0]][len(puzzle)-1] = "0"
            #0 goes right normal move
            oneStepRight.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]] = oneStepRight.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]+1]
            oneStepRight.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1] + 1] = "0"

            wrappingNode.numberMoved = int(wrappingNode.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]])
            oneStepRight.numberMoved = int(oneStepRight.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]])

            wrappingNode.initialized = True
            oneStepRight.initialized = True

        elif (indexOfEmpty[1] == (len(puzzle[0])-1)):
            #0 goes right
            wrappingNode.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]] = wrappingNode.stateWhenAtNode[indexOfEmpty[0]][0]
            wrappingNode.stateWhenAtNode[indexOfEmpty[0]][0] = "0"
            #0 goes left normal move
            oneStepLeft.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]] = oneStepLeft.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]-1]
            oneStepLeft.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]-1] = "0"

            wrappingNode.numberMoved = int(wrappingNode.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]])
            oneStepLeft.numberMoved = int(oneStepLeft.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]])

            wrappingNode.initialized = True
            oneStepLeft.initialized = True

        wrappingNode.cost += 1
        wrappingNode.totalCost += 1
        #no added cost for normal moves
    else:
        #no edge piece 0 goes left
        oneStepLeft.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]] = oneStepLeft.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1] - 1]
        oneStepLeft.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1] - 1] = "0"
        #no edge piece 0 goes right
        oneStepRight.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]] = oneStepRight.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1] + 1]
        oneStepRight.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1] + 1] = "0"

        oneStepLeft.numberMoved = int(oneStepLeft.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]])
        oneStepRight.numberMoved = int(oneStepRight.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]])

        oneStepLeft.initialized = True
        oneStepRight.initialized = True

    #diagonal move
    diagonalNodeRightUp = copy.copy(nodeToCopy)
    diagonalNodeRightUp.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
    diagonalNodeRightDown = copy.copy(nodeToCopy)
    diagonalNodeRightDown.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
    diagonalNodeLeftDown = copy.copy(nodeToCopy)
    diagonalNodeLeftDown.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
    diagonalNodeLeftUp = copy.copy(nodeToCopy)
    diagonalNodeLeftUp.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)

    if (indexOfEmpty[0] == 0):
        if (indexOfEmpty[1] == 0):
            diagonalNodeRightDown.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]] = diagonalNodeRightDown.stateWhenAtNode[indexOfEmpty[0]+1][indexOfEmpty[1]+1]
            diagonalNodeRightDown.stateWhenAtNode[indexOfEmpty[0] + 1][indexOfEmpty[1] + 1] = "0"
            diagonalNodeRightDown.numberMoved = int(diagonalNodeRightDown.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]])

            diagonalNodeLeftDown.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]] = diagonalNodeLeftDown.stateWhenAtNode[indexOfEmpty[0]+1][len(puzzle[0])-1]
            diagonalNodeLeftDown.stateWhenAtNode[indexOfEmpty[0]][len(puzzle[0])-1] = "0"
            diagonalNodeLeftDown.numberMoved = int(diagonalNodeLeftDown.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]])

        elif (indexOfEmpty[1] == (len(puzzle)-1)):
            diagonalNodeRightDown.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]] = diagonalNodeRightDown.stateWhenAtNode[indexOfEmpty[0]+1][0]
            diagonalNodeRightDown.stateWhenAtNode[indexOfEmpty[0]+1][0] = "0"
            diagonalNodeRightDown.numberMoved = int(diagonalNodeRightDown.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]])

            diagonalNodeLeftDown.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]] = diagonalNodeLeftDown.stateWhenAtNode[indexOfEmpty[0]+1][indexOfEmpty[1]-1]
            diagonalNodeLeftDown.stateWhenAtNode[indexOfEmpty[0] + 1][indexOfEmpty[1] - 1] = "0"
            diagonalNodeLeftDown.numberMoved = int(diagonalNodeLeftDown.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]])

        diagonalNodeRightDown.initialized = True
        diagonalNodeLeftDown.initialized = True

    elif (indexOfEmpty[0] == (len(puzzle)-1)):
        if (indexOfEmpty[1] == 0):
            diagonalNodeLeftUp.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]] = diagonalNodeLeftUp.stateWhenAtNode[indexOfEmpty[0]-1][len(puzzle[0])-1]
            diagonalNodeLeftUp.stateWhenAtNode[indexOfEmpty[0]][len(puzzle[0])-1] = "0"
            diagonalNodeLeftUp.numberMoved = int(diagonalNodeLeftUp.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]])

            diagonalNodeRightUp.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]] = diagonalNodeRightUp.stateWhenAtNode[indexOfEmpty[0]-1][indexOfEmpty[1]+1]
            diagonalNodeRightUp.stateWhenAtNode[indexOfEmpty[0] - 1][indexOfEmpty[1] + 1] = "0"
            diagonalNodeRightUp.numberMoved = int(diagonalNodeRightUp.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]])

        elif (indexOfEmpty[1] == (len(puzzle[0])-1)):
            diagonalNodeRightUp.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]] = diagonalNodeRightUp.stateWhenAtNode[indexOfEmpty[0]-1][0]
            diagonalNodeRightUp.stateWhenAtNode[indexOfEmpty[0]-1][0] = "0"
            diagonalNodeRightUp.numberMoved = int(diagonalNodeRightUp.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]])

            diagonalNodeLeftUp.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]] = diagonalNodeLeftUp.stateWhenAtNode[indexOfEmpty[0]-1][indexOfEmpty[1]-1]
            diagonalNodeLeftUp.stateWhenAtNode[indexOfEmpty[0] - 1][indexOfEmpty[1] - 1] = "0"
            diagonalNodeLeftUp.numberMoved = int(diagonalNodeLeftUp.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]])

        diagonalNodeLeftUp.initialized = True
        diagonalNodeRightUp.initialized = True

    diagonalNodeRightUp.cost += 2
    diagonalNodeRightUp.totalCost += 2
    diagonalNodeRightDown.cost += 2
    diagonalNodeRightDown.totalCost += 2
    diagonalNodeLeftUp.cost += 2
    diagonalNodeLeftUp.totalCost += 2
    diagonalNodeLeftDown.cost += 2
    diagonalNodeLeftDown.totalCost += 2

    # Normal move, one step vertical
    oneStepDown = copy.copy(nodeToCopy)
    oneStepDown.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)
    oneStepUp = copy.copy(nodeToCopy)
    oneStepUp.stateWhenAtNode = copy.deepcopy(nodeToCopy.stateWhenAtNode)

    if(indexOfEmpty[0] == 0):
        #one step down for 0
        oneStepDown.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]] = oneStepDown.stateWhenAtNode[indexOfEmpty[0]+1][indexOfEmpty[1]]
        oneStepDown.stateWhenAtNode[indexOfEmpty[0]+1][indexOfEmpty[1]] = "0"
        oneStepDown.numberMoved = int(oneStepDown.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]])

        #wrapping for puzzles bigger than 2
        if (len(puzzle) > 2):
            oneStepUp.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]] = oneStepUp.stateWhenAtNode[len(puzzle)-1][indexOfEmpty[1]]
            oneStepUp.stateWhenAtNode[len(puzzle) - 1][indexOfEmpty[1]] = "0"
            oneStepUp.numberMoved = int(oneStepUp.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]])
        oneStepDown.initialized = True
        oneStepUp.initialized = True

    elif (indexOfEmpty[0] == (len(puzzle)-1)):
        #one step up for 0
        oneStepUp.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]] = oneStepUp.stateWhenAtNode[indexOfEmpty[0]-1][indexOfEmpty[1]]
        oneStepUp.stateWhenAtNode[indexOfEmpty[0]-1][indexOfEmpty[1]] = "0"
        oneStepUp.numberMoved = int(oneStepUp.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]])

        #wrapping for puzzles bigger than 2
        if (len(puzzle) > 2):
            oneStepDown.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]] = oneStepDown.stateWhenAtNode[0][indexOfEmpty[1]]
            oneStepDown.stateWhenAtNode[0][indexOfEmpty[1]] = "0"
            oneStepDown.numberMoved = int(oneStepDown.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]])
            oneStepDown.initialized = True

        oneStepUp.initialized = True
    else:
        # one step down for 0 - normal move
        oneStepDown.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]] = oneStepDown.stateWhenAtNode[indexOfEmpty[0] + 1][indexOfEmpty[1]]
        oneStepDown.stateWhenAtNode[indexOfEmpty[0] + 1][indexOfEmpty[1]] = "0"
        oneStepDown.numberMoved = int(oneStepDown.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]])

        # one step up for 0 - normal move
        oneStepUp.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]] = oneStepUp.stateWhenAtNode[indexOfEmpty[0] - 1][indexOfEmpty[1]]
        oneStepUp.stateWhenAtNode[indexOfEmpty[0] - 1][indexOfEmpty[1]] = "0"
        oneStepUp.numberMoved = int(oneStepUp.stateWhenAtNode[indexOfEmpty[0]][indexOfEmpty[1]])

        oneStepDown.initialized = True
        oneStepUp.initialized = True

    generated.extend((wrappingNode, diagonalNodeLeftUp, diagonalNodeLeftDown, diagonalNodeRightUp, diagonalNodeRightDown, oneStepRight, oneStepLeft, oneStepDown, oneStepUp))

    for k in range(3):
        for i in generated:
            if not i.initialized:
                generated.remove(i)


    for newNode in generated:
        if goalState(newNode,_goalList1, _goalList2):
            _end = True
            _goalNode = newNode
            return generated

    return generated

#UCS
def findSolution(node, _goalList1, _goalList2):
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

        parentNode = _openList.pop(0)
        possibleMoves = findMoves(parentNode, parentNode.stateWhenAtNode, _goalList1, _goalList2)

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
        _openList = sorted(_openList, key=lambda n: n.totalCost)

    _searchedNodes = _closedList

    # If we are here, we either have a solution or we failed to find one.
    if _end and not _timeout:
        print("Solution found.")
    elif _timeout:
        print("Timed out. Longer than " + str(TIMEOUT_TIME_IN_SECONDS) + " seconds passed.")
    else:
        print("Failed to find a solution to the puzzle.")


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
            output.write(
                str(current.numberMoved) + " " + str(current.cost) + " " + current.toOneLineString().rstrip() + '\n')
    else:
        output.write("no solution" + "\n")

    output.write(str(solutionNode.totalCost) + " " + str(executeTime % 60))

    # Close output file
    output.close()

    # Open search file
    output = open('A2_Output/' + filePrefix + '_search.txt', 'w')

    for nodes in searchPath:
        output.write(
            str(nodes.functionCost) + " " + str(nodes.totalCost) + " " + str(
                nodes.heuristicCost) + " " + nodes.toOneLineString().rstrip() + "\n")

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
def gbfs(node, _goalList1, _goalList2, h_func):
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

        parentNode = _openList.pop(0)
        possibleMoves = findMoves(parentNode, parentNode.stateWhenAtNode, _goalList1, _goalList2)

        # For each of our node, check the closed list to see if it's there. If it's there, we don't want it.
        for newNode in possibleMoves:
            found = next((n for n in _closedList if n.stateWhenAtNode == newNode.stateWhenAtNode), None)
            if found is None:
                # We now check if it's in our open list. If it's not there, add the node and compute its heuristic value
                found = next((n for n in _openList if n.stateWhenAtNode == newNode.stateWhenAtNode), None)
                if found is None:
                    newNode.heuristicCost = h_func(newNode.stateWhenAtNode)
                    #newNode.functionCost = newNode.totalCost + newNode.heuristicCost
                    _openList.append(newNode)

        # Sorting the open list by heuristic of the nodes.
        _openList = sorted(_openList, key=lambda n: n.heuristicCost)

    _searchedNodes = _closedList

    # If we are here, we either have a solution or we failed to find one.
    if _end and not _timeout:
        print("Solution found.")
    elif _timeout:
        print("Timed out. Longer than " + str(TIMEOUT_TIME_IN_SECONDS) + " seconds passed.")
    else:
        print("Failed to find a solution to the puzzle.")

def a_star(node, _goalList1, _goalList2, h_func):
    global _timeout
    global _end
    global _searchedNodes
    global _openList
    global _closedList

    _openList.append(node)

    # For as long as we don't have a solution, pop the first node of the open list.
    i=0
    while not _end and len(_openList) != 0:
        if timeout():
            _timeout = True
            _end = True
            break

        parentNode = _openList.pop(0)
        #print(parentNode.stateWhenAtNode)
        #print(parentNode.totalCost)
        possibleMoves = findMoves(parentNode, parentNode.stateWhenAtNode, _goalList1, _goalList2)

        # For each of our node, check the closed list to see if it's there. If it's there, we don't want it.
        for newNode in possibleMoves:
            found = next((n for n in _closedList if n.stateWhenAtNode == newNode.stateWhenAtNode), None)
            if found is None:
                # We now check if it's in our open list. If it's there, we update the cost if we have a lower total
                # cost. If not, we add it to the open list.
                found = next((n for n in _openList if n.stateWhenAtNode == newNode.stateWhenAtNode), None)
                if found is None:
                    _openList.append(newNode)
                    newNode.heuristicCost = h_func(newNode.stateWhenAtNode)
                    newNode.functionCost = newNode.heuristicCost + newNode.totalCost
                else:
                    if found.functionCost > newNode.functionCost:
                        _openList.remove(found)
                        _openList.append(newNode)
                        newNode.heuristicCost = h_func(newNode.stateWhenAtNode)
                        newNode.functionCost = newNode.heuristicCost + newNode.totalCost

        # Sorting the open list by total cost of the nodes.
        _openList = sorted(_openList, key=lambda n: n.functionCost)
        i+=1

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
    if (nodeState[len(nodeState) - 1][len(nodeState[0]) - 1] == '0'):
        return 0
    else:
        return 1


def manhattanDistance(nodeState):
    _goalList1, _goalList2 = goalList(len(nodeState[0]), len(nodeState))
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


# Heuristic function 2: minimum Diagonal distance (cost of moving horizontally/vertically is 1, diagonal is 3) from passed node state
def diagonalDistance(nodeState, D=1, D2=3):
    _goalList1, _goalList2 = goalList(len(nodeState[0]), len(nodeState))
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


# Heuristic function 1: minimum Hamming distance from passed node
def hammingDistance(nodeState):
    _goalList1, _goalList2 = goalList(len(nodeState[0]), len(nodeState))
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
