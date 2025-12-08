test_case = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """.split('\n')

#convert 1d list of lines into 2d list of numbers and symbols
#transpose it so each line is a sequence to operate on
def processInput(inp):
    out_list = []
    for line in inp:
        out_list.append(line.split())
    transposed = [list(seq) for seq in zip(*out_list)]
    return transposed

test_case_ref = processInput(test_case)

def addAndMultCeph(data):
    totVal = 0
    for line in data:
        if line[-1] == '+': #addition
            for val in line[:-1]:
                totVal += int(val)
        else: #multiplication
            subTot = int(line[0])
            for val in line[1:-1]:
                subTot *= int(val)
            totVal += subTot
    return totVal

assert addAndMultCeph(test_case_ref) == 4277556

puzzle_case = []
with open("../adventFiles/puzzle6.txt") as f:
    for line in f:
        puzzle_case.append(line.strip('\n'))

puzzle_case_ref = processInput(puzzle_case)

print(f"Puzzle 6-1 Solution: {addAndMultCeph(puzzle_case_ref)}")

#this one takes just a list of each line
#and uses the accurate cephalapod format
def addAndMultRevamped(data):
    operator_indices = []
    #find indices of each operator
    for i,char in enumerate(data[-1]):
        if char != ' ':
            operator_indices.append(i)
    grandTot = 0
    dat_width = len(data[0])
    dat_height = len(data)
    #iterate over operators
    for op_i, dat_i in enumerate(operator_indices):
        op_char = data[-1][dat_i]
        max_j = dat_width #max index before next op, not counting the spaces
        if op_i < len(operator_indices) - 1:
            max_j = operator_indices[op_i+1]-1
        if op_char == "+":
            for j in range(dat_i,max_j): #technically this should be reversed but it doesn't matter for +/*
                num = 0
                for k in range(dat_height-1):
                    char = data[k][j]
                    if char != ' ':
                        num = num*10 + int(char)
                grandTot+=num
        else: #*
            subTot = -1
            for j in range(dat_i,max_j): #technically this should be reversed but it doesn't matter for +/*
                num = 0
                for k in range(dat_height-1):
                    char = data[k][j]
                    if char != ' ':
                        num = num*10 + int(char)
                if subTot < 0:
                    subTot = num
                else:
                    subTot *= num
            grandTot += subTot
    return grandTot

assert addAndMultRevamped(test_case) == 3263827

print(f"Puzzle 6-2 Solution: {addAndMultRevamped(puzzle_case)}")