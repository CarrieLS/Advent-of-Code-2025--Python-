test_case = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3""".split('\n')

#rectangle size is delta x * delta y
#brute force would be check rectangle size of every possible pair
#O(N^2)
#is there a better way?

def rectangle_size(pos1, pos2):
    pos1_split = pos1.split(',')
    pos2_split = pos2.split(',')
    return (1+abs(int(pos1_split[0])-int(pos2_split[0])))*\
               (1+abs(int(pos1_split[1])-int(pos2_split[1])))

def rectangle_size_ints(pos1, pos2):
    return (1+abs(pos1[0]-pos2[0]))*(1+abs(pos1[1]-pos2[1]))

def find_largest_area_brute_force(positions):
    sizes = [] #each element is (size, (i, j))
    for i, pos1 in enumerate(positions[:-1]):
        for j, pos2 in enumerate(positions[i+1:],start=i+1):
            sizes.append((rectangle_size(pos1,pos2),(i,j)))
    sorted_pairs = sorted(sizes,key=lambda s: s[0])
    return sorted_pairs[-1][0]

assert find_largest_area_brute_force(test_case) == 50

puzzle_case = []
with open("../adventFiles/puzzle9.txt") as f:
    for line in f:
        puzzle_case.append(line.strip())

print(f"Puzzle 9-1 Solution: {find_largest_area_brute_force(puzzle_case)}")

#what determines if a tile is inside the bounds?
#trace a path around the outside
#each edge has an interior and exterior side
#a tile is inside the bounds (green) if the nearest edge in each direction
#has the interior side facing it
#what about a rectangle?
#a rectangle is inside the bounds if the edges of the rectangle don't cross any
#edges of the bounds
#that's relatively easy to check I think

#when does an orthogonal line intersect w/ a rectangle?
#if the line goes along the x direction, then it happens when:
    #x is inside the rectangle (not counting the edges)
    #and:
        #y1 or y2 are inside the rectangle (not counting edges)
        #or y1 and y2 are on opposite sides of the rectangle (again, no edges)
#same for y direction but with x/y swapped

#takes lists/tuples of int lists/tuples for easier math
def does_rectangle_intersect_ortho_line(rectangle_corners,line_ends):
    line_axis = -1 #0 for x, 1 for y
    if line_ends[0][0] == line_ends[1][0]:
        line_axis = 0
    elif line_ends[0][1] == line_ends[1][1]:
        line_axis = 1
    else:
        raise ValueError("Line is not orthogonal!")
    rectangle_mins = (min(rectangle_corners[0][0],rectangle_corners[1][0]),
                      min(rectangle_corners[0][1],rectangle_corners[1][1]))
    rectangle_maxs = (max(rectangle_corners[0][0],rectangle_corners[1][0]),
                      max(rectangle_corners[0][1],rectangle_corners[1][1]))
    #constant axis not inside rectangle
    if line_ends[0][line_axis] <= rectangle_mins[line_axis] or \
        line_ends[0][line_axis] >= rectangle_maxs[line_axis]:
            return False
    line_min_coord = min(line_ends[0][1-line_axis],line_ends[1][1-line_axis])
    line_max_coord = max(line_ends[0][1-line_axis],line_ends[1][1-line_axis])
    #is either point inside the rectangle?
    if (line_min_coord > rectangle_mins[1-line_axis] and \
        line_min_coord < rectangle_maxs[1-line_axis]) or \
        (line_max_coord > rectangle_mins[1-line_axis] and \
         line_max_coord < rectangle_maxs[1-line_axis]):
            return True
    #are the points on opposite sides of the rectangle? we know they aren't in
    if (line_min_coord <= rectangle_mins[1-line_axis] and \
        line_max_coord >= rectangle_maxs[1-line_axis]):
        return True
    return False

#convert position list into tuples of ints for easier use
def positions_to_ints(pos_str):
    intpos = []
    for line in pos_str:
        split_pos = line.split(',')
        intpos.append((int(split_pos[0]),int(split_pos[1])))
    return intpos

#test - are any lines adjacent?  this could cause issues
def are_any_lines_adjacent(lines):
    for i, line1 in enumerate(lines[:-1]):
        for j, line2 in enumerate(lines[i+1:],start=i+1):
            line1_axis = int(line1[0][1]==line1[1][1]) #0 for x, 1 for y
            line2_axis = int(line2[0][1]==line2[1][1])
            if line1_axis != line2_axis:
                continue
            if abs(line1[0][line1_axis]-line2[0][line2_axis]) != 1:
                continue
            line1_bounds = (min(line1[0][1-line1_axis],line1[1][1-line1_axis]),
                            max(line1[0][1-line1_axis],line1[1][1-line1_axis]))
            line2_bounds = (min(line2[0][1-line2_axis],line2[1][1-line2_axis]),
                            max(line2[0][1-line2_axis],line2[1][1-line2_axis]))
            for i in (0,1):
                if line1_bounds[i] >= line2_bounds[0] and \
                    line1_bounds[i] <= line2_bounds[1]:
                        return True
            if line1_bounds[0] < line2_bounds[0] and \
                line1_bounds[1] > line2_bounds[1]:
                    return True
    return False
#checked for test and puzzle case, no in both cases

def find_largest_area_in_bounds(positions):
    intpos = positions_to_ints(positions)
    #construct all lines for bounds
    edges = []
    for i, pos in enumerate(intpos):
        nextpos = intpos[(i+1)%len(intpos)]
        edges.append((pos,nextpos))
    #now record sizes of rectangles which are in bounds
    sizes = [] #element: (size,(i,j))
    for i, pos1 in enumerate(intpos[:-1]):
        for j, pos2 in enumerate(intpos[i+1:],start=i+1):
            for line in edges:
                if does_rectangle_intersect_ortho_line((pos1,pos2), line):
                    break
            else: #if no intersection was found
                sizes.append((rectangle_size_ints(pos1,pos2),(i,j)))
    #sort and return largest
    sorted_pairs = sorted(sizes,key=lambda s: s[0])
    return sorted_pairs[-1]

assert find_largest_area_in_bounds(test_case)[0] == 24

print(f"Puzzle 9-2 Solution: {find_largest_area_in_bounds(puzzle_case)}")