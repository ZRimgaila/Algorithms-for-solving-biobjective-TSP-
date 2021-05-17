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
    # didziausios vertes radimas
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
        "Vilnius": { "Vilnius": 0, "Kaunas": 11.716, "Klaipėda": 36.32, "Šiauliai": 25.56, "Panevėžys": 16.32, "Alytus": 11.128, "Marijampolė": 18.8, "Mažeikiai": 31.644, "Jonava": 9.664, "Utena": 11.568, "Kėdainiai": 16.52, "Tauragė": 28.08, "Telšiai": 30.56, "Ukmergė": 8.576, "Visaginas": 12, "Plungė": 32.4, "Kretinga": 36.16, "Palanga": 39.24, "Radviliškis": 23.04, "Šilutė": 32.28 },
        "Kaunas": { "Vilnius": 11.716, "Kaunas": 0, "Klaipėda": 25.44, "Šiauliai": 14.388, "Panevėžys": 12.88, "Alytus": 6.208, "Marijampolė": 7.032, "Mažeikiai": 22.96, "Jonava": 3.52, "Utena": 15.84, "Kėdainiai": 5.604, "Tauragė": 17.24, "Telšiai": 19.68, "Ukmergė": 8.108, "Visaginas": 22.68, "Plungė": 21.56, "Kretinga": 25.4, "Palanga": 28.4, "Radviliškis": 11.916, "Šilutė": 21.32 },
        "Klaipėda": { "Vilnius": 36.32, "Kaunas": 25.44, "Klaipėda": 0, "Šiauliai": 18.32, "Panevėžys": 24.28, "Alytus": 30.96, "Marijampolė": 32, "Mažeikiai": 9.696, "Jonava": 26.64, "Utena": 38.744, "Kėdainiai": 23.64, "Tauragė": 10.94, "Telšiai": 8.588, "Ukmergė": 31.024, "Visaginas": 45.492, "Plungė": 5.048, "Kretinga": 2.384, "Palanga": 3.38, "Radviliškis": 22.2, "Šilutė": 4.024 },
        "Šiauliai": { "Vilnius": 25.56, "Kaunas": 14.388, "Klaipėda": 18.32, "Šiauliai": 0, "Panevėžys": 9.452, "Alytus": 20.02, "Marijampolė": 20.964, "Mažeikiai": 7.228, "Jonava": 11.472, "Utena": 23.6, "Kėdainiai": 8.832, "Tauragė": 12.28, "Telšiai": 8.42, "Ukmergė": 16.96, "Visaginas": 19.604, "Plungė": 11.424, "Kretinga": 16.244, "Palanga": 17.48, "Radviliškis": 2.636, "Šilutė": 16.38 },
        "Panevėžys": { "Vilnius": 16.32, "Kaunas": 12.88, "Klaipėda": 24.28, "Šiauliai": 9.452, "Panevėžys": 0, "Alytus": 18.56, "Marijampolė": 19.36, "Mažeikiai": 16.728, "Jonava": 9.564, "Utena": 8.24, "Kėdainiai": 7.312, "Tauragė": 15.972, "Telšiai": 17.952, "Ukmergė": 8.076, "Visaginas": 13.28, "Plungė": 20.32, "Kretinga": 25.1, "Palanga": 26.416, "Radviliškis": 7.548, "Šilutė": 20.052 },
        "Alytus": { "Vilnius": 11.128, "Kaunas": 6.208, "Klaipėda": 30.96, "Šiauliai": 20.02, "Panevėžys": 18.56, "Alytus": 0, "Marijampolė": 5.224, "Mažeikiai": 28.8, "Jonava": 9.2, "Utena": 22.6, "Kėdainiai": 11.372, "Tauragė": 22.96, "Telšiai": 25.48, "Ukmergė": 13.78, "Visaginas": 24.564, "Plungė": 27.28, "Kretinga": 31.12, "Palanga": 34.12, "Radviliškis": 17.616, "Šilutė": 27.04 },
        "Marijampolė": { "Vilnius": 18.8, "Kaunas": 7.032, "Klaipėda": 32, "Šiauliai": 20.964, "Panevėžys": 19.36, "Alytus": 5.224, "Marijampolė": 0, "Mažeikiai": 29.736, "Jonava": 11.088, "Utena": 23.28, "Kėdainiai": 12.224, "Tauragė": 10.564, "Telšiai": 26.52, "Ukmergė": 15.68, "Visaginas": 30.24, "Plungė": 28.12, "Kretinga": 31.96, "Palanga": 34.96, "Radviliškis": 18.468, "Šilutė": 15.044 },
        "Mažeikiai": { "Vilnius": 31.644, "Kaunas": 22.96, "Klaipėda": 9.696, "Šiauliai": 7.228, "Panevėžys": 16.728, "Alytus": 28.8, "Marijampolė": 29.736, "Mažeikiai": 0, "Jonava": 18.748, "Utena": 29.664, "Kėdainiai": 16.108, "Tauragė": 11.47, "Telšiai": 3.184, "Ukmergė": 24.264, "Visaginas": 29.624, "Plungė": 4.488, "Kretinga": 9.308, "Palanga": 10.576, "Radviliškis": 9.868, "Šilutė": 11.92 },
        "Jonava": { "Vilnius": 9.664, "Kaunas": 3.52, "Klaipėda": 26.64, "Šiauliai": 11.472, "Panevėžys": 9.564, "Alytus": 9.2, "Marijampolė": 11.088, "Mažeikiai": 18.748, "Jonava": 0, "Utena": 12.104, "Kėdainiai": 2.76, "Tauragė": 17.76, "Telšiai": 20.208, "Ukmergė": 4.392, "Visaginas": 18.96, "Plungė": 24.56, "Kretinga": 28.36, "Palanga": 31.36, "Radviliškis": 8.964, "Šilutė": 24.28 },
        "Utena": { "Vilnius": 11.568, "Kaunas": 15.84, "Klaipėda": 38.744, "Šiauliai": 23.6, "Panevėžys": 8.24, "Alytus": 22.6, "Marijampolė": 23.28, "Mažeikiai": 29.664, "Jonava": 12.104, "Utena": 0, "Kėdainiai": 12.932, "Tauragė": 32.6, "Telšiai": 23.512, "Ukmergė": 7.656, "Visaginas": 7.632, "Plungė": 26.352, "Kretinga": 40.344, "Palanga": 43.424, "Radviliškis": 21.004, "Šilutė": 36.264 },
        "Kėdainiai": { "Vilnius": 16.52, "Kaunas": 5.604, "Klaipėda": 23.64, "Šiauliai": 8.832, "Panevėžys": 7.312, "Alytus": 11.372, "Marijampolė": 12.224, "Mažeikiai": 16.108, "Jonava": 2.76, "Utena": 12.932, "Kėdainiai": 0, "Tauragė": 15.36, "Telšiai": 17.884, "Ukmergė": 4.804, "Visaginas": 19.388, "Plungė": 19.68, "Kretinga": 23.48, "Palanga": 26.48, "Radviliškis": 6.316, "Šilutė": 19.44 },
        "Tauragė": { "Vilnius": 28.08, "Kaunas": 17.24, "Klaipėda": 10.94, "Šiauliai": 12.28, "Panevėžys": 15.972, "Alytus": 22.96, "Marijampolė": 10.564, "Mažeikiai": 11.47, "Jonava": 17.76, "Utena": 32.6, "Kėdainiai": 15.36, "Tauragė": 0, "Telšiai": 7.608, "Ukmergė": 22.704, "Visaginas": 37.28, "Plungė": 6.984, "Kretinga": 10.804, "Palanga": 13.888, "Radviliškis": 14.628, "Šilutė": 5.156 },
        "Telšiai": { "Vilnius": 30.56, "Kaunas": 19.68, "Klaipėda": 8.588, "Šiauliai": 8.42, "Panevėžys": 17.952, "Alytus": 25.48, "Marijampolė": 26.52, "Mažeikiai": 3.184, "Jonava": 20.208, "Utena": 23.512, "Kėdainiai": 17.884, "Tauragė": 7.608, "Telšiai": 0, "Ukmergė": 25.348, "Visaginas": 28.484, "Plungė": 3.404, "Kretinga": 8.228, "Palanga": 9.5, "Radviliškis": 11.004, "Šilutė": 10.9 },
        "Ukmergė": { "Vilnius": 8.576, "Kaunas": 8.108, "Klaipėda": 31.024, "Šiauliai": 16.96, "Panevėžys": 8.076, "Alytus": 13.78, "Marijampolė": 15.68, "Mažeikiai": 24.264, "Jonava": 4.392, "Utena": 7.656, "Kėdainiai": 4.804, "Tauragė": 22.704, "Telšiai": 25.348, "Ukmergė": 0, "Visaginas": 14.388, "Plungė": 29.2, "Kretinga": 32.92, "Palanga": 36, "Radviliškis": 14.396, "Šilutė": 28.96 },
        "Visaginas": { "Vilnius": 12, "Kaunas": 22.68, "Klaipėda": 45.492, "Šiauliai": 19.604, "Panevėžys": 13.28, "Alytus": 24.564, "Marijampolė": 30.24, "Mažeikiai": 29.624, "Jonava": 18.96, "Utena": 7.632, "Kėdainiai": 19.388, "Tauragė": 37.28, "Telšiai": 28.484, "Ukmergė": 14.388, "Visaginas": 0, "Plungė": 31.132, "Kretinga": 36.2, "Palanga": 37.4, "Radviliškis": 18.88, "Šilutė": 43.12 },
        "Plungė": { "Vilnius": 32.4, "Kaunas": 21.56, "Klaipėda": 5.048, "Šiauliai": 11.424, "Panevėžys": 20.32, "Alytus": 27.28, "Marijampolė": 28.12, "Mažeikiai": 4.488, "Jonava": 24.56, "Utena": 26.352, "Kėdainiai": 19.68, "Tauragė": 6.984, "Telšiai": 3.404, "Ukmergė": 29.2, "Visaginas": 31.132, "Plungė": 0, "Kretinga": 5, "Palanga": 6.16, "Radviliškis": 14.092, "Šilutė": 6.888 },
        "Kretinga": { "Vilnius": 36.16, "Kaunas": 25.4, "Klaipėda": 2.384, "Šiauliai": 16.244, "Panevėžys": 25.1, "Alytus": 31.12, "Marijampolė": 31.96, "Mažeikiai": 9.308, "Jonava": 28.36, "Utena": 40.344, "Kėdainiai": 23.48, "Tauragė": 10.804, "Telšiai": 8.228, "Ukmergė": 32.92, "Visaginas": 36.2, "Plungė": 5, "Kretinga": 0, "Palanga": 1.496, "Radviliškis": 18.964, "Šilutė": 5.688 },
        "Palanga": { "Vilnius": 39.24, "Kaunas": 28.4, "Klaipėda": 3.38, "Šiauliai": 17.48, "Panevėžys": 26.416, "Alytus": 34.12, "Marijampolė": 34.96, "Mažeikiai": 10.576, "Jonava": 31.36, "Utena": 43.424, "Kėdainiai": 26.48, "Tauragė": 13.888, "Telšiai": 9.5, "Ukmergė": 36, "Visaginas": 37.4, "Plungė": 6.16, "Kretinga": 1.496, "Palanga": 0, "Radviliškis": 20.124, "Šilutė": 5.928 },
        "Radviliškis": { "Vilnius": 23.04, "Kaunas": 11.916, "Klaipėda": 22.2, "Šiauliai": 2.636, "Panevėžys": 7.548, "Alytus": 17.616, "Marijampolė": 18.468, "Mažeikiai": 9.868, "Jonava": 8.964, "Utena": 21.004, "Kėdainiai": 6.316, "Tauragė": 14.628, "Telšiai": 11.004, "Ukmergė": 14.396, "Visaginas": 18.88, "Plungė": 14.092, "Kretinga": 18.964, "Palanga": 20.124, "Radviliškis": 0, "Šilutė": 15.884 },
        "Šilutė": { "Vilnius": 32.28, "Kaunas": 21.32, "Klaipėda": 4.024, "Šiauliai": 16.38, "Panevėžys": 20.052, "Alytus": 27.04, "Marijampolė": 15.044, "Mažeikiai": 11.92, "Jonava": 24.28, "Utena": 36.264, "Kėdainiai": 19.44, "Tauragė": 5.156, "Telšiai": 10.9, "Ukmergė": 28.96, "Visaginas": 43.12, "Plungė": 6.888, "Kretinga": 5.688, "Palanga": 5.928, "Radviliškis": 15.884, "Šilutė": 0 }
    }

    f = fuels[cityA][cityB]
    return f

