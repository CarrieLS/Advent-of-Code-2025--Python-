test_case = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.""".split("\n")

def countAccessibleRolls(layout):
    height = len(layout)
    width = len(layout[0]) #this assumes width is constant, would break if not
    count = 0
    for i in range(height):
        for j in range(width):
            if layout[i][j] == '.':
                continue
            adjCount = 0
            for adj_i in range(max(0,i-1),min(height,i+2)):
                for adj_j in range(max(0,j-1),min(height,j+2)):
                    if adj_i == i and adj_j == j:
                        continue
                    if layout[adj_i][adj_j] == '@':
                        adjCount += 1
            if adjCount < 4:
                count += 1
    return count

assert countAccessibleRolls(test_case) == 13

puzzle_case = []
with open("../adventFiles/puzzle4.txt",'r') as f:
    for line in f:
        puzzle_case.append(line.strip())

print(f"Puzzle 4-1 Solution: {countAccessibleRolls(puzzle_case)}")

#true for rolls, false for none
def layoutToBools(layout):
    layoutBools = []
    for line in layout:
        lineBools = []
        for char in line:
            lineBools.append(char == "@")
        layoutBools.append(lineBools)
    return layoutBools

#this will be easier if we make it a 2d list of bools, cuz strings are immutable
def countAccessibleRollsRepeats(layout):
    lbools = layoutToBools(layout)
    height = len(lbools)
    width = len(lbools[0]) #this assumes width is constant, would break if not
    count = 0
    remCount = 1 #tracks removed in one loop, set to 1 for loop to start
    while remCount > 0:
        remCount = 0
        for i in range(height):
            for j in range(width):
                if not lbools[i][j]:
                    continue
                adjCount = 0
                for adj_i in range(max(0,i-1),min(height,i+2)):
                    for adj_j in range(max(0,j-1),min(height,j+2)):
                        if adj_i == i and adj_j == j:
                            continue
                        if lbools[adj_i][adj_j]:
                            adjCount += 1
                if adjCount < 4:
                    remCount += 1
                    lbools[i][j] = False #remove stack
        count += remCount
    return count

assert countAccessibleRollsRepeats(test_case) == 43

print(f"Puzzle 4-2 Solution: {countAccessibleRollsRepeats(puzzle_case)}")