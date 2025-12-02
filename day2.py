# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 12:55:06 2025

@author: Carrie LS
"""

import numpy as np

testIDs = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,\
1698522-1698528,446443-446449,38593856-38593862,565653-565659,\
824824821-824824827,2121212118-2121212124"

puzzleIDs = None
with open("../adventFiles/puzzle2.txt") as f:
    puzzleIDs = f.readline().strip()

#func to check if a single int ID is made up of two repeat numbers
def _IDisTwoRepeats(IDval):
    digits = int(np.log10(IDval)) + 1
    if digits % 2 == 1:
        return False
    else:
        tenFactor = 10**(digits//2)
        return (IDval % tenFactor) == (IDval // tenFactor)

def addInvalidIDs(IDstr):
    IDlist = IDstr.split(",")
    summedInvalid = 0
    for IDrange in IDlist:
        IDends = IDrange.split("-")
        (minID, maxID) = [int(ID) for ID in IDends]
        IDvals = range(minID,maxID+1)
        for IDval in IDvals:
            if _IDisTwoRepeats(IDval):
                summedInvalid += IDval
    return summedInvalid

assert addInvalidIDs(testIDs) == 1227775554

print(f"Puzzle 2-1 solution: {addInvalidIDs(puzzleIDs)}")

#2-2
#now we need to include all repeats, not just two
#can't do this as simply, have to check for possible repeats of any
#digit count which is a factor of total digits and is <= digits/2

#lets try to make the factor finding not toooo slow
#simple check for factors up to sqrt(N)
#A is factor of B if B % A == 0
#add factor pair when found
#cache results so we aren't repeatedly factorizing the same numbers
#cache is a dict of factor sets for each number
#i'll precache 1
cachedFactors = {1 : {1}}

#there are def faster ways to do this
#but this shouldn't be too slow, O(sqrt(N)) for fixed size ints i think
#also we are just factoring digit count which doesn't go too high in this problem
#returns factors as a list
def _findFactors(wholeNumber):
    if wholeNumber <= 0 or type(wholeNumber) is not int:
        raise ValueError("Number to factorize is not whole!")
    cachedVal = cachedFactors.get(wholeNumber)
    if cachedVal:
        return cachedVal
    else:
        cachedFactors[wholeNumber] = set()
        for n in range(1,int(np.sqrt(wholeNumber))+1):
            if wholeNumber % n == 0:
                cachedFactors[wholeNumber].add(n)
                cachedFactors[wholeNumber].add(wholeNumber//n)
    return cachedFactors[wholeNumber]

#func to check if a single int ID is made up of repeated substrings
#lets do it as a string now
def _IDisRepeats(IDval):
    stringID = str(IDval)
    digitCount = len(stringID)
    #find all factors
    factors = _findFactors(digitCount)
    for factor in factors:
        if factor == digitCount:
            continue #ignore this case, since this is all the digits
        subStringCount = digitCount//factor #how many repeats would there be?
        firstSubString = stringID[:factor]
        repeat = True
        for i in range(1,subStringCount):
            if stringID[i*factor:(i+1)*factor] != firstSubString:
                repeat = False
                break
        if repeat:
            return True
    return False

def addAllInvalidIDs(IDstr):
    IDlist = IDstr.split(",")
    summedInvalid = 0
    for IDrange in IDlist:
        IDends = IDrange.split("-")
        (minID, maxID) = [int(ID) for ID in IDends]
        IDvals = range(minID,maxID+1)
        for IDval in IDvals:
            if _IDisRepeats(IDval):
                summedInvalid += IDval
    return summedInvalid

assert addAllInvalidIDs(testIDs) == 4174379265

print(f"Puzzle 2-2 solution: {addAllInvalidIDs(puzzleIDs)}")