# Miestai ir keliavimo trukmės tarp jų gauti iš Google MAPS API 
def getDuration(cityA, cityB):
    durations = {
        'Vilnius': {'Vilnius': 0, 'Kaunas': 75, 'Klaipėda': 193, 'Šiauliai': 159, 'Panevėžys': 94, 'Alytus': 89, 'Marijampolė': 111, 'Mažeikiai': 220, 'Jonava': 81, 'Utena': 77, 'Kėdainiai': 103, 'Tauragė': 155, 'Telšiai': 188, 'Ukmergė': 53, 'Visaginas': 127, 'Plungė': 185, 'Kretinga': 198, 'Palanga': 209, 'Radviliškis': 139, 'Šilutė': 204},
        'Kaunas': {'Vilnius': 77, 'Kaunas': 0, 'Klaipėda': 136, 'Šiauliai': 122, 'Panevėžys': 88, 'Alytus': 64, 'Marijampolė': 47, 'Mažeikiai': 165, 'Jonava': 32, 'Utena': 113, 'Kėdainiai': 46, 'Tauragė': 98, 
        'Telšiai': 131, 'Ukmergė': 65, 'Visaginas': 173, 'Plungė': 128, 'Kretinga': 142, 'Palanga': 152, 'Radviliškis': 101, 'Šilutė': 148},
        'Klaipėda': {'Vilnius': 197, 'Kaunas': 137, 'Klaipėda': 0, 'Šiauliai': 127, 'Panevėžys': 174, 'Alytus': 186, 'Marijampolė': 169, 'Mažeikiai': 95, 'Jonava': 151, 'Utena': 232, 'Kėdainiai': 132, 'Tauragė': 81, 'Telšiai': 74, 'Ukmergė': 184, 'Visaginas': 292, 'Plungė': 49, 'Kretinga': 29, 'Palanga': 30, 'Radviliškis': 144, 'Šilutė': 46},
        'Šiauliai': {'Vilnius': 153, 'Kaunas': 122, 'Klaipėda': 126, 'Šiauliai': 0, 'Panevėžys': 73, 'Alytus': 171, 'Marijampolė': 154, 'Mažeikiai': 66, 'Jonava': 105, 'Utena': 149, 'Kėdainiai': 80, 'Tauragė': 88, 'Telšiai': 58, 'Ukmergė': 107, 'Visaginas': 192, 'Plungė': 78, 'Kretinga': 108, 'Palanga': 118, 'Radviliškis': 23, 'Šilutė': 138},
        'Panevėžys': {'Vilnius': 96, 'Kaunas': 88, 'Klaipėda': 173, 'Šiauliai': 79, 'Panevėžys': 0, 'Alytus': 137, 'Marijampolė': 120, 'Mažeikiai': 139, 'Jonava': 70, 'Utena': 84, 'Kėdainiai': 55, 'Tauragė': 135, 'Telšiai': 132, 'Ukmergė': 50, 'Visaginas': 133, 'Plungė': 152, 'Kretinga': 179, 'Palanga': 189, 'Radviliškis': 63, 'Šilutė': 185},
        'Alytus': {'Vilnius': 89, 'Kaunas': 63, 'Klaipėda': 185, 'Šiauliai': 171, 'Panevėžys': 137, 'Alytus': 0, 'Marijampolė': 52, 'Mažeikiai': 214, 'Jonava': 79, 'Utena': 154, 'Kėdainiai': 95, 'Tauragė': 147, 'Telšiai': 180, 'Ukmergė': 111, 'Visaginas': 209, 'Plungė': 177, 'Kretinga': 191, 'Palanga': 201, 'Radviliškis': 150, 'Šilutė': 197},
        'Marijampolė': {'Vilnius': 113, 'Kaunas': 48, 'Klaipėda': 170, 'Šiauliai': 156, 'Panevėžys': 122, 'Alytus': 52, 'Marijampolė': 0, 'Mažeikiai': 199, 'Jonava': 71, 'Utena': 152, 'Kėdainiai': 80, 'Tauragė': 104, 'Telšiai': 165, 'Ukmergė': 103, 'Visaginas': 211, 'Plungė': 162, 'Kretinga': 176, 'Palanga': 186, 'Radviliškis': 135, 'Šilutė': 156},
        'Mažeikiai': {'Vilnius': 218, 'Kaunas': 167, 'Klaipėda': 95, 'Šiauliai': 66, 'Panevėžys': 138, 'Alytus': 216, 'Marijampolė': 199, 'Mažeikiai': 0, 'Jonava': 170, 'Utena': 206, 'Kėdainiai': 145, 'Tauragė': 115, 'Telšiai': 36, 'Ukmergė': 172, 'Visaginas': 255, 'Plungė': 47, 'Kretinga': 77, 'Palanga': 87, 'Radviliškis': 88, 'Šilutė': 121},
        'Jonava': {'Vilnius': 78, 'Kaunas': 32, 'Klaipėda': 150, 'Šiauliai': 104, 'Panevėžys': 70, 'Alytus': 79, 'Marijampolė': 68, 'Mažeikiai': 169, 'Jonava': 0, 'Utena': 81, 'Kėdainiai': 29, 'Tauragė': 112, 
        'Telšiai': 145, 'Ukmergė': 32, 'Visaginas': 140, 'Plungė': 142, 'Kretinga': 156, 'Palanga': 166, 'Radviliškis': 84, 'Šilutė': 161},
        'Utena': {'Vilnius': 77, 'Kaunas': 114, 'Klaipėda': 231, 'Šiauliai': 145, 'Panevėžys': 84, 'Alytus': 153, 'Marijampolė': 150, 'Mažeikiai': 205, 'Jonava': 81, 'Utena': 0, 'Kėdainiai': 104, 'Tauragė': 193, 'Telšiai': 198, 'Ukmergė': 55, 'Visaginas': 59, 'Plungė': 218, 'Kretinga': 237, 'Palanga': 247, 'Radviliškis': 135, 'Šilutė': 243},
        'Kėdainiai': {'Vilnius': 106, 'Kaunas': 47, 'Klaipėda': 130, 'Šiauliai': 80, 'Panevėžys': 56, 'Alytus': 95, 'Marijampolė': 78, 'Mažeikiai': 144, 'Jonava': 29, 'Utena': 104, 'Kėdainiai': 0, 'Tauragė': 92, 'Telšiai': 125, 'Ukmergė': 57, 'Visaginas': 164, 'Plungė': 122, 'Kretinga': 136, 'Palanga': 146, 'Radviliškis': 59, 'Šilutė': 141},
        'Tauragė': {'Vilnius': 157, 'Kaunas': 97, 'Klaipėda': 80, 'Šiauliai': 86, 'Panevėžys': 134, 'Alytus': 146, 'Marijampolė': 105, 'Mažeikiai': 113, 'Jonava': 111, 'Utena': 192, 'Kėdainiai': 92, 'Tauragė': 0, 'Telšiai': 80, 'Ukmergė': 144, 'Visaginas': 252, 'Plungė': 71, 'Kretinga': 86, 'Palanga': 96, 'Radviliškis': 103, 'Šilutė': 56},
        'Telšiai': {'Vilnius': 192, 'Kaunas': 132, 'Klaipėda': 74, 'Šiauliai': 58, 'Panevėžys': 129, 'Alytus': 181, 'Marijampolė': 164, 'Mažeikiai': 36, 'Jonava': 146, 'Utena': 198, 'Kėdainiai': 127, 'Tauragė': 81, 'Telšiai': 0, 'Ukmergė': 164, 'Visaginas': 247, 'Plungė': 26, 'Kretinga': 56, 'Palanga': 66, 'Radviliškis': 80, 'Šilutė': 100},
        'Ukmergė': {'Vilnius': 55, 'Kaunas': 65, 'Klaipėda': 183, 'Šiauliai': 115, 'Panevėžys': 50, 'Alytus': 112, 'Marijampolė': 101, 'Mažeikiai': 176, 'Jonava': 32, 'Utena': 54, 'Kėdainiai': 57, 'Tauragė': 145, 'Telšiai': 168, 'Ukmergė': 0, 'Visaginas': 113, 'Plungė': 175, 'Kretinga': 189, 'Palanga': 199, 'Radviliškis': 94, 'Šilutė': 194},
        'Visaginas': {'Vilnius': 129, 'Kaunas': 173, 'Klaipėda': 291, 'Šiauliai': 194, 'Panevėžys': 133, 'Alytus': 210, 'Marijampolė': 209, 'Mažeikiai': 255, 'Jonava': 141, 'Utena': 59, 'Kėdainiai': 164, 'Tauragė': 253, 'Telšiai': 247, 'Ukmergė': 114, 'Visaginas': 0, 'Plungė': 267, 'Kretinga': 297, 'Palanga': 307, 'Radviliškis': 187, 'Šilutė': 303},
        'Plungė': {'Vilnius': 189, 'Kaunas': 129, 'Klaipėda': 48, 'Šiauliai': 78, 'Panevėžys': 149, 'Alytus': 178, 'Marijampolė': 161, 'Mažeikiai': 46, 'Jonava': 143, 'Utena': 218, 'Kėdainiai': 123, 'Tauragė': 72, 'Telšiai': 26, 'Ukmergė': 175, 'Visaginas': 267, 'Plungė': 0, 'Kretinga': 40, 'Palanga': 50, 'Radviliškis': 100, 'Šilutė': 75},
        'Kretinga': {'Vilnius': 204, 'Kaunas': 144, 'Klaipėda': 29, 'Šiauliai': 108, 'Panevėžys': 179, 'Alytus': 193, 'Marijampolė': 176, 'Mažeikiai': 76, 'Jonava': 158, 'Utena': 239, 'Kėdainiai': 138, 'Tauragė': 88, 'Telšiai': 55, 'Ukmergė': 191, 'Visaginas': 299, 'Plungė': 39, 'Kretinga': 0, 'Palanga': 17, 'Radviliškis': 130, 'Šilutė': 64},
        'Palanga': {'Vilnius': 211, 'Kaunas': 151, 'Klaipėda': 27, 'Šiauliai': 117, 'Panevėžys': 188, 'Alytus': 200, 'Marijampolė': 183, 'Mažeikiai': 85, 'Jonava': 165, 'Utena': 246, 'Kėdainiai': 146, 'Tauragė': 95, 'Telšiai': 64, 'Ukmergė': 198, 'Visaginas': 306, 'Plungė': 48, 'Kretinga': 16, 'Palanga': 0, 'Radviliškis': 139, 'Šilutė': 61},
        'Radviliškis': {'Vilnius': 132, 'Kaunas': 101, 'Klaipėda': 141, 'Šiauliai': 23, 'Panevėžys': 52, 'Alytus': 150, 'Marijampolė': 133, 'Mažeikiai': 88, 'Jonava': 84, 'Utena': 128, 'Kėdainiai': 59, 'Tauragė': 102, 'Telšiai': 80, 'Ukmergė': 86, 'Visaginas': 181, 'Plungė': 100, 'Kretinga': 130, 'Palanga': 140, 'Radviliškis': 0, 'Šilutė': 152},
        'Šilutė': {'Vilnius': 208, 'Kaunas': 148, 'Klaipėda': 47, 'Šiauliai': 137, 'Panevėžys': 185, 'Alytus': 197, 'Marijampolė': 157, 'Mažeikiai': 121, 'Jonava': 162, 'Utena': 243, 'Kėdainiai': 142, 'Tauragė': 56, 'Telšiai': 100, 'Ukmergė': 194, 'Visaginas': 303, 'Plungė': 75, 'Kretinga': 63, 'Palanga': 63, 'Radviliškis': 155, 'Šilutė': 0}
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
    #print("Minimum cost:", final_res)
    print("Path Taken: ", path)
    totalDuration = getRouteDuration(final_cities_path)
    totalFuelCost = round(getRouteFuelCost(final_cities_path), 3)
    print("Path total duration: " + str(totalDuration) + " min")
    print("Path total fuel: " + str(totalFuelCost) + " liters")
    print("Time: " + str(executionTime) + "s")

# Main code ----------------------------------------------------------------------------------------------------------
start = tm.time()
executionTime = 0
cities = ['Vilnius', 'Kaunas', 'Klaipėda', 'Šiauliai', 'Panevėžys', 'Alytus', 'Marijampolė', 'Mažeikiai',
'Jonava', 'Utena', 'Kėdainiai', 'Tauragė', 'Telšiai', 'Ukmergė', 'Visaginas', 'Plungė', 'Kretinga', 'Palanga', 'Radviliškis', 'Šilutė']

# Fuel cost values (liters)
adj_fuel = [
	[0, 11.716, 36.32, 25.56, 16.32, 11.128, 18.8, 31.644, 9.664, 11.568, 16.52, 28.08, 30.56, 8.576, 12, 32.4, 36.16, 39.24, 23.04, 32.28], 
	[11.716, 0, 25.44, 14.388, 12.88, 6.208, 7.032, 22.96, 3.52, 15.84, 5.604, 17.24, 19.68, 8.108, 22.68, 21.56, 25.4, 28.4, 11.916, 21.32], 
	[36.32, 25.44, 0, 18.32, 24.28, 30.96, 32, 9.696, 26.64, 38.744, 23.64, 10.94, 8.588, 31.024, 45.492, 5.048, 2.384, 3.38, 22.2, 4.024], 
	[25.56, 14.388, 18.32, 0, 9.452, 20.02, 20.964, 7.228, 11.472, 23.6, 8.832, 12.28, 8.42, 16.96, 19.604, 11.424, 16.244, 17.48, 2.636, 16.38], 
	[16.32, 12.88, 24.28, 9.452, 0, 18.56, 19.36, 16.728, 9.564, 8.24, 7.312, 15.972, 17.952, 8.076, 13.28, 20.32, 25.1, 26.416, 7.548, 20.052], 
	[11.128, 6.208, 30.96, 20.02, 18.56, 0, 5.224, 28.8, 9.2, 22.6, 11.372, 22.96, 25.48, 13.78, 24.564, 27.28, 31.12, 34.12, 17.616, 27.04], 
	[18.8, 7.032, 32, 20.964, 19.36, 5.224, 0, 29.736, 11.088, 23.28, 12.224, 10.564, 26.52, 15.68, 30.24, 28.12, 31.96, 34.96, 18.468, 15.044], 
	[31.644, 22.96, 9.696, 7.228, 16.728, 28.8, 29.736, 0, 18.748, 29.664, 16.108, 11.47, 3.184, 24.264, 29.624, 4.488, 9.308, 10.576, 9.868, 11.92], 
	[9.664, 3.52, 26.64, 11.472, 9.564, 9.2, 11.088, 18.748, 0, 12.104, 2.76, 17.76, 20.208, 4.392, 18.96, 24.56, 28.36, 31.36, 8.964, 24.28], 
	[11.568, 15.84, 38.744, 23.6, 8.24, 22.6, 23.28, 29.664, 12.104, 0, 12.932, 32.6, 23.512, 7.656, 7.632, 26.352, 40.344, 43.424, 21.004, 36.264], 
	[16.52, 5.604, 23.64, 8.832, 7.312, 11.372, 12.224, 16.108, 2.76, 12.932, 0, 15.36, 17.884, 4.804, 19.388, 19.68, 23.48, 26.48, 6.316, 19.44], 
	[28.08, 17.24, 10.94, 12.28, 15.972, 22.96, 10.564, 11.47, 17.76, 32.6, 15.36, 0, 7.608, 22.704, 37.28, 6.984, 10.804, 13.888, 14.628, 5.156], 
	[30.56, 19.68, 8.588, 8.42, 17.952, 25.48, 26.52, 3.184, 20.208, 23.512, 17.884, 7.608, 0, 25.348, 28.484, 3.404, 8.228, 9.5, 11.004, 10.9], 
	[8.576, 8.108, 31.024, 16.96, 8.076, 13.78, 15.68, 24.264, 4.392, 7.656, 4.804, 22.704, 25.348, 0, 14.388, 29.2, 32.92, 36, 14.396, 28.96], 
	[12, 22.68, 45.492, 19.604, 13.28, 24.564, 30.24, 29.624, 18.96, 7.632, 19.388, 37.28, 28.484, 14.388, 0, 31.132, 36.2, 37.4, 18.88, 43.12], 
	[32.4, 21.56, 5.048, 11.424, 20.32, 27.28, 28.12, 4.488, 24.56, 26.352, 19.68, 6.984, 3.404, 29.2, 31.132, 0, 5, 6.16, 14.092, 6.888], 
	[36.16, 25.4, 2.384, 16.244, 25.1, 31.12, 31.96, 9.308, 28.36, 40.344, 23.48, 10.804, 8.228, 32.92, 36.2, 5, 0, 1.496, 18.964, 5.688], 
	[39.24, 28.4, 3.38, 17.48, 26.416, 34.12, 34.96, 10.576, 31.36, 43.424, 26.48, 13.888, 9.5, 36, 37.4, 6.16, 1.496, 0, 20.124, 5.928], 
	[23.04, 11.916, 22.2, 2.636, 7.548, 17.616, 18.468, 9.868, 8.964, 21.004, 6.316, 14.628, 11.004, 14.396, 18.88, 14.092, 18.964, 20.124, 0, 15.884], 
	[32.28, 21.32, 4.024, 16.38, 20.052, 27.04, 15.044, 11.92, 24.28, 36.264, 19.44, 5.156, 10.9, 28.96, 43.12, 6.888, 5.688, 5.928, 15.884, 0]
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

# the final path of the salesman
final_path = [None] * (N + 1)

# visited nodes in a particular path
visited = [False] * N

# Stores the final minimum weight
# of shortest tour.
final_res = maxsize

TSP(adj)

final_cities_path = convertPathToCities(final_path)
executionTime = (tm.time() - start)

printFinalResults(final_cities_path, executionTime)