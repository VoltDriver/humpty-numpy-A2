from codebase import *

# --------------- Program ---------------

# Load puzzles
data = load_input("A2_Input/samplePuzzles.txt")
for line in data:
    for element in line:
        print(element)

counter = 0
# Finding Solutions
for currentPuzzle in data:

    _goalList1, _goalList2 = goalList(len(currentPuzzle[0]), len(currentPuzzle))

    # initializing the start of the algorithm
    startNode = Node(0, 0, 0, 0, currentPuzzle, None, -1)
    startTime = startTimer()  # Starting the stopwatch.

    possibleMoves = None

    # Running the algorithm
    findSolution(startNode, _goalList1, _goalList2)

    # Stopping the stopwatch
    finalTime = time.time()

    from codebase import _goalNode, _searchedNodes

    finalNode = _goalNode
    print("Total cost is " + str(finalNode.totalCost) + "\n")

    nodeStack = []

    # traversing the nodes, to print them  to console.
    if finalNode.parent is not None:
        curNode = finalNode
        while curNode.parent is not None:
            nodeStack.append(curNode.toString())
            curNode = curNode.parent
        while nodeStack:
            print("-------")
            print(nodeStack.pop())

    print("Total time taken: " + timeFormat(finalTime - startTime))

    # Creating the output files
    createOutputFile(str(counter) + "_ucs", currentPuzzle, finalNode, finalTime - startTime, _searchedNodes)

    # Resetting global variables, to prepare for the next puzzle.
    resetGlobals()

    counter += 1
