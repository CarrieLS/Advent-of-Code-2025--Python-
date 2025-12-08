test_case = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689""".split("\n")

def reformat_input(str_list):
    coord_list = []
    for line in str_list:
        line_split = line.split(',')
        coord_list.append((int(line_split[0]),int(line_split[1]), \
                           int(line_split[2])))
    return coord_list

test_coords = reformat_input(test_case)

#we can use squared dist since we just care about relative dists
def find_squared_distance(coord1, coord2):
    dist = 0
    for x_i, x_j in zip(coord1, coord2):
        dist += (x_i - x_j)**2
    return dist

#brute force all the pairs
#is there a better way?  that's O(N_boxes^2)
def connect_N_closest_count_circuits(boxes, N, circuit_count):
    dists_indices = [] #elements are (sq_dist, (i,j))
    for i, box_i in enumerate(boxes[:-1]):
        for j, box_j in enumerate(boxes[i+1:],start = i+1):
            dists_indices.append((find_squared_distance(box_i,box_j),(i,j)))
    sorted_pairs = sorted(dists_indices, key = lambda d: d[0], reverse = True)
    circuits = [] #circuits are sets
    N_connections = 0
    while N_connections < N:
        N_connections += 1 #assume connection will be made, sub 1 later if not
        pair = sorted_pairs.pop()
        box1 = pair[1][0] #just use index
        box2 = pair[1][1]
        #check if box1 is already in a circuit
        box1_circuit = -1
        box2_circuit = -1
        for i, circuit in enumerate(circuits):
            if box1 in circuit:
                box1_circuit = i
            if box2 in circuit:
                box2_circuit = i
            if box1_circuit != -1 and box2_circuit != -1:
                break #both should only be in max 1 circuit
        #box1 not in a circuit yet
        if box1_circuit == -1:
            if box2_circuit == -1:
                #new circuit
                circuits.append({box1, box2})
            else:
                #add box1 to box2's circuit
                circuits[box2_circuit].add(box1)
        else:
            if box2_circuit == -1:
                #add box2 to box1's circuit
                circuits[box1_circuit].add(box2)
            elif box2_circuit == box1_circuit:
                #no connection is needed, already share a circuit
                pass #N_connections -= 1
            else:
                #merge the two circuits
                circuits[box1_circuit] = \
                    circuits[box1_circuit].union(circuits[box2_circuit])
                del circuits[box2_circuit]
    #now multiply size of 3 largest circuits
    circuit_lengths = [len(c) for c in circuits]
    sorted_lengths = sorted(circuit_lengths, reverse = True)
    retval = 1
    for length in sorted_lengths[:circuit_count]:
        retval *= length
    return retval

assert connect_N_closest_count_circuits(test_coords, 10,3) == 40

puzzle_case = []
with open("../adventFiles/puzzle8.txt") as f:
    for line in f:
        puzzle_case.append(line.strip())

puzzle_coords = reformat_input(puzzle_case)

print(f"Puzzle 8-1 Solution: {connect_N_closest_count_circuits(puzzle_coords,1000,3)}")

#connect all circuits, then multiply the x coords of the final two
#starts the same as other func
def connect_all_circuits(boxes):
    dists_indices = [] #elements are (sq_dist, (i,j))
    for i, box_i in enumerate(boxes[:-1]):
        for j, box_j in enumerate(boxes[i+1:],start = i+1):
            dists_indices.append((find_squared_distance(box_i,box_j),(i,j)))
    sorted_pairs = sorted(dists_indices, key = lambda d: d[0], reverse = True)
    box1 = -1
    box2 = -1
    #indices kept out here so we can check their final vals
    circuits = [] #circuits are sets
    #go until there is a set containing all boxes
    while len(circuits) == 0 or len(circuits[0]) < len(boxes):
        pair = sorted_pairs.pop()
        box1 = pair[1][0] #just use index
        box2 = pair[1][1]
        #check if box1 is already in a circuit
        box1_circuit = -1
        box2_circuit = -1
        for i, circuit in enumerate(circuits):
            if box1 in circuit:
                box1_circuit = i
            if box2 in circuit:
                box2_circuit = i
            if box1_circuit != -1 and box2_circuit != -1:
                break #both should only be in max 1 circuit
        #box1 not in a circuit yet
        if box1_circuit == -1:
            if box2_circuit == -1:
                #new circuit
                circuits.append({box1, box2})
            else:
                #add box1 to box2's circuit
                circuits[box2_circuit].add(box1)
        else:
            if box2_circuit == -1:
                #add box2 to box1's circuit
                circuits[box1_circuit].add(box2)
            elif box2_circuit == box1_circuit:
                #no connection is needed, already share a circuit
                pass #N_connections -= 1
            else:
                #merge the two circuits
                circuits[box1_circuit] = \
                    circuits[box1_circuit].union(circuits[box2_circuit])
                del circuits[box2_circuit]
    return boxes[box1][0]*boxes[box2][0]

assert connect_all_circuits(test_coords) == 25272

print(f"Puzzle 8-2 Solution: {connect_all_circuits(puzzle_coords)}")
