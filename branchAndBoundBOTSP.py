# Branch and Bound algorithm for solving Traveling Salesman Problem
import math
import time as tm
maxsize = float('inf')
  
# Function to copy temporary solution
# to the final solution
def copyToFinal(curr_path):
    final_path[:N + 1] = curr_path[:]
    final_path[N] = curr_path[0]
  
# Function to find the minimum edge cost 
# having an end at the vertex i
def firstMin(adj, i):
    min = maxsize
    for k in range(N):
        if adj[i][k] < min and i != k:
            min = adj[i][k]
    return min
  
# function to find the second minimum edge 
# cost having an end at the vertex i
def secondMin(adj, i):
    first, second = maxsize, maxsize
    for j in range(N):
        if i == j:
            continue
        if adj[i][j] <= first:
            second = first
            first = adj[i][j]
        elif(adj[i][j] <= second and 
             adj[i][j] != first):
            second = adj[i][j]
    return second
  
# function that takes as arguments:
# curr_bound -> lower bound of the root node
# curr_weight-> stores the weight of the path so far
# level-> current level while moving
# in the search space tree
# curr_path[] -> where the solution is being stored
# which would later be copied to final_path[]
def TSPRec(adj, curr_bound, curr_weight, 
              level, curr_path, visited):
    global final_res
      
    # base case is when we have reached level N 
    # which means we have covered all the nodes once
    if level == N:
          
        # check if there is an edge from
        # last vertex in path back to the first vertex
        if adj[curr_path[level - 1]][curr_path[0]] != 0:
              
            # curr_res has the total weight
            # of the solution we got
            curr_res = curr_weight + adj[curr_path[level - 1]]\
                                        [curr_path[0]]
            if curr_res < final_res:
                copyToFinal(curr_path)
                final_res = curr_res
        return
  
    # for any other level iterate for all vertices
    # to build the search space tree recursively
    for i in range(N):
          
        # Consider next vertex if it is not same 
        # (diagonal entry in adjacency matrix and 
        #  not visited already)
        if (adj[curr_path[level-1]][i] != 0 and
                            visited[i] == False):
            temp = curr_bound
            curr_weight += adj[curr_path[level - 1]][i]
  
            # different computation of curr_bound 
            # for level 2 from the other levels
            if level == 1:
                curr_bound -= ((firstMin(adj, curr_path[level - 1]) + 
                                firstMin(adj, i)) / 2)
            else:
                curr_bound -= ((secondMin(adj, curr_path[level - 1]) +
                                 firstMin(adj, i)) / 2)
  
            # curr_bound + curr_weight is the actual lower bound 
            # for the node that we have arrived on.
            # If current lower bound < final_res, 
            # we need to explore the node further
            if curr_bound + curr_weight < final_res:
                curr_path[level] = i
                visited[i] = True
                  
                # call TSPRec for the next level
                TSPRec(adj, curr_bound, curr_weight, 
                       level + 1, curr_path, visited)
  
            # Else we have to prune the node by resetting 
            # all changes to curr_weight and curr_bound
            curr_weight -= adj[curr_path[level - 1]][i]
            curr_bound = temp
  
            # Also reset the visited array
            visited = [False] * len(visited)
            for j in range(level):
                if curr_path[j] != -1:
                    visited[curr_path[j]] = True
  
# This function sets up final_path
def TSP(adj):
      
    # Calculate initial lower bound for the root node 
    # using the formula 1/2 * (sum of first min + 
    # second min) for all edges. Also initialize the 
    # curr_path and visited array
    curr_bound = 0
    curr_path = [-1] * (N + 1)
    visited = [False] * N
  
    # Compute initial bound
    for i in range(N):
        curr_bound += (firstMin(adj, i) + 
                       secondMin(adj, i))
  
    # Rounding off the lower bound to an integer
    curr_bound = math.ceil(curr_bound / 2)
  
    # We start at vertex 1 so the first vertex 
    # in curr_path[] is 0
    visited[0] = True
    curr_path[0] = 0
  
    # Call to TSPRec for curr_weight 
    # equal to 0 and level 1
    TSPRec(adj, curr_bound, 0, 1, curr_path, visited)

def biggestValue(adj):
    did = 0
    for i in range(len(adj)):
        for j in range(len(adj)):
            if adj[i][j] > did:
                did = adj[i][j]
    return did

def newValues(adj, maxVal):
    adj_new = []
    length = len(adj)
    for i in range(length):
        adj_t = []
        for j in range(length):
            adj_t.append(adj[i][j]/maxVal)
        adj_new.append(adj_t)
    return adj_new

def normalizedValues(adj_fuel, adj_time):
    max_fuel = biggestValue(adj_fuel)
    max_time = biggestValue(adj_time)
    length = len(adj_fuel)
    adj_f = newValues(adj_fuel, max_fuel)
    adj_t = newValues(adj_time, max_time)
    adj = []
    for i in range(length):
        adj_temp = []
        for j in range(length):
            adj_temp.append(round(adj_f[i][j] + adj_t[i][j], 3))
        adj.append(adj_temp)
    return adj
  
