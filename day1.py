# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 11:10:48 2025

@author: Carrie LS
"""

#puzzle 1-1
#rotate dial, count 0s
#func takes rotations as an array of strings

#test from puzzle page
testRots = ['L68', 'L30', 'R48', 'L5', 'R60', 'L55', 'L1', 'L99', 'R14', 'L82']

def safeCountZeros(rotations):
    dialVal = 50
    zeroCount = 0
    for rotString in rotations:
        rotDir = rotString[0]
        rotCount = rotString[1:]
        if rotDir == "L":
            dialVal = (dialVal - int(rotCount)) % 100
        else:
            dialVal = (dialVal + int(rotCount)) % 100
        if dialVal == 0:
            zeroCount += 1
    return zeroCount

assert safeCountZeros(testRots) == 3 #test case

puzzleRots = []
with open('../adventFiles/puzzle1.txt', 'r') as f:
    for rot in f:
        puzzleRots.append(rot.strip())

print(f"Puzzle 1-1 solution: {safeCountZeros(puzzleRots)}")

#puzzle 1-2
#rotate dial, count EVERY pass of 0
#func works the same way otherwise

def safeCountAllZeros(rotations):
    dialVal = 50
    zeroCount = 0
    for rotString in rotations:
        rotDir = rotString[0]
        rotCount = rotString[1:]
        preModDialVal = dialVal
        if rotDir == "L":
            preModDialVal -= int(rotCount)
            #if dialVal was already 0, don't count unless preMod <= -100
            if dialVal == 0:
                zeroCount += (-preModDialVal)//100 #count zero passes
            else:
                zeroCount += (100-preModDialVal)//100 #count zero passes
        else:
            preModDialVal += int(rotCount)
            zeroCount += preModDialVal//100 #count zero passes
        dialVal = preModDialVal % 100
    return zeroCount

assert safeCountAllZeros(testRots) == 6

print(f"Puzzle 1-2 solution: {safeCountAllZeros(puzzleRots)}")
