from codebase import *
from codebase import _startTime

# ------------------------------
# Execute Greedy/Best-First Search
# Load puzzles
data = load_input("A2_Input/samplePuzzles.txt")

# Finding Solution
currentPuzzle = data[0]
startNode = Node(diagonalDistance(currentPuzzle), 0, 0, currentPuzzle, None)
print(startNode.toString())
_startTime = time.time()  # Starting the stopwatch.
#findSolution(startNode)
#gbfs(startNode, h0)
#gbfs(startNode, manhattanDistance)
gbfs(startNode, diagonalDistance)

finalTime = time.time()

from codebase import _goalNode, _closedList

finalNode = _goalNode
print("Total cost is " + str(finalNode.totalCost) + "\n")
print(len(_closedList))

nodeStack = []

if finalNode.parent is not None:
    curNode = finalNode
    while curNode.parent is not None:
        #nodeStack.append(curNode.toString())
        nodeStack.append(curNode)
        curNode = curNode.parent
    while nodeStack:
        print("-------")
        #print(nodeStack.pop())
        node = nodeStack.pop()
        print('heuristic = ' + str(node.heuristicCost))
        print(node.toString())

print("Total time taken: " + timeFormat(finalTime - _startTime))

