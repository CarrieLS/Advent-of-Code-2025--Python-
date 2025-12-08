test_case = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............""".split('\n')

def toCharList(strList):
    charList = []
    for line in strList:
        charList.append(list(line))
    return charList

test_case = toCharList(test_case)

#from top to bottom
#changes input list and returns splitCount
def applyBeams(layout):
    splitCount = 0
    for y,line in enumerate(layout[:-1]): #skip process for final line
        for x,char in enumerate(line):
            if char == 'S' or char == '|':
                targ_char = layout[y+1][x]
                if targ_char == '.':
                    layout[y+1][x] = '|' #ray goes down
                elif targ_char == '^': #split
                    if x > 0:
                        layout[y+1][x-1] = '|'
                    if x < len(line) - 1:
                        layout[y+1][x+1] = '|'
                    splitCount += 1
    return splitCount

assert applyBeams(test_case[:]) == 21

puzzle_case = []
with open("../adventFiles/puzzle7.txt") as f:
    for line in f:
        puzzle_case.append(list(line.strip()))

print(f"Puzzle 7-1 Solution: {applyBeams(puzzle_case[:])}")

#recursive helper
#give coords of beam
#store cached subpaths because you can take alternate ones to the same place
#dict of (y,x) and subpaths
cachedSubPaths = {}

def _countSubPaths(layout,y,x):
    #check cache
    if (y,x) in cachedSubPaths:
        return cachedSubPaths[(y,x)]
    if x < 0 or x >= len(layout[0]): #out of bounds
        return 0
    curr_y = y+1
    while curr_y < len(layout):
        if layout[curr_y][x] == '^': #split
            count = _countSubPaths(layout,curr_y,x-1) + \
                _countSubPaths(layout,curr_y,x+1) 
            for cache_y in range(y,curr_y):
                cachedSubPaths[(cache_y,x)] = count
            return count
        curr_y += 1
    #no more splits
    cachedSubPaths[(y,x)] = 1
    return 1

#count all possible paths
def countPossiblePaths(layout):
    #find S
    for x, char in enumerate(layout[0]):
        if char == 'S':
            return _countSubPaths(layout,0,x)

assert countPossiblePaths(test_case) == 40
print(f"Puzzle 7-2 Solution: {countPossiblePaths(puzzle_case)}")