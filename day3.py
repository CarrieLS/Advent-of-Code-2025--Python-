#to find first digit:
    #read thru from left to right, from [0] to [-2]
    #store current highest digit and pos of it 
    #if you find a 9, just use that immediately
    #otherwise, use highest digit found (and first position if there are multiple)
#to find second digit:
    #read thru remaining digits after first one
    #save highest
    #pick it
    #stop early if you find 9
#func takes line of values as a string
def maxLineJoltage(battLine):
    firstDigit = 0
    first_i = -1
    for i, battery in enumerate(battLine[:-1]):
        if int(battery) > firstDigit:
            firstDigit = int(battery)
            first_i = i
            if firstDigit == 9:
                break #stop early, no higher digits possible
    secondDigit = 0
    for battery in battLine[first_i+1:]:
        if int(battery) > secondDigit:
            secondDigit = int(battery)
            if secondDigit == 9:
                break
    return firstDigit*10 + secondDigit

#takes list of battlines
def addAllJoltages(batteries):
    total = 0
    for battLine in batteries:
        total += maxLineJoltage(battLine)
    return total

#test case
test_batteries = ['987654321111111',
'811111111111119',
'234234234234278',
'818181911112111']

assert addAllJoltages(test_batteries) == 357

puzzle_batteries = []
with open("../adventFiles/puzzle3.txt", "r") as f:
    for line in f:
        puzzle_batteries.append(line.strip())

print(f"Puzzle 3-1 Solution: {addAllJoltages(puzzle_batteries)}")

#now for arbitrary number of batteries
def maxLineJoltageN(battLine,N):
    if N > len(battLine):
        raise ValueError("Tried to check more batteries than exist!")
    digits = [0]*N
    i_tracker = -1 #tracks index of previously found high val
    B = len(battLine)
    for n in range(N):
        for i in range(i_tracker+1,1+n+B-N):
            battVal = int(battLine[i])
            if battVal > digits[n]:
                digits[n] = battVal
                i_tracker = i
                if battVal == 9:
                    break
    retVal = 0
    for i, digit in enumerate(digits):
        retVal += digit*10**(N-i-1)
    return retVal

def addAllJoltagesTwelve(batteries):
    total = 0
    for battLine in batteries:
        total += maxLineJoltageN(battLine,12)
    return total

assert addAllJoltagesTwelve(test_batteries) == 3121910778619

print(f"Puzzle 3-2 Solution: {addAllJoltagesTwelve(puzzle_batteries)}")