def getFuel(cityA, cityB):
    fuels = {
        "Vilnius": { "Vilnius": 0, "Kaunas": 8.884, "Klaipėda": 25.08, "Šiauliai": 17.24, "Panevėžys": 11.08, "Alytus": 10.672, "Marijampolė": 13.4, "Mažeikiai": 28.956, "Jonava": 10.236, "Utena": 7.912, "Kėdainiai": 13.28, "Tauragė": 19.52, "Telšiai": 26.04, "Ukmergė": 6.064, "Visaginas": 18, "Plungė": 24.6, "Kretinga": 26.24, "Palanga": 26.96, "Radviliškis": 15.56, "Šilutė": 26.52 },
        "Kaunas": { "Vilnius": 8.884, "Kaunas": 0, "Klaipėda": 17.56, "Šiauliai": 15.412, "Panevėžys": 9.12, "Alytus": 8.212, "Marijampolė": 5.288, "Mažeikiai": 23.44, "Jonava": 2.82, "Utena": 10.96, "Kėdainiai": 5.716, "Tauragė": 11.96, "Telšiai": 18.52, "Ukmergė": 5.912, "Visaginas": 17.92, "Plungė": 17.04, "Kretinga": 18.8, "Palanga": 19.4, "Radviliškis": 13.684, "Šilutė": 19.08 },
        "Klaipėda": { "Vilnius": 25.08, "Kaunas": 17.56, "Klaipėda": 0, "Šiauliai": 12.48, "Panevėžys": 23.52, "Alytus": 24.44, "Marijampolė": 21.8, "Mažeikiai": 12.704, "Jonava": 19.56, "Utena": 27.856, "Kėdainiai": 17.56, "Tauragė": 11.06, "Telšiai": 8.612, "Ukmergė": 22.776, "Visaginas": 34.908, "Plungė": 6.272, "Kretinga": 2.796, "Palanga": 2.68, "Radviliškis": 16.8, "Šilutė": 6.036 },
        "Šiauliai": { "Vilnius": 17.24, "Kaunas": 15.412, "Klaipėda": 12.48, "Šiauliai": 0, "Panevėžys": 6.548, "Alytus": 22.38, "Marijampolė": 19.636, "Mažeikiai": 8.772, "Jonava": 13.728, "Utena": 15.8, "Kėdainiai": 9.768, "Tauragė": 8.32, "Telšiai": 5.78, "Ukmergė": 11.64, "Visaginas": 29.196, "Plungė": 8.276, "Kretinga": 11.356, "Palanga": 12.12, "Radviliškis": 1.884, "Šilutė": 15.42 },
        "Panevėžys": { "Vilnius": 11.08, "Kaunas": 9.12, "Klaipėda": 23.52, "Šiauliai": 6.548, "Panevėžys": 0, "Alytus": 16.24, "Marijampolė": 13.24, "Mažeikiai": 15.672, "Jonava": 8.036, "Utena": 12.36, "Kėdainiai": 5.488, "Tauragė": 17.828, "Telšiai": 12.448, "Ukmergė": 5.724, "Visaginas": 19.92, "Plungė": 18.48, "Kretinga": 21.5, "Palanga": 22.384, "Radviliškis": 5.752, "Šilutė": 24.948 },
        "Alytus": { "Vilnius": 10.672, "Kaunas": 8.212, "Klaipėda": 24.44, "Šiauliai": 22.38, "Panevėžys": 16.24, "Alytus": 0, "Marijampolė": 5.916, "Mažeikiai": 30.6, "Jonava": 10.56, "Utena": 18.2, "Kėdainiai": 12.828, "Tauragė": 19.04, "Telšiai": 25.72, "Ukmergė": 13.62, "Visaginas": 29.236, "Plungė": 24.12, "Kretinga": 25.88, "Palanga": 26.48, "Radviliškis": 20.784, "Šilutė": 26.16 },
        "Marijampolė": { "Vilnius": 13.4, "Kaunas": 5.288, "Klaipėda": 21.8, "Šiauliai": 19.636, "Panevėžys": 13.24, "Alytus": 5.916, "Marijampolė": 0, "Mažeikiai": 27.664, "Jonava": 7.712, "Utena": 15.72, "Kėdainiai": 9.976, "Tauragė": 14.636, "Telšiai": 22.68, "Ukmergė": 10.72, "Visaginas": 22.76, "Plungė": 21.28, "Kretinga": 23.04, "Palanga": 23.64, "Radviliškis": 17.932, "Šilutė": 21.356 },
        "Mažeikiai": { "Vilnius": 28.956, "Kaunas": 23.44, "Klaipėda": 12.704, "Šiauliai": 8.772, "Panevėžys": 15.672, "Alytus": 30.6, "Marijampolė": 27.664, "Mažeikiai": 0, "Jonava": 22.852, "Utena": 23.136, "Kėdainiai": 18.892, "Tauragė": 17.13, "Telšiai": 4.776, "Ukmergė": 20.736, "Visaginas": 35.776, "Plungė": 6.732, "Kretinga": 9.812, "Palanga": 10.624, "Radviliškis": 10.932, "Šilutė": 17.88 },
        "Jonava": { "Vilnius": 10.236, "Kaunas": 2.82, "Klaipėda": 19.56, "Šiauliai": 13.728, "Panevėžys": 8.036, "Alytus": 10.56, "Marijampolė": 7.712, "Mažeikiai": 22.852, "Jonava": 0, "Utena": 8.296, "Kėdainiai": 4.14, "Tauragė": 15.44, "Telšiai": 21.992, "Ukmergė": 3.228, "Visaginas": 15.24, "Plungė": 18.64, "Kretinga": 20.44, "Palanga": 21.04, "Radviliškis": 12.036, "Šilutė": 20.72 },
        "Utena": { "Vilnius": 7.912, "Kaunas": 10.96, "Klaipėda": 27.856, "Šiauliai": 15.8, "Panevėžys": 12.36, "Alytus": 18.2, "Marijampolė": 15.72, "Mažeikiai": 23.136, "Jonava": 8.296, "Utena": 0, "Kėdainiai": 12.268, "Tauragė": 21.8, "Telšiai": 27.488, "Ukmergė": 5.184, "Visaginas": 6.668, "Plungė": 29.448, "Kretinga": 28.856, "Palanga": 29.576, "Radviliškis": 14.596, "Šilutė": 29.136 },
        "Kėdainiai": { "Vilnius": 13.28, "Kaunas": 5.716, "Klaipėda": 17.56, "Šiauliai": 9.768, "Panevėžys": 5.488, "Alytus": 12.828, "Marijampolė": 9.976, "Mažeikiai": 18.892, "Jonava": 4.14, "Utena": 12.268, "Kėdainiai": 0, "Tauragė": 11.84, "Telšiai": 18.516, "Ukmergė": 6.976, "Visaginas": 18.612, "Plungė": 16.92, "Kretinga": 18.72, "Palanga": 19.32, "Radviliškis": 8.064, "Šilutė": 18.96 },
        "Tauragė": { "Vilnius": 19.52, "Kaunas": 11.96, "Klaipėda": 11.06, "Šiauliai": 8.32, "Panevėžys": 17.828, "Alytus": 19.04, "Marijampolė": 14.636, "Mažeikiai": 17.13, "Jonava": 15.44, "Utena": 21.8, "Kėdainiai": 11.84, "Tauragė": 0, "Telšiai": 11.412, "Ukmergė": 17.096, "Visaginas": 29.12, "Plungė": 10.476, "Kretinga": 12.196, "Palanga": 12.912, "Radviliškis": 10.372, "Šilutė": 7.184 },
        "Telšiai": { "Vilnius": 26.04, "Kaunas": 18.52, "Klaipėda": 8.612, "Šiauliai": 5.78, "Panevėžys": 12.448, "Alytus": 25.72, "Marijampolė": 22.68, "Mažeikiai": 4.776, "Jonava": 21.992, "Utena": 27.488, "Kėdainiai": 18.516, "Tauragė": 11.412, "Telšiai": 0, "Ukmergė": 17.652, "Visaginas": 35.116, "Plungė": 2.656, "Kretinga": 5.752, "Palanga": 6.56, "Radviliškis": 7.916, "Šilutė": 13.9 },
        "Ukmergė": { "Vilnius": 6.064, "Kaunas": 5.912, "Klaipėda": 22.776, "Šiauliai": 11.64, "Panevėžys": 5.724, "Alytus": 13.62, "Marijampolė": 10.72, "Mažeikiai": 20.736, "Jonava": 3.228, "Utena": 5.184, "Kėdainiai": 6.976, "Tauragė": 17.096, "Telšiai": 17.652, "Ukmergė": 0, "Visaginas": 12.012, "Plungė": 21.8, "Kretinga": 23.48, "Palanga": 24.2, "Radviliškis": 10.404, "Šilutė": 23.84 },
        "Visaginas": { "Vilnius": 18, "Kaunas": 17.92, "Klaipėda": 34.908, "Šiauliai": 29.196, "Panevėžys": 19.92, "Alytus": 29.236, "Marijampolė": 22.76, "Mažeikiai": 35.776, "Jonava": 15.24, "Utena": 6.668, "Kėdainiai": 18.612, "Tauragė": 29.12, "Telšiai": 35.116, "Ukmergė": 12.012, "Visaginas": 0, "Plungė": 37.268, "Kretinga": 40.2, "Palanga": 41, "Radviliškis": 28.32, "Šilutė": 36.08 },
        "Plungė": { "Vilnius": 24.6, "Kaunas": 17.04, "Klaipėda": 6.272, "Šiauliai": 8.276, "Panevėžys": 18.48, "Alytus": 24.12, "Marijampolė": 21.28, "Mažeikiai": 6.732, "Jonava": 18.64, "Utena": 29.448, "Kėdainiai": 16.92, "Tauragė": 10.476, "Telšiai": 2.656, "Ukmergė": 21.8, "Visaginas": 37.268, "Plungė": 0, "Kretinga": 3.72, "Palanga": 4.66, "Radviliškis": 10.108, "Šilutė": 10.332 },
        "Kretinga": { "Vilnius": 26.24, "Kaunas": 18.8, "Klaipėda": 2.796, "Šiauliai": 11.356, "Panevėžys": 21.5, "Alytus": 25.88, "Marijampolė": 23.04, "Mažeikiai": 9.812, "Jonava": 20.44, "Utena": 28.856, "Kėdainiai": 18.72, "Tauragė": 12.196, "Telšiai": 5.752, "Ukmergė": 23.48, "Visaginas": 40.2, "Plungė": 3.72, "Kretinga": 0, "Palanga": 1.204, "Radviliškis": 13.236, "Šilutė": 8.532 },
        "Palanga": { "Vilnius": 26.96, "Kaunas": 19.4, "Klaipėda": 2.68, "Šiauliai": 12.12, "Panevėžys": 22.384, "Alytus": 26.48, "Marijampolė": 23.64, "Mažeikiai": 10.624, "Jonava": 21.04, "Utena": 29.576, "Kėdainiai": 19.32, "Tauragė": 12.912, "Telšiai": 6.56, "Ukmergė": 24.2, "Visaginas": 41, "Plungė": 4.66, "Kretinga": 1.204, "Palanga": 0, "Radviliškis": 13.876, "Šilutė": 8.892 },
        "Radviliškis": { "Vilnius": 15.56, "Kaunas": 13.684, "Klaipėda": 16.8, "Šiauliai": 1.884, "Panevėžys": 5.752, "Alytus": 20.784, "Marijampolė": 17.932, "Mažeikiai": 10.932, "Jonava": 12.036, "Utena": 14.596, "Kėdainiai": 8.064, "Tauragė": 10.372, "Telšiai": 7.916, "Ukmergė": 10.404, "Visaginas": 28.32, "Plungė": 10.108, "Kretinga": 13.236, "Palanga": 13.876, "Radviliškis": 0, "Šilutė": 18.916 },
        "Šilutė": { "Vilnius": 26.52, "Kaunas": 19.08, "Klaipėda": 6.036, "Šiauliai": 15.42, "Panevėžys": 24.948, "Alytus": 26.16, "Marijampolė": 21.356, "Mažeikiai": 17.88, "Jonava": 20.72, "Utena": 29.136, "Kėdainiai": 18.96, "Tauragė": 7.184, "Telšiai": 13.9, "Ukmergė": 23.84, "Visaginas": 36.08, "Plungė": 10.332, "Kretinga": 8.532, "Palanga": 8.892, "Radviliškis": 18.916, "Šilutė": 0 }
    }

    f = fuels[cityA][cityB]
    return f

