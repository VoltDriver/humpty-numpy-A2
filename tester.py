import codebase

puzzle = [['1','4','3','9','6'],['7','0','5','2','8']]
data = codebase.load_input("A2_Input/samplePuzzles.txt")

startNode = codebase.Node(0, codebase.diagonalDistance(data[2]), 0, 0, data[2], None, -1)
_goalList1, _goalList2 = codebase.goalList(len(data[2][0]), len(data[2]))
possibleMoves = codebase.findMoves(startNode, data[2], _goalList1, _goalList2)

print(startNode.stateWhenAtNode)
print()
for i in possibleMoves:
    print(i.stateWhenAtNode)
    print(i.initialized)
