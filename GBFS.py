from codebase import *

# ------------------------------
# Execute Greedy/Best-First Search
# Load puzzles
data = load_input("A2_Input/samplePuzzles.txt")

gbfs_h = {
    manhattanDistance : "_gbfs-h1",
    diagonalDistance : "_gbfs-h2"
}

for heuristic in gbfs_h:

    counter = 0

    # Finding Solutions
    for currentPuzzle in data:

        # initializing the start of the algorithm
        startNode = Node(0, heuristic(currentPuzzle), 0, 0, currentPuzzle, None, -1)
        startTime = startTimer()  # Starting the stopwatch.

        # Running the algorithm
        #findSolution(startNode)
        gbfs(startNode, heuristic)

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
        createOutputFile(str(counter) + gbfs_h[heuristic], currentPuzzle, finalNode, finalTime - startTime, _searchedNodes)

        # Resetting global variables, to prepare for the next puzzle.
        resetGlobals()

        counter += 1


