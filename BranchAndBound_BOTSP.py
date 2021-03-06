# Branch and Bound algorithm for solving Traveling Salesman Problem
# Author: ┼Żygimantas Rimgaila
import math
import time as tm
maxsize = float('inf')
  
# Function to copy temporary solution
# to the final solution
def copyToFinal(final_p, curr_path):
    final_p[:N + 1] = curr_path[:]
    final_p[N] = curr_path[0]
  
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
def TSPRec(adj_fuel, adj_time, curr_bound_f, curr_bound_t, curr_weight_f, curr_weight_t, level, curr_path, visited):

    global final_res_f
    global final_res_t
    curr_res_f = 0
    curr_res_t = 0
      
    # base case is when we have reached level N 
    # which means we have covered all the nodes once
    if level == N:
          
        # check if there is an edge from
        # last vertex in path back to the first vertex
        if adj_fuel[curr_path[level - 1]][curr_path[0]] != 0:
              
            # curr_res has the total weight
            # of the solution we got
            curr_res_f = curr_weight_f + adj_fuel[curr_path[level - 1]][curr_path[0]]
            curr_res_t = curr_weight_t + adj_time[curr_path[level - 1]][curr_path[0]]
            if curr_res_f < final_res_f:
                copyToFinal(final_path_f, curr_path)
                final_res_f = curr_res_f
            if curr_res_t < final_res_t:
                copyToFinal(final_path_t, curr_path)
                final_res_t = curr_res_t
        return
  
    # for any other level iterate for all vertices
    # to build the search space tree recursively
    for i in range(N):
          
        # Consider next vertex if it is not same 
        # (diagonal entry in adjacency matrix and 
        #  not visited already)
        if (adj_fuel[curr_path[level-1]][i] != 0 and
                            visited[i] == False):
            temp_f = curr_bound_f
            temp_t = curr_bound_t
            curr_weight_f += adj_fuel[curr_path[level - 1]][i]
            curr_weight_t += adj_time[curr_path[level - 1]][i]
  
            # different computation of curr_bound 
            # for level 2 from the other levels
            if level == 1:
                curr_bound_f -= ((firstMin(adj_fuel, curr_path[level - 1]) + 
                                firstMin(adj_fuel, i)) / 2)
                curr_bound_t -= ((firstMin(adj_time, curr_path[level - 1]) + 
                                firstMin(adj_time, i)) / 2)
            else:
                curr_bound_f -= ((secondMin(adj_fuel, curr_path[level - 1]) +
                                 firstMin(adj_fuel, i)) / 2)
                curr_bound_t -= ((secondMin(adj_time, curr_path[level - 1]) +
                                 firstMin(adj_time, i)) / 2)
  
            # curr_bound + curr_weight is the actual lower bound 
            # for the node that we have arrived on.
            # If current lower bound < final_res, 
            # we need to explore the node further
            
            if curr_bound_f + curr_weight_f < final_res_f or curr_bound_t + curr_weight_t < final_res_t:
                curr_path[level] = i
                visited[i] = True
                # call TSPRec for the next level
                TSPRec(adj_fuel, adj_time, curr_bound_f, curr_bound_t, curr_weight_f, curr_weight_t, 
                       level + 1, curr_path, visited)
            
            cities = convertPathToCities(curr_path)
            #print(curr_path)
            # Else we have to prune the node by resetting 
            # all changes to curr_weight and curr_bound
            curr_weight_f -= adj_fuel[curr_path[level - 1]][i]
            curr_weight_t -= adj_time[curr_path[level - 1]][i]
            curr_bound_f = temp_f
            curr_bound_t = temp_t
  
            # Also reset the visited array
            visited = [False] * len(visited)
            for j in range(level):
                if curr_path[j] != -1:
                    visited[curr_path[j]] = True
  
