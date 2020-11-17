from codebase import *

num_rand_puzzles = 50
input_filename = 'A2_Input/randomPuzzles.txt'

# Generate 50 puzzles, and put them in a text file
random_puzzle_input = open(input_filename, 'w')
for i in range(len(range(num_rand_puzzles))):
    random_puzzle = puzzlegenerator(4, 2)
    for row in random_puzzle:
        for j in row:
            random_puzzle_input.write(str(j) + ' ')
    if i < num_rand_puzzles - 1:
        random_puzzle_input.write('\n')
random_puzzle_input.close()

# Read puzzle from generated file
data = load_input(input_filename)

# Define some DS to store used solvers (key) and heuristics (value)
solvers = {
    'UCS' : (findSolution, None),
    'GBFS Hamming Distance' : (gbfs, hammingDistance),
    'GBFS Diagonal Distance' : (gbfs, diagonalDistance),
    'A* Hamming Distance' : (a_star, hammingDistance),
    'A* Diagonal Distance' : (a_star, diagonalDistance)
}

output = open('A2_Output/RandomPuzzleStats.txt', 'w')

# Loop over solvers, and within loop over the puzzles
for solver in solvers:
    # Initialize statistics
    total_len_solution = 0
    total_len_search = 0
    total_no_solution = 0
    total_cost = 0
    total_execution_time = 0
    
    # Solve each puzzle
    for puzzle in data:
        
        startNode = Node(0, 0, 0, 0, puzzle, None, -1)
        if (solvers[solver][1] is not None):
            startNode.heuristicCost = solvers[solver][1](puzzle)
        _goalList1, _goalList2 = goalList(len(puzzle[0]), len(puzzle))
        startTime = startTimer()  # Starting the stopwatch.

        # Running the algorithm
        if (solvers[solver][1] is None):
            solvers[solver][0](startNode, _goalList1, _goalList2)
        else:
            solvers[solver][0](startNode, _goalList1, _goalList2, solvers[solver][1])
            
        # Stopping the stopwatch
        finalTime = time.time()

        from codebase import _goalNode, _searchedNodes
        finalNode = _goalNode

        # Update statistics
        total_len_search += len(_searchedNodes)
        
        nodeStack = []
        if finalNode.parent is not None:
            curNode = finalNode
            while curNode.parent is not None:
                nodeStack.append(curNode.toString())
                curNode = curNode.parent
            total_len_solution += len(nodeStack) + 1 # Initial state not included in nodeStack
            total_cost += finalNode.totalCost
        else:
            total_no_solution += 1
        
        total_execution_time += finalTime - startTime
        
        # Reset variables in codebase.py
        resetGlobals()
        
    # Calculate averages 
    avg_len_solution = 0
    avg_cost = 0
    avg_len_search = total_len_search / num_rand_puzzles
    avg_execution_time = total_execution_time / num_rand_puzzles
    if (num_rand_puzzles - total_no_solution > 0):
        avg_len_solution = total_len_solution / (num_rand_puzzles - total_no_solution)
        avg_cost = total_cost / (num_rand_puzzles - total_no_solution)

    # Write in an output file the stats so they can be noted in slides
    output.write(solver + '\n')
    output.write('Total solution path length: ' + str(total_len_solution) + '\n')
    output.write('Average solution path length: ' + str(avg_len_solution) + '\n')
    output.write('Total search path length: ' + str(total_len_search) + '\n')
    output.write('Average search path length: ' + str(avg_len_search) + '\n')
    output.write('Total no solution: ' + str(total_no_solution) + '\n')
    output.write('Total total cost: ' + str(total_cost) + '\n')
    output.write('Average cost: ' + str(avg_cost) + '\n')
    output.write('Total execution time: ' + str(total_execution_time) + ' sec.\n')
    output.write('Average execution time: ' + str(avg_execution_time) + ' sec.\n')
    output.write('--------------------------------\n\n')

output.close()