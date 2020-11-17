from codebase import *

# ------------------------------
# Execute Greedy/Best-First Search
# Load puzzles
data = load_input("A2_Input/samplePuzzles.txt")

# Declare a dictionary of heuristic functions and their string component for output files
gbfs_h = {
    hammingDistance : "_gbfs-h1", # Hamming Distance
    diagonalDistance : "_gbfs-h2", # Diagonal distance (D=1, D2=3)
}

# Loop through heuristic functions
for heuristic in gbfs_h:

    counter = 0

    # Finding Solutions
    for currentPuzzle in data:

        # initializing the start of the algorithm
        startNode = Node(0, heuristic(currentPuzzle), 0, 0, currentPuzzle, None, -1)
        _goalList1, _goalList2 = goalList(len(currentPuzzle[0]), len(currentPuzzle))
        startTime = startTimer()  # Starting the stopwatch.

        # Running the algorithm
        #findSolution(startNode)
        gbfs(startNode, _goalList1, _goalList2, heuristic)
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
            #while nodeStack:
            #    print("-------")
            #    print(nodeStack.pop())

        #print("Total time taken: " + timeFormat(finalTime - startTime))
        print("Total time taken: " + str(finalTime - startTime))

        # Creating the output files
        createOutputFile(str(counter) + gbfs_h[heuristic], currentPuzzle, finalNode, finalTime - startTime, _searchedNodes)

        # Resetting global variables, to prepare for the next puzzle.
        resetGlobals()

        counter += 1