# This function sets up final_path
def TSP(adj_fuel, adj_time):
      
    # Calculate initial lower bound for the root node 
    # using the formula 1/2 * (sum of first min + 
    # second min) for all edges. Also initialize the 
    # curr_path and visited array
    curr_bound_f = 0
    curr_bound_t = 0
    curr_path = [-1] * (N + 1)
    visited = [False] * N
  
    # Compute initial bound
    for i in range(N):
        curr_bound_f += (firstMin(adj_fuel, i) + secondMin(adj_fuel, i))
        curr_bound_t += (firstMin(adj_time, i) + secondMin(adj_time, i))

    # Rounding off the lower bound to an integer
    curr_bound_f = math.ceil(curr_bound_f / 2)
    curr_bound_t = math.ceil(curr_bound_t / 2)
  
    # We start at vertex 1 so the first vertex 
    # in curr_path[] is 0
    visited[0] = True
    curr_path[0] = 0
  
    # Call to TSPRec for curr_weight 
    # equal to 0 and level 1
    TSPRec(adj_fuel, adj_time, curr_bound_f, curr_bound_t, 0, 0, 1, curr_path, visited)

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
        "Vilnius": { "Vilnius": 0, "Kaunas": 8.884, "Klaip─Śda": 25.08, "┼áiauliai": 17.24, "Panev─Ś┼żys": 11.08, "Alytus": 10.672, "Marijampol─Ś": 13.4, "Ma┼żeikiai": 28.956, "Jonava": 10.236, "Utena": 7.912, "K─Śdainiai": 13.28, "Taurag─Ś": 19.52, "Tel┼íiai": 26.04, "Ukmerg─Ś": 6.064, "Visaginas": 18, "Plung─Ś": 24.6, "Kretinga": 26.24, "Palanga": 26.96, "Radvili┼íkis": 15.56, "┼áilut─Ś": 26.52 },
        "Kaunas": { "Vilnius": 8.884, "Kaunas": 0, "Klaip─Śda": 17.56, "┼áiauliai": 15.412, "Panev─Ś┼żys": 9.12, "Alytus": 8.212, "Marijampol─Ś": 5.288, "Ma┼żeikiai": 23.44, "Jonava": 2.82, "Utena": 10.96, "K─Śdainiai": 5.716, "Taurag─Ś": 11.96, "Tel┼íiai": 18.52, "Ukmerg─Ś": 5.912, "Visaginas": 17.92, "Plung─Ś": 17.04, "Kretinga": 18.8, "Palanga": 19.4, "Radvili┼íkis": 13.684, "┼áilut─Ś": 19.08 },
        "Klaip─Śda": { "Vilnius": 25.08, "Kaunas": 17.56, "Klaip─Śda": 0, "┼áiauliai": 12.48, "Panev─Ś┼żys": 23.52, "Alytus": 24.44, "Marijampol─Ś": 21.8, "Ma┼żeikiai": 12.704, "Jonava": 19.56, "Utena": 27.856, "K─Śdainiai": 17.56, "Taurag─Ś": 11.06, "Tel┼íiai": 8.612, "Ukmerg─Ś": 22.776, "Visaginas": 34.908, "Plung─Ś": 6.272, "Kretinga": 2.796, "Palanga": 2.68, "Radvili┼íkis": 16.8, "┼áilut─Ś": 6.036 },
        "┼áiauliai": { "Vilnius": 17.24, "Kaunas": 15.412, "Klaip─Śda": 12.48, "┼áiauliai": 0, "Panev─Ś┼żys": 6.548, "Alytus": 22.38, "Marijampol─Ś": 19.636, "Ma┼żeikiai": 8.772, "Jonava": 13.728, "Utena": 15.8, "K─Śdainiai": 9.768, "Taurag─Ś": 8.32, "Tel┼íiai": 5.78, "Ukmerg─Ś": 11.64, "Visaginas": 29.196, "Plung─Ś": 8.276, "Kretinga": 11.356, "Palanga": 12.12, "Radvili┼íkis": 1.884, "┼áilut─Ś": 15.42 },
        "Panev─Ś┼żys": { "Vilnius": 11.08, "Kaunas": 9.12, "Klaip─Śda": 23.52, "┼áiauliai": 6.548, "Panev─Ś┼żys": 0, "Alytus": 16.24, "Marijampol─Ś": 13.24, "Ma┼żeikiai": 15.672, "Jonava": 8.036, "Utena": 12.36, "K─Śdainiai": 5.488, "Taurag─Ś": 17.828, "Tel┼íiai": 12.448, "Ukmerg─Ś": 5.724, "Visaginas": 19.92, "Plung─Ś": 18.48, "Kretinga": 21.5, "Palanga": 22.384, "Radvili┼íkis": 5.752, "┼áilut─Ś": 24.948 },
        "Alytus": { "Vilnius": 10.672, "Kaunas": 8.212, "Klaip─Śda": 24.44, "┼áiauliai": 22.38, "Panev─Ś┼żys": 16.24, "Alytus": 0, "Marijampol─Ś": 5.916, "Ma┼żeikiai": 30.6, "Jonava": 10.56, "Utena": 18.2, "K─Śdainiai": 12.828, "Taurag─Ś": 19.04, "Tel┼íiai": 25.72, "Ukmerg─Ś": 13.62, "Visaginas": 29.236, "Plung─Ś": 24.12, "Kretinga": 25.88, "Palanga": 26.48, "Radvili┼íkis": 20.784, "┼áilut─Ś": 26.16 },
        "Marijampol─Ś": { "Vilnius": 13.4, "Kaunas": 5.288, "Klaip─Śda": 21.8, "┼áiauliai": 19.636, "Panev─Ś┼żys": 13.24, "Alytus": 5.916, "Marijampol─Ś": 0, "Ma┼żeikiai": 27.664, "Jonava": 7.712, "Utena": 15.72, "K─Śdainiai": 9.976, "Taurag─Ś": 14.636, "Tel┼íiai": 22.68, "Ukmerg─Ś": 10.72, "Visaginas": 22.76, "Plung─Ś": 21.28, "Kretinga": 23.04, "Palanga": 23.64, "Radvili┼íkis": 17.932, "┼áilut─Ś": 21.356 },
        "Ma┼żeikiai": { "Vilnius": 28.956, "Kaunas": 23.44, "Klaip─Śda": 12.704, "┼áiauliai": 8.772, "Panev─Ś┼żys": 15.672, "Alytus": 30.6, "Marijampol─Ś": 27.664, "Ma┼żeikiai": 0, "Jonava": 22.852, "Utena": 23.136, "K─Śdainiai": 18.892, "Taurag─Ś": 17.13, "Tel┼íiai": 4.776, "Ukmerg─Ś": 20.736, "Visaginas": 35.776, "Plung─Ś": 6.732, "Kretinga": 9.812, "Palanga": 10.624, "Radvili┼íkis": 10.932, "┼áilut─Ś": 17.88 },
        "Jonava": { "Vilnius": 10.236, "Kaunas": 2.82, "Klaip─Śda": 19.56, "┼áiauliai": 13.728, "Panev─Ś┼żys": 8.036, "Alytus": 10.56, "Marijampol─Ś": 7.712, "Ma┼żeikiai": 22.852, "Jonava": 0, "Utena": 8.296, "K─Śdainiai": 4.14, "Taurag─Ś": 15.44, "Tel┼íiai": 21.992, "Ukmerg─Ś": 3.228, "Visaginas": 15.24, "Plung─Ś": 18.64, "Kretinga": 20.44, "Palanga": 21.04, "Radvili┼íkis": 12.036, "┼áilut─Ś": 20.72 },
        "Utena": { "Vilnius": 7.912, "Kaunas": 10.96, "Klaip─Śda": 27.856, "┼áiauliai": 15.8, "Panev─Ś┼żys": 12.36, "Alytus": 18.2, "Marijampol─Ś": 15.72, "Ma┼żeikiai": 23.136, "Jonava": 8.296, "Utena": 0, "K─Śdainiai": 12.268, "Taurag─Ś": 21.8, "Tel┼íiai": 27.488, "Ukmerg─Ś": 5.184, "Visaginas": 6.668, "Plung─Ś": 29.448, "Kretinga": 28.856, "Palanga": 29.576, "Radvili┼íkis": 14.596, "┼áilut─Ś": 29.136 },
        "K─Śdainiai": { "Vilnius": 13.28, "Kaunas": 5.716, "Klaip─Śda": 17.56, "┼áiauliai": 9.768, "Panev─Ś┼żys": 5.488, "Alytus": 12.828, "Marijampol─Ś": 9.976, "Ma┼żeikiai": 18.892, "Jonava": 4.14, "Utena": 12.268, "K─Śdainiai": 0, "Taurag─Ś": 11.84, "Tel┼íiai": 18.516, "Ukmerg─Ś": 6.976, "Visaginas": 18.612, "Plung─Ś": 16.92, "Kretinga": 18.72, "Palanga": 19.32, "Radvili┼íkis": 8.064, "┼áilut─Ś": 18.96 },
        "Taurag─Ś": { "Vilnius": 19.52, "Kaunas": 11.96, "Klaip─Śda": 11.06, "┼áiauliai": 8.32, "Panev─Ś┼żys": 17.828, "Alytus": 19.04, "Marijampol─Ś": 14.636, "Ma┼żeikiai": 17.13, "Jonava": 15.44, "Utena": 21.8, "K─Śdainiai": 11.84, "Taurag─Ś": 0, "Tel┼íiai": 11.412, "Ukmerg─Ś": 17.096, "Visaginas": 29.12, "Plung─Ś": 10.476, "Kretinga": 12.196, "Palanga": 12.912, "Radvili┼íkis": 10.372, "┼áilut─Ś": 7.184 },
        "Tel┼íiai": { "Vilnius": 26.04, "Kaunas": 18.52, "Klaip─Śda": 8.612, "┼áiauliai": 5.78, "Panev─Ś┼żys": 12.448, "Alytus": 25.72, "Marijampol─Ś": 22.68, "Ma┼żeikiai": 4.776, "Jonava": 21.992, "Utena": 27.488, "K─Śdainiai": 18.516, "Taurag─Ś": 11.412, "Tel┼íiai": 0, "Ukmerg─Ś": 17.652, "Visaginas": 35.116, "Plung─Ś": 2.656, "Kretinga": 5.752, "Palanga": 6.56, "Radvili┼íkis": 7.916, "┼áilut─Ś": 13.9 },
        "Ukmerg─Ś": { "Vilnius": 6.064, "Kaunas": 5.912, "Klaip─Śda": 22.776, "┼áiauliai": 11.64, "Panev─Ś┼żys": 5.724, "Alytus": 13.62, "Marijampol─Ś": 10.72, "Ma┼żeikiai": 20.736, "Jonava": 3.228, "Utena": 5.184, "K─Śdainiai": 6.976, "Taurag─Ś": 17.096, "Tel┼íiai": 17.652, "Ukmerg─Ś": 0, "Visaginas": 12.012, "Plung─Ś": 21.8, "Kretinga": 23.48, "Palanga": 24.2, "Radvili┼íkis": 10.404, "┼áilut─Ś": 23.84 },
        "Visaginas": { "Vilnius": 18, "Kaunas": 17.92, "Klaip─Śda": 34.908, "┼áiauliai": 29.196, "Panev─Ś┼żys": 19.92, "Alytus": 29.236, "Marijampol─Ś": 22.76, "Ma┼żeikiai": 35.776, "Jonava": 15.24, "Utena": 6.668, "K─Śdainiai": 18.612, "Taurag─Ś": 29.12, "Tel┼íiai": 35.116, "Ukmerg─Ś": 12.012, "Visaginas": 0, "Plung─Ś": 37.268, "Kretinga": 40.2, "Palanga": 41, "Radvili┼íkis": 28.32, "┼áilut─Ś": 36.08 },
        "Plung─Ś": { "Vilnius": 24.6, "Kaunas": 17.04, "Klaip─Śda": 6.272, "┼áiauliai": 8.276, "Panev─Ś┼żys": 18.48, "Alytus": 24.12, "Marijampol─Ś": 21.28, "Ma┼żeikiai": 6.732, "Jonava": 18.64, "Utena": 29.448, "K─Śdainiai": 16.92, "Taurag─Ś": 10.476, "Tel┼íiai": 2.656, "Ukmerg─Ś": 21.8, "Visaginas": 37.268, "Plung─Ś": 0, "Kretinga": 3.72, "Palanga": 4.66, "Radvili┼íkis": 10.108, "┼áilut─Ś": 10.332 },
        "Kretinga": { "Vilnius": 26.24, "Kaunas": 18.8, "Klaip─Śda": 2.796, "┼áiauliai": 11.356, "Panev─Ś┼żys": 21.5, "Alytus": 25.88, "Marijampol─Ś": 23.04, "Ma┼żeikiai": 9.812, "Jonava": 20.44, "Utena": 28.856, "K─Śdainiai": 18.72, "Taurag─Ś": 12.196, "Tel┼íiai": 5.752, "Ukmerg─Ś": 23.48, "Visaginas": 40.2, "Plung─Ś": 3.72, "Kretinga": 0, "Palanga": 1.204, "Radvili┼íkis": 13.236, "┼áilut─Ś": 8.532 },
        "Palanga": { "Vilnius": 26.96, "Kaunas": 19.4, "Klaip─Śda": 2.68, "┼áiauliai": 12.12, "Panev─Ś┼żys": 22.384, "Alytus": 26.48, "Marijampol─Ś": 23.64, "Ma┼żeikiai": 10.624, "Jonava": 21.04, "Utena": 29.576, "K─Śdainiai": 19.32, "Taurag─Ś": 12.912, "Tel┼íiai": 6.56, "Ukmerg─Ś": 24.2, "Visaginas": 41, "Plung─Ś": 4.66, "Kretinga": 1.204, "Palanga": 0, "Radvili┼íkis": 13.876, "┼áilut─Ś": 8.892 },
        "Radvili┼íkis": { "Vilnius": 15.56, "Kaunas": 13.684, "Klaip─Śda": 16.8, "┼áiauliai": 1.884, "Panev─Ś┼żys": 5.752, "Alytus": 20.784, "Marijampol─Ś": 17.932, "Ma┼żeikiai": 10.932, "Jonava": 12.036, "Utena": 14.596, "K─Śdainiai": 8.064, "Taurag─Ś": 10.372, "Tel┼íiai": 7.916, "Ukmerg─Ś": 10.404, "Visaginas": 28.32, "Plung─Ś": 10.108, "Kretinga": 13.236, "Palanga": 13.876, "Radvili┼íkis": 0, "┼áilut─Ś": 18.916 },
        "┼áilut─Ś": { "Vilnius": 26.52, "Kaunas": 19.08, "Klaip─Śda": 6.036, "┼áiauliai": 15.42, "Panev─Ś┼żys": 24.948, "Alytus": 26.16, "Marijampol─Ś": 21.356, "Ma┼żeikiai": 17.88, "Jonava": 20.72, "Utena": 29.136, "K─Śdainiai": 18.96, "Taurag─Ś": 7.184, "Tel┼íiai": 13.9, "Ukmerg─Ś": 23.84, "Visaginas": 36.08, "Plung─Ś": 10.332, "Kretinga": 8.532, "Palanga": 8.892, "Radvili┼íkis": 18.916, "┼áilut─Ś": 0 }
    }

    f = fuels[cityA][cityB]
    return f