def getDuration(cityA, cityB):
    durations = {
        "Vilnius": { "Vilnius": 0, "Kaunas": 75, "Klaipėda": 193, "Šiauliai": 159, "Panevėžys": 94, "Alytus": 89, "Marijampolė": 111, "Mažeikiai": 220, "Jonava": 81, "Utena": 77, "Kėdainiai": 103, "Tauragė": 155, "Telšiai": 188, "Ukmergė": 53, "Visaginas": 127, "Plungė": 185, "Kretinga": 198, "Palanga": 209, "Radviliškis": 139, "Šilutė": 204 },
        "Kaunas": { "Vilnius": 77, "Kaunas": 0, "Klaipėda": 136, "Šiauliai": 122, "Panevėžys": 88, "Alytus": 64, "Marijampolė": 47, "Mažeikiai": 165, "Jonava": 32, "Utena": 113, "Kėdainiai": 46, "Tauragė": 98, "Telšiai": 131, "Ukmergė": 65, "Visaginas": 173, "Plungė": 128, "Kretinga": 142, "Palanga": 152, "Radviliškis": 101, "Šilutė": 148 },
        "Klaipėda": { "Vilnius": 197, "Kaunas": 137, "Klaipėda": 0, "Šiauliai": 127, "Panevėžys": 174, "Alytus": 186, "Marijampolė": 169, "Mažeikiai": 95, "Jonava": 151, "Utena": 232, "Kėdainiai": 132, "Tauragė": 81, "Telšiai": 74, "Ukmergė": 184, "Visaginas": 292, "Plungė": 49, "Kretinga": 29, "Palanga": 30, "Radviliškis": 144, "Šilutė": 46 },
        "Šiauliai": { "Vilnius": 153, "Kaunas": 122, "Klaipėda": 126, "Šiauliai": 0, "Panevėžys": 73, "Alytus": 171, "Marijampolė": 154, "Mažeikiai": 66, "Jonava": 105, "Utena": 149, "Kėdainiai": 80, "Tauragė": 88, "Telšiai": 58, "Ukmergė": 107, "Visaginas": 192, "Plungė": 78, "Kretinga": 108, "Palanga": 118, "Radviliškis": 23, "Šilutė": 138 },
        "Panevėžys": { "Vilnius": 96, "Kaunas": 88, "Klaipėda": 173, "Šiauliai": 79, "Panevėžys": 0, "Alytus": 137, "Marijampolė": 120, "Mažeikiai": 139, "Jonava": 70, "Utena": 84, "Kėdainiai": 55, "Tauragė": 135, "Telšiai": 132, "Ukmergė": 50, "Visaginas": 133, "Plungė": 152, "Kretinga": 179, "Palanga": 189, "Radviliškis": 63, "Šilutė": 185 },
        "Alytus": { "Vilnius": 89, "Kaunas": 63, "Klaipėda": 185, "Šiauliai": 171, "Panevėžys": 137, "Alytus": 0, "Marijampolė": 52, "Mažeikiai": 214, "Jonava": 79, "Utena": 154, "Kėdainiai": 95, "Tauragė": 147, "Telšiai": 180, "Ukmergė": 111, "Visaginas": 209, "Plungė": 177, "Kretinga": 191, "Palanga": 201, "Radviliškis": 150, "Šilutė": 197 },
        "Marijampolė": { "Vilnius": 113, "Kaunas": 48, "Klaipėda": 170, "Šiauliai": 156, "Panevėžys": 122, "Alytus": 52, "Marijampolė": 0, "Mažeikiai": 199, "Jonava": 71, "Utena": 152, "Kėdainiai": 80, "Tauragė": 104, "Telšiai": 165, "Ukmergė": 103, "Visaginas": 211, "Plungė": 162, "Kretinga": 176, "Palanga": 186, "Radviliškis": 135, "Šilutė": 156 },
        "Mažeikiai": { "Vilnius": 218, "Kaunas": 167, "Klaipėda": 95, "Šiauliai": 66, "Panevėžys": 138, "Alytus": 216, "Marijampolė": 199, "Mažeikiai": 0, "Jonava": 170, "Utena": 206, "Kėdainiai": 145, "Tauragė": 115, "Telšiai": 36, "Ukmergė": 172, "Visaginas": 255, "Plungė": 47, "Kretinga": 77, "Palanga": 87, "Radviliškis": 88, "Šilutė": 121 },
        "Jonava": { "Vilnius": 78, "Kaunas": 32, "Klaipėda": 150, "Šiauliai": 104, "Panevėžys": 70, "Alytus": 79, "Marijampolė": 68, "Mažeikiai": 169, "Jonava": 0, "Utena": 81, "Kėdainiai": 29, "Tauragė": 112, "Telšiai": 145, "Ukmergė": 32, "Visaginas": 140, "Plungė": 142, "Kretinga": 156, "Palanga": 166, "Radviliškis": 84, "Šilutė": 161 },
        "Utena": { "Vilnius": 77, "Kaunas": 114, "Klaipėda": 231, "Šiauliai": 145, "Panevėžys": 84, "Alytus": 153, "Marijampolė": 150, "Mažeikiai": 205, "Jonava": 81, "Utena": 0, "Kėdainiai": 104, "Tauragė": 193, "Telšiai": 198, "Ukmergė": 55, "Visaginas": 59, "Plungė": 218, "Kretinga": 237, "Palanga": 247, "Radviliškis": 135, "Šilutė": 243 },
        "Kėdainiai": { "Vilnius": 106, "Kaunas": 47, "Klaipėda": 130, "Šiauliai": 80, "Panevėžys": 56, "Alytus": 95, "Marijampolė": 78, "Mažeikiai": 144, "Jonava": 29, "Utena": 104, "Kėdainiai": 0, "Tauragė": 92, "Telšiai": 125, "Ukmergė": 57, "Visaginas": 164, "Plungė": 122, "Kretinga": 136, "Palanga": 146, "Radviliškis": 59, "Šilutė": 141 },
        "Tauragė": { "Vilnius": 157, "Kaunas": 97, "Klaipėda": 80, "Šiauliai": 86, "Panevėžys": 134, "Alytus": 146, "Marijampolė": 105, "Mažeikiai": 113, "Jonava": 111, "Utena": 192, "Kėdainiai": 92, "Tauragė": 0, "Telšiai": 80, "Ukmergė": 144, "Visaginas": 252, "Plungė": 71, "Kretinga": 86, "Palanga": 96, "Radviliškis": 103, "Šilutė": 56 },
        "Telšiai": { "Vilnius": 192, "Kaunas": 132, "Klaipėda": 74, "Šiauliai": 58, "Panevėžys": 129, "Alytus": 181, "Marijampolė": 164, "Mažeikiai": 36, "Jonava": 146, "Utena": 198, "Kėdainiai": 127, "Tauragė": 81, "Telšiai": 0, "Ukmergė": 164, "Visaginas": 247, "Plungė": 26, "Kretinga": 56, "Palanga": 66, "Radviliškis": 80, "Šilutė": 100 },
        "Ukmergė": { "Vilnius": 55, "Kaunas": 65, "Klaipėda": 183, "Šiauliai": 115, "Panevėžys": 50, "Alytus": 112, "Marijampolė": 101, "Mažeikiai": 176, "Jonava": 32, "Utena": 54, "Kėdainiai": 57, "Tauragė": 145, "Telšiai": 168, "Ukmergė": 0, "Visaginas": 113, "Plungė": 175, "Kretinga": 189, "Palanga": 199, "Radviliškis": 94, "Šilutė": 194 },
        "Visaginas": { "Vilnius": 129, "Kaunas": 173, "Klaipėda": 291, "Šiauliai": 194, "Panevėžys": 133, "Alytus": 210, "Marijampolė": 209, "Mažeikiai": 255, "Jonava": 141, "Utena": 59, "Kėdainiai": 164, "Tauragė": 253, "Telšiai": 247, "Ukmergė": 114, "Visaginas": 0, "Plungė": 267, "Kretinga": 297, "Palanga": 307, "Radviliškis": 187, "Šilutė": 303 },
        "Plungė": { "Vilnius": 189, "Kaunas": 129, "Klaipėda": 48, "Šiauliai": 78, "Panevėžys": 149, "Alytus": 178, "Marijampolė": 161, "Mažeikiai": 46, "Jonava": 143, "Utena": 218, "Kėdainiai": 123, "Tauragė": 72, "Telšiai": 26, "Ukmergė": 175, "Visaginas": 267, "Plungė": 0, "Kretinga": 40, "Palanga": 50, "Radviliškis": 100, "Šilutė": 75 },
        "Kretinga": { "Vilnius": 204, "Kaunas": 144, "Klaipėda": 29, "Šiauliai": 108, "Panevėžys": 179, "Alytus": 193, "Marijampolė": 176, "Mažeikiai": 76, "Jonava": 158, "Utena": 239, "Kėdainiai": 138, "Tauragė": 88, "Telšiai": 55, "Ukmergė": 191, "Visaginas": 299, "Plungė": 39, "Kretinga": 0, "Palanga": 17, "Radviliškis": 130, "Šilutė": 64 },
        "Palanga": { "Vilnius": 211, "Kaunas": 151, "Klaipėda": 27, "Šiauliai": 117, "Panevėžys": 188, "Alytus": 200, "Marijampolė": 183, "Mažeikiai": 85, "Jonava": 165, "Utena": 246, "Kėdainiai": 146, "Tauragė": 95, "Telšiai": 64, "Ukmergė": 198, "Visaginas": 306, "Plungė": 48, "Kretinga": 16, "Palanga": 0, "Radviliškis": 139, "Šilutė": 61 },
        "Radviliškis": { "Vilnius": 132, "Kaunas": 101, "Klaipėda": 141, "Šiauliai": 23, "Panevėžys": 52, "Alytus": 150, "Marijampolė": 133, "Mažeikiai": 88, "Jonava": 84, "Utena": 128, "Kėdainiai": 59, "Tauragė": 102, "Telšiai": 80, "Ukmergė": 86, "Visaginas": 181, "Plungė": 100, "Kretinga": 130, "Palanga": 140, "Radviliškis": 0, "Šilutė": 152 },
        "Šilutė": { "Vilnius": 208, "Kaunas": 148, "Klaipėda": 47, "Šiauliai": 137, "Panevėžys": 185, "Alytus": 197, "Marijampolė": 157, "Mažeikiai": 121, "Jonava": 162, "Utena": 243, "Kėdainiai": 142, "Tauragė": 56, "Telšiai": 100, "Ukmergė": 194, "Visaginas": 303, "Plungė": 75, "Kretinga": 63, "Palanga": 63, "Radviliškis": 155, "Šilutė": 0 }
    }
    t = durations[cityA][cityB]
    return t

