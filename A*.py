from codebase import *

# ------------------------------
# Execute Greedy/Best-First Search
# Load puzzles
data = load_input("A2_Input/samplePuzzles.txt")
#puzzle = [['7','4','3','9','6', '11'],['1','0','5','2','8', '10']]
puzzle = [['1','3','8'],['2','5','0'],['6','4','7']]
#puzzle = [['5','6','7','8', '12'],['1','2','3','4', '14'],['9','10','11','0', '13']]

# Declare a dictionary of heuristic functions and their string component for output files
a_star_h = {
    hammingDistance : "a_star-h1", # Hamming Distance
    diagonalDistance : "a_star-h2", # Diagonal distance (D=1, D2=3)
    manhattanDistance : "a_star-h3" #manhattan distance
}

# Loop through heuristic functions
for heuristic in a_star_h:

    counter = 0

    # Finding Solutions
    for currentPuzzle in data:
    #print(a_star_h[heuristic])
    #if (a_star_h[heuristic] == "a_star-h1"):
    # initializing the start of the algorithm
        startNode = Node(0, heuristic(currentPuzzle), 0, 0, currentPuzzle, None, -1)
        _goalList1, _goalList2 = goalList(len(currentPuzzle[0]), len(currentPuzzle))
        startTime = startTimer()  # Starting the stopwatch.

        # Running the algorithm
        a_star(startNode, _goalList1, _goalList2, heuristic)

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
        createOutputFile(str(counter) + a_star_h[heuristic], currentPuzzle, finalNode, finalTime - startTime, _searchedNodes)

        # Resetting global variables, to prepare for the next puzzle.
        resetGlobals()

        counter += 1