def getDuration(cityA, cityB):
    durations = {
        "Vilnius": { "Vilnius": 0, "Kaunas": 75, "Klaip─Śda": 193, "┼áiauliai": 159, "Panev─Ś┼żys": 94, "Alytus": 89, "Marijampol─Ś": 111, "Ma┼żeikiai": 220, "Jonava": 81, "Utena": 77, "K─Śdainiai": 103, "Taurag─Ś": 155, "Tel┼íiai": 188, "Ukmerg─Ś": 53, "Visaginas": 127, "Plung─Ś": 185, "Kretinga": 198, "Palanga": 209, "Radvili┼íkis": 139, "┼áilut─Ś": 204 },
        "Kaunas": { "Vilnius": 77, "Kaunas": 0, "Klaip─Śda": 136, "┼áiauliai": 122, "Panev─Ś┼żys": 88, "Alytus": 64, "Marijampol─Ś": 47, "Ma┼żeikiai": 165, "Jonava": 32, "Utena": 113, "K─Śdainiai": 46, "Taurag─Ś": 98, "Tel┼íiai": 131, "Ukmerg─Ś": 65, "Visaginas": 173, "Plung─Ś": 128, "Kretinga": 142, "Palanga": 152, "Radvili┼íkis": 101, "┼áilut─Ś": 148 },
        "Klaip─Śda": { "Vilnius": 197, "Kaunas": 137, "Klaip─Śda": 0, "┼áiauliai": 127, "Panev─Ś┼żys": 174, "Alytus": 186, "Marijampol─Ś": 169, "Ma┼żeikiai": 95, "Jonava": 151, "Utena": 232, "K─Śdainiai": 132, "Taurag─Ś": 81, "Tel┼íiai": 74, "Ukmerg─Ś": 184, "Visaginas": 292, "Plung─Ś": 49, "Kretinga": 29, "Palanga": 30, "Radvili┼íkis": 144, "┼áilut─Ś": 46 },
        "┼áiauliai": { "Vilnius": 153, "Kaunas": 122, "Klaip─Śda": 126, "┼áiauliai": 0, "Panev─Ś┼żys": 73, "Alytus": 171, "Marijampol─Ś": 154, "Ma┼żeikiai": 66, "Jonava": 105, "Utena": 149, "K─Śdainiai": 80, "Taurag─Ś": 88, "Tel┼íiai": 58, "Ukmerg─Ś": 107, "Visaginas": 192, "Plung─Ś": 78, "Kretinga": 108, "Palanga": 118, "Radvili┼íkis": 23, "┼áilut─Ś": 138 },
        "Panev─Ś┼żys": { "Vilnius": 96, "Kaunas": 88, "Klaip─Śda": 173, "┼áiauliai": 79, "Panev─Ś┼żys": 0, "Alytus": 137, "Marijampol─Ś": 120, "Ma┼żeikiai": 139, "Jonava": 70, "Utena": 84, "K─Śdainiai": 55, "Taurag─Ś": 135, "Tel┼íiai": 132, "Ukmerg─Ś": 50, "Visaginas": 133, "Plung─Ś": 152, "Kretinga": 179, "Palanga": 189, "Radvili┼íkis": 63, "┼áilut─Ś": 185 },
        "Alytus": { "Vilnius": 89, "Kaunas": 63, "Klaip─Śda": 185, "┼áiauliai": 171, "Panev─Ś┼żys": 137, "Alytus": 0, "Marijampol─Ś": 52, "Ma┼żeikiai": 214, "Jonava": 79, "Utena": 154, "K─Śdainiai": 95, "Taurag─Ś": 147, "Tel┼íiai": 180, "Ukmerg─Ś": 111, "Visaginas": 209, "Plung─Ś": 177, "Kretinga": 191, "Palanga": 201, "Radvili┼íkis": 150, "┼áilut─Ś": 197 },
        "Marijampol─Ś": { "Vilnius": 113, "Kaunas": 48, "Klaip─Śda": 170, "┼áiauliai": 156, "Panev─Ś┼żys": 122, "Alytus": 52, "Marijampol─Ś": 0, "Ma┼żeikiai": 199, "Jonava": 71, "Utena": 152, "K─Śdainiai": 80, "Taurag─Ś": 104, "Tel┼íiai": 165, "Ukmerg─Ś": 103, "Visaginas": 211, "Plung─Ś": 162, "Kretinga": 176, "Palanga": 186, "Radvili┼íkis": 135, "┼áilut─Ś": 156 },
        "Ma┼żeikiai": { "Vilnius": 218, "Kaunas": 167, "Klaip─Śda": 95, "┼áiauliai": 66, "Panev─Ś┼żys": 138, "Alytus": 216, "Marijampol─Ś": 199, "Ma┼żeikiai": 0, "Jonava": 170, "Utena": 206, "K─Śdainiai": 145, "Taurag─Ś": 115, "Tel┼íiai": 36, "Ukmerg─Ś": 172, "Visaginas": 255, "Plung─Ś": 47, "Kretinga": 77, "Palanga": 87, "Radvili┼íkis": 88, "┼áilut─Ś": 121 },
        "Jonava": { "Vilnius": 78, "Kaunas": 32, "Klaip─Śda": 150, "┼áiauliai": 104, "Panev─Ś┼żys": 70, "Alytus": 79, "Marijampol─Ś": 68, "Ma┼żeikiai": 169, "Jonava": 0, "Utena": 81, "K─Śdainiai": 29, "Taurag─Ś": 112, "Tel┼íiai": 145, "Ukmerg─Ś": 32, "Visaginas": 140, "Plung─Ś": 142, "Kretinga": 156, "Palanga": 166, "Radvili┼íkis": 84, "┼áilut─Ś": 161 },
        "Utena": { "Vilnius": 77, "Kaunas": 114, "Klaip─Śda": 231, "┼áiauliai": 145, "Panev─Ś┼żys": 84, "Alytus": 153, "Marijampol─Ś": 150, "Ma┼żeikiai": 205, "Jonava": 81, "Utena": 0, "K─Śdainiai": 104, "Taurag─Ś": 193, "Tel┼íiai": 198, "Ukmerg─Ś": 55, "Visaginas": 59, "Plung─Ś": 218, "Kretinga": 237, "Palanga": 247, "Radvili┼íkis": 135, "┼áilut─Ś": 243 },
        "K─Śdainiai": { "Vilnius": 106, "Kaunas": 47, "Klaip─Śda": 130, "┼áiauliai": 80, "Panev─Ś┼żys": 56, "Alytus": 95, "Marijampol─Ś": 78, "Ma┼żeikiai": 144, "Jonava": 29, "Utena": 104, "K─Śdainiai": 0, "Taurag─Ś": 92, "Tel┼íiai": 125, "Ukmerg─Ś": 57, "Visaginas": 164, "Plung─Ś": 122, "Kretinga": 136, "Palanga": 146, "Radvili┼íkis": 59, "┼áilut─Ś": 141 },
        "Taurag─Ś": { "Vilnius": 157, "Kaunas": 97, "Klaip─Śda": 80, "┼áiauliai": 86, "Panev─Ś┼żys": 134, "Alytus": 146, "Marijampol─Ś": 105, "Ma┼żeikiai": 113, "Jonava": 111, "Utena": 192, "K─Śdainiai": 92, "Taurag─Ś": 0, "Tel┼íiai": 80, "Ukmerg─Ś": 144, "Visaginas": 252, "Plung─Ś": 71, "Kretinga": 86, "Palanga": 96, "Radvili┼íkis": 103, "┼áilut─Ś": 56 },
        "Tel┼íiai": { "Vilnius": 192, "Kaunas": 132, "Klaip─Śda": 74, "┼áiauliai": 58, "Panev─Ś┼żys": 129, "Alytus": 181, "Marijampol─Ś": 164, "Ma┼żeikiai": 36, "Jonava": 146, "Utena": 198, "K─Śdainiai": 127, "Taurag─Ś": 81, "Tel┼íiai": 0, "Ukmerg─Ś": 164, "Visaginas": 247, "Plung─Ś": 26, "Kretinga": 56, "Palanga": 66, "Radvili┼íkis": 80, "┼áilut─Ś": 100 },
        "Ukmerg─Ś": { "Vilnius": 55, "Kaunas": 65, "Klaip─Śda": 183, "┼áiauliai": 115, "Panev─Ś┼żys": 50, "Alytus": 112, "Marijampol─Ś": 101, "Ma┼żeikiai": 176, "Jonava": 32, "Utena": 54, "K─Śdainiai": 57, "Taurag─Ś": 145, "Tel┼íiai": 168, "Ukmerg─Ś": 0, "Visaginas": 113, "Plung─Ś": 175, "Kretinga": 189, "Palanga": 199, "Radvili┼íkis": 94, "┼áilut─Ś": 194 },
        "Visaginas": { "Vilnius": 129, "Kaunas": 173, "Klaip─Śda": 291, "┼áiauliai": 194, "Panev─Ś┼żys": 133, "Alytus": 210, "Marijampol─Ś": 209, "Ma┼żeikiai": 255, "Jonava": 141, "Utena": 59, "K─Śdainiai": 164, "Taurag─Ś": 253, "Tel┼íiai": 247, "Ukmerg─Ś": 114, "Visaginas": 0, "Plung─Ś": 267, "Kretinga": 297, "Palanga": 307, "Radvili┼íkis": 187, "┼áilut─Ś": 303 },
        "Plung─Ś": { "Vilnius": 189, "Kaunas": 129, "Klaip─Śda": 48, "┼áiauliai": 78, "Panev─Ś┼żys": 149, "Alytus": 178, "Marijampol─Ś": 161, "Ma┼żeikiai": 46, "Jonava": 143, "Utena": 218, "K─Śdainiai": 123, "Taurag─Ś": 72, "Tel┼íiai": 26, "Ukmerg─Ś": 175, "Visaginas": 267, "Plung─Ś": 0, "Kretinga": 40, "Palanga": 50, "Radvili┼íkis": 100, "┼áilut─Ś": 75 },
        "Kretinga": { "Vilnius": 204, "Kaunas": 144, "Klaip─Śda": 29, "┼áiauliai": 108, "Panev─Ś┼żys": 179, "Alytus": 193, "Marijampol─Ś": 176, "Ma┼żeikiai": 76, "Jonava": 158, "Utena": 239, "K─Śdainiai": 138, "Taurag─Ś": 88, "Tel┼íiai": 55, "Ukmerg─Ś": 191, "Visaginas": 299, "Plung─Ś": 39, "Kretinga": 0, "Palanga": 17, "Radvili┼íkis": 130, "┼áilut─Ś": 64 },
        "Palanga": { "Vilnius": 211, "Kaunas": 151, "Klaip─Śda": 27, "┼áiauliai": 117, "Panev─Ś┼żys": 188, "Alytus": 200, "Marijampol─Ś": 183, "Ma┼żeikiai": 85, "Jonava": 165, "Utena": 246, "K─Śdainiai": 146, "Taurag─Ś": 95, "Tel┼íiai": 64, "Ukmerg─Ś": 198, "Visaginas": 306, "Plung─Ś": 48, "Kretinga": 16, "Palanga": 0, "Radvili┼íkis": 139, "┼áilut─Ś": 61 },
        "Radvili┼íkis": { "Vilnius": 132, "Kaunas": 101, "Klaip─Śda": 141, "┼áiauliai": 23, "Panev─Ś┼żys": 52, "Alytus": 150, "Marijampol─Ś": 133, "Ma┼żeikiai": 88, "Jonava": 84, "Utena": 128, "K─Śdainiai": 59, "Taurag─Ś": 102, "Tel┼íiai": 80, "Ukmerg─Ś": 86, "Visaginas": 181, "Plung─Ś": 100, "Kretinga": 130, "Palanga": 140, "Radvili┼íkis": 0, "┼áilut─Ś": 152 },
        "┼áilut─Ś": { "Vilnius": 208, "Kaunas": 148, "Klaip─Śda": 47, "┼áiauliai": 137, "Panev─Ś┼żys": 185, "Alytus": 197, "Marijampol─Ś": 157, "Ma┼żeikiai": 121, "Jonava": 162, "Utena": 243, "K─Śdainiai": 142, "Taurag─Ś": 56, "Tel┼íiai": 100, "Ukmerg─Ś": 194, "Visaginas": 303, "Plung─Ś": 75, "Kretinga": 63, "Palanga": 63, "Radvili┼íkis": 155, "┼áilut─Ś": 0 }
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

def printFinalResults(path_f, path_t, executionTime):
    print("Path taken: ", path_f)
    totalDuration = getRouteDuration(final_cities_path_f)
    totalFuelCost = round(getRouteFuelCost(final_cities_path_f), 3)
    print("Path total duration: " + str(totalDuration) + " min")
    print("Path total fuel: " + str(totalFuelCost) + " liters")
    print("Path taken: ", path_t)
    totalDuration = getRouteDuration(final_cities_path_t)
    totalFuelCost = round(getRouteFuelCost(final_cities_path_t), 3)
    print("Path total duration: " + str(totalDuration) + " min")
    print("Path total fuel: " + str(totalFuelCost) + " liters")
    print("Time: " + str(executionTime) + "s")

# Main code

start = tm.time()
executionTime = 0
cities = ['Vilnius', 'Kaunas', 'Klaip─Śda', '┼áiauliai', 'Panev─Ś┼żys', 'Alytus', 'Marijampol─Ś', 'Ma┼żeikiai',
'Jonava', 'Utena', 'K─Śdainiai', 'Taurag─Ś', 'Tel┼íiai', 'Ukmerg─Ś', 'Visaginas', 'Plung─Ś', 'Kretinga']

# Fuel cost values (liters)
adj_fuel = [
	[0, 8.884, 25.08, 17.24, 11.08, 10.672, 13.4, 28.956, 10.236, 7.912, 13.28, 19.52, 26.04, 6.064, 18, 24.6, 26.24],
	[8.884, 0, 17.56, 15.412, 9.12, 8.212, 5.288, 23.44, 2.82, 10.96, 5.716, 11.96, 18.52, 5.912, 17.92, 17.04, 18.8],
	[25.08, 17.56, 0, 12.48, 23.52, 24.44, 21.8, 12.704, 19.56, 27.856, 17.56, 11.06, 8.612, 22.776, 34.908, 6.272, 2.796],
	[17.24, 15.412, 12.48, 0, 6.548, 22.38, 19.636, 8.772, 13.728, 15.8, 9.768, 8.32, 5.78, 11.64, 29.196, 8.276, 11.356],
	[11.08, 9.12, 23.52, 6.548, 0, 16.24, 13.24, 15.672, 8.036, 12.36, 5.488, 17.828, 12.448, 5.724, 19.92, 18.48, 21.5], 
	[10.672, 8.212, 24.44, 22.38, 16.24, 0, 5.916, 30.6, 10.56, 18.2, 12.828, 19.04, 25.72, 13.62, 29.236, 24.12, 25.88],
	[13.4, 5.288, 21.8, 19.636, 13.24, 5.916, 0, 27.664, 7.712, 15.72, 9.976, 14.636, 22.68, 10.72, 22.76, 21.28, 23.04],
	[28.956, 23.44, 12.704, 8.772, 15.672, 30.6, 27.664, 0, 22.852, 23.136, 18.892, 17.13, 4.776, 20.736, 35.776, 6.732, 9.812],
	[10.236, 2.82, 19.56, 13.728, 8.036, 10.56, 7.712, 22.852, 0, 8.296, 4.14, 15.44, 21.992, 3.228, 15.24, 18.64, 20.44],
	[7.912, 10.96, 27.856, 15.8, 12.36, 18.2, 15.72, 23.136, 8.296, 0, 12.268, 21.8, 27.488, 5.184, 6.668, 29.448, 28.856],
	[13.28, 5.716, 17.56, 9.768, 5.488, 12.828, 9.976, 18.892, 4.14, 12.268, 0, 11.84, 18.516, 6.976, 18.612, 16.92, 18.72], 
	[19.52, 11.96, 11.06, 8.32, 17.828, 19.04, 14.636, 17.13, 15.44, 21.8, 11.84, 0, 11.412, 17.096, 29.12, 10.476, 12.196],
	[26.04, 18.52, 8.612, 5.78, 12.448, 25.72, 22.68, 4.776, 21.992, 27.488, 18.516, 11.412, 0, 17.652, 35.116, 2.656, 5.752],
	[6.064, 5.912, 22.776, 11.64, 5.724, 13.62, 10.72, 20.736, 3.228, 5.184, 6.976, 17.096, 17.652, 0, 12.012, 21.8, 23.48],
	[18, 17.92, 34.908, 29.196, 19.92, 29.236, 22.76, 35.776, 15.24, 6.668, 18.612, 29.12, 35.116, 12.012, 0, 37.268, 40.2],
	[24.6, 17.04, 6.272, 8.276, 18.48, 24.12, 21.28, 6.732, 18.64, 29.448, 16.92, 10.476, 2.656, 21.8, 37.268, 0, 3.72],
	[26.24, 18.8, 2.796, 11.356, 21.5, 25.88, 23.04, 9.812, 20.44, 28.856, 18.72, 12.196, 5.752, 23.48, 40.2, 3.72, 0] 
]

# Traveling time values (min)
adj_time = [
	[0, 75, 193, 159, 94, 89, 111, 220, 81, 77, 103, 155, 188, 53, 127, 185, 198],
	[77, 0, 136, 122, 88, 64, 47, 165, 32, 113, 46, 98, 131, 65, 173, 128, 142],
	[197, 137, 0, 127, 174, 186, 169, 95, 151, 232, 132, 81, 74, 184, 292, 49, 29],
	[153, 122, 126, 0, 73, 171, 154, 66, 105, 149, 80, 88, 58, 107, 192, 78, 108],
	[96, 88, 173, 79, 0, 137, 120, 139, 70, 84, 55, 135, 132, 50, 133, 152, 179], 
	[89, 63, 185, 171, 137, 0, 52, 214, 79, 154, 95, 147, 180, 111, 209, 177, 191],
	[113, 48, 170, 156, 122, 52, 0, 199, 71, 152, 80, 104, 165, 103, 211, 162, 176],
	[218, 167, 95, 66, 138, 216, 199, 0, 170, 206, 145, 115, 36, 172, 255, 47, 77],
	[78, 32, 150, 104, 70, 79, 68, 169, 0, 81, 29, 112, 145, 32, 140, 142, 156],
	[77, 114, 231, 145, 84, 153, 150, 205, 81, 0, 104, 193, 198, 55, 59, 218, 237],
	[106, 47, 130, 80, 56, 95, 78, 144, 29, 104, 0, 92, 125, 57, 164, 122, 136],
	[157, 97, 80, 86, 134, 146, 105, 113, 111, 192, 92, 0, 80, 144, 252, 71, 86],
	[192, 132, 74, 58, 129, 181, 164, 36, 146, 198, 127, 81, 0, 164, 247, 26, 56], 
	[55, 65, 183, 115, 50, 112, 101, 176, 32, 54, 57, 145, 168, 0, 113, 175, 189],
	[129, 173, 291, 194, 133, 210, 209, 255, 141, 59, 164, 253, 247, 114, 0, 267, 297],
	[189, 129, 48, 78, 149, 178, 161, 46, 143, 218, 123, 72, 26, 175, 267, 0, 40],
	[204, 144, 29, 108, 179, 193, 176, 76, 158, 239, 138, 88, 55, 191, 299, 39, 0]
]

# adj = normalizedValues(adj_fuel, adj_time)

N = 17

final_path_f = [None] * (N + 1)
final_path_t = [None] * (N + 1)

visited = [False] * N

final_res_f = maxsize
final_res_t = maxsize

TSP(adj_fuel, adj_time)

final_cities_path_f = convertPathToCities(final_path_f)
final_cities_path_t = convertPathToCities(final_path_t)
executionTime = (tm.time() - start)

printFinalResults(final_cities_path_f, final_cities_path_t, executionTime)