def getRouteDuration(route):
    suma = 0
    for i in range(len(route)-1):
        city_a = route[i]
        city_b = route[i+1]
        d = getDuration(city_a,city_b)
        suma += d
    return suma

def getRouteFuelCost(route):
    suma = 0
    for i in range(len(route)-1):
        city_a = route[i]
        city_b = route[i+1]
        d = getFuel(city_a,city_b)
        suma += d
    return suma

def convertPathToCities(path):
    citiesPath = []
    for i in range(len(path)):
        for j in range(len(cities)):
            if path[i] == j:
                citiesPath.append(cities[j])
    return citiesPath

def printFinalResults(path, executionTime):
    print("Path Taken: ", path)
    totalDuration = getRouteDuration(final_cities_path)
    totalFuelCost = round(getRouteFuelCost(final_cities_path), 3)
    print("Path total duration: " + str(totalDuration) + " min")
    print("Path total fuel: " + str(totalFuelCost) + " liters")
    print("Time: " + str(executionTime) + "s")

# Main code

start = tm.time()
executionTime = 0
cities = ['Vilnius', 'Kaunas', 'Klaipėda', 'Šiauliai', 'Panevėžys', 'Alytus', 'Marijampolė', 'Mažeikiai',
'Jonava', 'Utena', 'Kėdainiai', 'Tauragė', 'Telšiai', 'Ukmergė', 'Visaginas', 'Plungė', 'Kretinga', 'Palanga', 'Radviliškis', 'Šilutė']

