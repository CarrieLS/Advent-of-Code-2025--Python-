test_case = """3-5
10-14
16-20
12-18

1
5
8
11
17
32""".split("\n")

#check each range for each value
def countFreshIngredients(ingredients):
    break_i = ingredients.index('')
    freshCount = 0
    for val_str in ingredients[break_i+1:]:
        val = int(val_str)
        for range_str in ingredients[:break_i]:
            ranges = range_str.split('-')
            if val >= int(ranges[0]) and val <= int(ranges[1]):
                freshCount+=1
                break
    return freshCount

assert countFreshIngredients(test_case) == 3

puzzle_case = []
with open("../adventFiles/puzzle5.txt") as f:
    for line in f:
        puzzle_case.append(line.strip())

print(f"Puzzle 5-1 Solution: {countFreshIngredients(puzzle_case)}")

#returns index right above, and also True/False if val is in lst
#if value is a max, return one higher on match (important for collapsing)
def _binarySearchHelper(val,lst,isMax):
    min_i = 0
    max_i = len(lst)
    while max_i > min_i:
        i = (max_i + min_i)//2
        if val == lst[i]:
            #found
            if isMax:
                return i+1
            return i
        elif val > lst[i]:
            min_i = i+1
        else:
            max_i = i
    return min_i

#read in ranges
#track the boundaries
#insert via binary process, keep sorted
#collapse all values between inserts (go down to even index and up to odd)
#for example, with test case:
    #3-5 -> [3,5]
    #10-14 -> [3,5,10,14]
    #16-20 -> [3,5,10,14,16,20]
    #12-18 -> [3,5,10,12*,14,16,18*,20] -> [3,5,10,20]
def countAllFresh(ranges):
    boundaries = []
    for rpair in ranges:
        print(rpair)
        (min_str,max_str) = rpair.split("-")
        minval = int(min_str)
        maxval = int(max_str)
        if not boundaries:
            boundaries.append(minval)
            boundaries.append(maxval)
        else:
            minval_iabove = _binarySearchHelper(minval,boundaries,False)
            maxval_iabove = _binarySearchHelper(maxval,boundaries,True)
            #insert min and max
            boundaries.insert(minval_iabove,minval)
            boundaries.insert(maxval_iabove+1,maxval)
            #find indices to collapse between
            collapse_mini = minval_iabove
            if collapse_mini % 2 != 0: #middle of range
                collapse_mini -= 1
            collapse_maxi = maxval_iabove+1
            if collapse_maxi % 2 == 0: #middle of range
                collapse_maxi += 1
            #remove between these indices, not inclusive
            del boundaries[collapse_mini+1:collapse_maxi]
        print(boundaries)
        print(len(boundaries))
        print('\n')
    #now try counting all values
    #ranges shouldn't overlap now hopefully
    count = 0
    for i in range(len(boundaries)//2):
        count += 1 + boundaries[2*i+1]-boundaries[2*i]
    return count

test_ranges = test_case[:4]
assert countAllFresh(test_ranges) == 14
            
puzzle_ranges = []
for line in puzzle_case:
    if line == '':
        break
    puzzle_ranges.append(line)

print(f"Puzzle 5-2 Solution: {countAllFresh(puzzle_ranges[:])}")

            