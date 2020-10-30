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


# Load puzzles
data = load_input("A2_Input/samplePuzzles.txt")
for line in data:
    for element in line:
        print(element)