# Fuel cost values (liters)
adj_fuel = [
	[0, 8.884, 25.08, 17.24, 11.08, 10.672, 13.4, 28.956, 10.236, 7.912, 13.28, 19.52, 26.04, 6.064, 18, 24.6, 26.24, 26.96, 15.56, 26.52], 
	[8.884, 0, 17.56, 15.412, 9.12, 8.212, 5.288, 23.44, 2.82, 10.96, 5.716, 11.96, 18.52, 5.912, 17.92, 17.04, 18.8, 19.4, 13.684, 19.08], 
	[25.08, 17.56, 0, 12.48, 23.52, 24.44, 21.8, 12.704, 19.56, 27.856, 17.56, 11.06, 8.612, 22.776, 34.908, 6.272, 2.796, 2.68, 16.8, 6.036], 
	[17.24, 15.412, 12.48, 0, 6.548, 22.38, 19.636, 8.772, 13.728, 15.8, 9.768, 8.32, 5.78, 11.64, 29.196, 8.276, 11.356, 12.12, 1.884, 15.42], 
	[11.08, 9.12, 23.52, 6.548, 0, 16.24, 13.24, 15.672, 8.036, 12.36, 5.488, 17.828, 12.448, 5.724, 19.92, 18.48, 21.5, 22.384, 5.752, 24.948], 
	[10.672, 8.212, 24.44, 22.38, 16.24, 0, 5.916, 30.6, 10.56, 18.2, 12.828, 19.04, 25.72, 13.62, 29.236, 24.12, 25.88, 26.48, 20.784, 26.16], 
	[13.4, 5.288, 21.8, 19.636, 13.24, 5.916, 0, 27.664, 7.712, 15.72, 9.976, 14.636, 22.68, 10.72, 22.76, 21.28, 23.04, 23.64, 17.932, 21.356], 
	[28.956, 23.44, 12.704, 8.772, 15.672, 30.6, 27.664, 0, 22.852, 23.136, 18.892, 17.13, 4.776, 20.736, 35.776, 6.732, 9.812, 10.624, 10.932, 17.88], 
	[10.236, 2.82, 19.56, 13.728, 8.036, 10.56, 7.712, 22.852, 0, 8.296, 4.14, 15.44, 21.992, 3.228, 15.24, 18.64, 20.44, 21.04, 12.036, 20.72], 
	[7.912, 10.96, 27.856, 15.8, 12.36, 18.2, 15.72, 23.136, 8.296, 0, 12.268, 21.8, 27.488, 5.184, 6.668, 29.448, 28.856, 29.576, 14.596, 29.136], 
	[13.28, 5.716, 17.56, 9.768, 5.488, 12.828, 9.976, 18.892, 4.14, 12.268, 0, 11.84, 18.516, 6.976, 18.612, 16.92, 18.72, 19.32, 8.064, 18.96], 
	[19.52, 11.96, 11.06, 8.32, 17.828, 19.04, 14.636, 17.13, 15.44, 21.8, 11.84, 0, 11.412, 17.096, 29.12, 10.476, 12.196, 12.912, 10.372, 7.184], 
	[26.04, 18.52, 8.612, 5.78, 12.448, 25.72, 22.68, 4.776, 21.992, 27.488, 18.516, 11.412, 0, 17.652, 35.116, 2.656, 5.752, 6.56, 7.916, 13.9], 
	[6.064, 5.912, 22.776, 11.64, 5.724, 13.62, 10.72, 20.736, 3.228, 5.184, 6.976, 17.096, 17.652, 0, 12.012, 21.8, 23.48, 24.2, 10.404, 23.84], 
	[18, 17.92, 34.908, 29.196, 19.92, 29.236, 22.76, 35.776, 15.24, 6.668, 18.612, 29.12, 35.116, 12.012, 0, 37.268, 40.2, 41, 28.32, 36.08], 
	[24.6, 17.04, 6.272, 8.276, 18.48, 24.12, 21.28, 6.732, 18.64, 29.448, 16.92, 10.476, 2.656, 21.8, 37.268, 0, 3.72, 4.66, 10.108, 10.332], 
	[26.24, 18.8, 2.796, 11.356, 21.5, 25.88, 23.04, 9.812, 20.44, 28.856, 18.72, 12.196, 5.752, 23.48, 40.2, 3.72, 0, 1.204, 13.236, 8.532], 
	[26.96, 19.4, 2.68, 12.12, 22.384, 26.48, 23.64, 10.624, 21.04, 29.576, 19.32, 12.912, 6.56, 24.2, 41, 4.66, 1.204, 0, 13.876, 8.892], 
	[15.56, 13.684, 16.8, 1.884, 5.752, 20.784, 17.932, 10.932, 12.036, 14.596, 8.064, 10.372, 7.916, 10.404, 28.32, 10.108, 13.236, 13.876, 0, 18.916], 
	[26.52, 19.08, 6.036, 15.42, 24.948, 26.16, 21.356, 17.88, 20.72, 29.136, 18.96, 7.184, 13.9, 23.84, 36.08, 10.332, 8.532, 8.892, 18.916, 0]
]

# Traveling time values (min)
adj_time = [
	[0, 75, 193, 159, 94, 89, 111, 220, 81, 77, 103, 155, 188, 53, 127, 185, 198, 209, 139, 204], 
	[77, 0, 136, 122, 88, 64, 47, 165, 32, 113, 46, 98, 131, 65, 173, 128, 142, 152, 101, 148], 
	[197, 137, 0, 127, 174, 186, 169, 95, 151, 232, 132, 81, 74, 184, 292, 49, 29, 30, 144, 46], 
	[153, 122, 126, 0, 73, 171, 154, 66, 105, 149, 80, 88, 58, 107, 192, 78, 108, 118, 23, 138], 
	[96, 88, 173, 79, 0, 137, 120, 139, 70, 84, 55, 135, 132, 50, 133, 152, 179, 189, 63, 185], 
	[89, 63, 185, 171, 137, 0, 52, 214, 79, 154, 95, 147, 180, 111, 209, 177, 191, 201, 150, 197], 
	[113, 48, 170, 156, 122, 52, 0, 199, 71, 152, 80, 104, 165, 103, 211, 162, 176, 186, 135, 156], 
	[218, 167, 95, 66, 138, 216, 199, 0, 170, 206, 145, 115, 36, 172, 255, 47, 77, 87, 88, 121], 
	[78, 32, 150, 104, 70, 79, 68, 169, 0, 81, 29, 112, 145, 32, 140, 142, 156, 166, 84, 161], 
	[77, 114, 231, 145, 84, 153, 150, 205, 81, 0, 104, 193, 198, 55, 59, 218, 237, 247, 135, 243], 
	[106, 47, 130, 80, 56, 95, 78, 144, 29, 104, 0, 92, 125, 57, 164, 122, 136, 146, 59, 141], 
	[157, 97, 80, 86, 134, 146, 105, 113, 111, 192, 92, 0, 80, 144, 252, 71, 86, 96, 103, 56], 
	[192, 132, 74, 58, 129, 181, 164, 36, 146, 198, 127, 81, 0, 164, 247, 26, 56, 66, 80, 100], 
	[55, 65, 183, 115, 50, 112, 101, 176, 32, 54, 57, 145, 168, 0, 113, 175, 189, 199, 94, 194], 
	[129, 173, 291, 194, 133, 210, 209, 255, 141, 59, 164, 253, 247, 114, 0, 267, 297, 307, 187, 303], 
	[189, 129, 48, 78, 149, 178, 161, 46, 143, 218, 123, 72, 26, 175, 267, 0, 40, 50, 100, 75], 
	[204, 144, 29, 108, 179, 193, 176, 76, 158, 239, 138, 88, 55, 191, 299, 39, 0, 17, 130, 64], 
	[211, 151, 27, 117, 188, 200, 183, 85, 165, 246, 146, 95, 64, 198, 306, 48, 16, 0, 139, 61], 
	[132, 101, 141, 23, 52, 150, 133, 88, 84, 128, 59, 102, 80, 86, 181, 100, 130, 140, 0, 152], 
	[208, 148, 47, 137, 185, 197, 157, 121, 162, 243, 142, 56, 100, 194, 303, 75, 63, 63, 155, 0]
]

adj = normalizedValues(adj_fuel, adj_time)

N = 20

final_path = [None] * (N + 1)

visited = [False] * N

final_res = maxsize

TSP(adj)

final_cities_path = convertPathToCities(final_path)
executionTime = (tm.time() - start)

printFinalResults(final_cities_path, executionTime)