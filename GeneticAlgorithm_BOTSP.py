# Genetic Algorithm for solving bicriteric Travel Salesman Problem
# Author: Žygimantas Rimgaila
import pandas as pd
import array as arr
import string
import random
import math
import matplotlib.pyplot as plt
from random import randint
from random import choice
from random import shuffle
import requests
import json
import time as tm

class DNA:
    def __init__(self):
        self.genes = []
    
    def create(self, coords):
        newCoords = coords[:]
        newCoords.pop(0)
        newCoords.pop()
        random.shuffle(newCoords)
        newCoords.insert(0, 'Vilnius')
        newCoords.insert(len(newCoords), 'Vilnius')
        return newCoords
    
    def createFirstGene(self):
        data = """Vilnius, Kaunas, Klaipėda, Šiauliai, Panevėžys, Alytus, Marijampolė, Mažeikiai, Jonava, Utena, Kėdainiai, Tauragė, Telšiai, Ukmergė, Visaginas, Plungė, Kretinga, Vilnius"""
        self.genes = data.split(", ")
        return self.genes
 
    def crossover(self, parent1, parent2, rate):
        child = []
        childP1 = []
        childP2 = []
        if(random.random() < rate):
            parent1 = parent1[1:len(parent1)-1]
            parent2 = parent2[1:len(parent2)-1]
            geneA = int(random.random() * len(parent1))
            geneB = int(random.random() * len(parent1))
            startGene = min(geneA, geneB)
            endGene = max(geneA, geneB)
            childP1.append("Vilnius")
            for i in range(startGene, endGene):
                childP1.append(parent1[i])
            childP2 = [item for item in parent2 if item not in childP1]
            childP2.append("Vilnius")
            child = childP1 + childP2
        else:
            child = choice([parent1, parent1])
        return child
    
    def mutate(self, child, mutationRate):
        for i in range(len(child)):
            if(random.random() < mutationRate):
                x = randint(1,len(child)-2)
                y = choice([i for i in range(1,len(child)-2) if i!=x])
                temp = child[x]
                child[x] = child[y]
                child[y] = temp
        return child

class Population:
    def __init__(self, populationSize, mutationRate, crossoverRate):
        self.populationSize = populationSize
        self.mutationRate = mutationRate
        self.crossoverRate = crossoverRate
        self.nicheSize = 1
        self.dna = DNA()
        self.popFit = 0
        self.fit = []
        self.smallest = [1,1]
        self.biggest = [0,0]

    def create(self):
        self.population = []
        coords = self.dna.createFirstGene()
        for i in range(self.populationSize):
            self.population.append(self.dna.create(coords))
        return self.population
   
    def get_time(self, start, stop):
        api = "private-api-key" 
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + start + "&destinations=" + stop + "&key=" + api
        link = requests.get(url)
        json_loc = link.json()
        d = json_loc['rows'][0]['elements'][0]['distance']['value']
        return d
    
    # Miestai ir kuro sąnaudos gauti iš Google MAPS API 
    def getFuel(self, cityA, cityB):
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

    # Miestai ir keliavimo trukmės tarp jų gauti iš Google MAPS API 
    def getDuration(self, cityA, cityB):
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

    def calculateRouteDistances(self):
        fuels = []
        for i in range(self.populationSize):
            dist = []
            for j in range(len(self.population[i])-1):
                city_a = self.population[i][j]
                city_b = self.population[i][j+1]
                d = self.getFuel(city_a,city_b)
                dist.append(d)
            fuels.append(sum(dist))
        return fuels

    def fitnessEvaluation(self):
        f = []
        f1 = []
        self.fit = []
        
        # 3.1 Priskiriamas rangas kiekvienam sprendiniui
        p = self.getPopulationWithValues()
        self.ranks = self.ranking(p)

        # 3.2. Priskiriama tinkamumo reikšmė kiekvienam sprendiniui pagal jo rangą
        N = len(self.ranks)
        for i in range(len(self.ranks)):  
            suma = 0
            for k in range(self.ranks[i]):
                n_k = self.solutionsCount(k)
                suma += n_k
            f.append(N - suma - 0.5*(self.solutionsCount(self.ranks[i])-1))

        # nišos skaičius
        nc = self.nicheCount(p)

        for i in range(len(self.ranks)):
            f1.append(f[i]/nc[i])

        self.fit = self.normalizingFitness(f, f1)

        for i in range(len(self.fit)):
            if self.fit[i] > 1:
                print("ranks", self.ranks)
                print("fit", self.fit)
                print("something wrong with fitness probabilities")

        return self.fit

    def naturalSelection(self):
        matingPool = []
        f = 0
        for i in range(len(self.population)):
            f = self.fit[i]
            if f>0.5:
                n = int(f*100)
            else: n = int(f*30)
            for j in range(n):
                matingPool.append(self.population[i])
        return matingPool
                
    def reproduction(self, matingPool):
        length = len(self.population)
        self.population = []
        for i in range(length):
            a = int(random.randrange(len(matingPool)))
            b = int(random.randrange(len(matingPool)))
            partnerA = matingPool[a]
            partnerB = matingPool[b]
            child = self.dna.crossover(partnerA, partnerB, self.crossoverRate)
            mutatedChild = self.dna.mutate(child, self.mutationRate)
            self.population.append(child)

    def solutionsCount(self, k):
        count = 0
        for i in range(len(self.ranks)):
            if k == self.ranks[i]:
                count += 1
        return count

    def ranking(self, p):
        ranks = []
        value = []
        for i in range(len(p)):
            value.append([p[i][0],p[i][1]])
        for i in range(len(p)):
            ranks.append(2+self.domSolutions(value,i))
        return ranks

    def getPopulationWithValues(self):
        p = []
        for i in range(self.populationSize):
            fuel = []
            time = []
            for j in range(len(self.population[i])-1):
                city_a = self.population[i][j]
                city_b = self.population[i][j+1]
                f = self.getFuel(city_a,city_b)
                fuel.append(f)
                t = self.getDuration(city_a,city_b)
                time.append(t)
            p.append([sum(fuel),sum(time)])
        return p

    def domSolutions(self, val, t):
        rank = 0
        for i in range(len(val)):
            if val[t][0] > val[i][0] and val[t][1] > val[i][1] and t!=i:
                rank += 2
            else:
                if val[t][0] > val[i][0] and t!=i:
                    rank += 1
                else:
                    if val[t][1] > val[i][1] and t!=i:
                        rank += 1
        return rank
    
    def nicheCount(self, p):
        nc = []
        for i in range(len(p)):
            suma = 0
            for j in range(len(p)):
                value = (self.nicheSize - self.euclideanDist(i,j,p)) / self.nicheSize
                if value > 0:
                    suma += value
                else: suma += 0
            nc.append(suma)
        return nc

    def euclideanDist(self, x, y, p):
        suma = 0
        # i - kriterines funkcijos numeris i=1 - fuel cost; i=2 - duration
        for i in range(2):
            suma += ( (p[x][i]-p[y][i]) / (self.findMax(i,p)-self.findMin(i,p)) )**2
        return math.sqrt(suma)

    def findMax(self, k, p):
        for i in range(len(p)):
            if p[i][k] > self.biggest[k]:
                self.biggest[k] = p[i][k]
        return self.biggest[k]

    def findMin(self, k, p):
        for i in range(len(p)):
            if p[i][k] < self.smallest[k]:
                self.smallest[k] = p[i][k]
        return self.smallest[k]

    def normalizingFitness(self, f1, f2):
        f = []
        for i in range(len(self.ranks)):
            suma = 0
            for j in range(len(self.ranks)):
                suma += f2[i]
            value = round((f2[i] / suma) * f1[i], 2)
            f.append(value)
        return f
    
    def getBest(self):
        max = 0
        index = 0
        for i in range(len(self.fit)):
            if(self.fit[i] > max):
                index = i
                max = self.fit[i]
        return self.population[index]
    
    def getBestRouteValues(self, p, fit):
        best = 0
        index = 0
        for i in range(len(fit)):
            if best < fit[i]:
                best = fit[i]
                index = i
            
        return p[index]
    
    def printResults(self, path1, path2, gen, executionTime):
        path1_fuelCost = self.findRouteFuelCost(path1)
        path1_duration = self.findRouteDuration(path1)
        path2_fuelCost = self.findRouteFuelCost(path2)
        path2_duration = self.findRouteDuration(path2)
        print("Best route 1: ", path1)
        print("Fuel cost: ", path1_fuelCost)
        print("Duration: ", path1_duration)
        print("Best route 2: ", path2)
        print("Fuel cost: ", path2_fuelCost)
        print("Duration: ", path2_duration)
        print("Generations: ", gen)
        print("Time: ", executionTime)

    def findRouteFuelCost(self, route):
        suma = 0
        for i in range(len(route)-1):
            city_a = route[i]
            city_b = route[i+1]
            d = self.getFuel(city_a,city_b)
            suma += d
        return suma

    def findRouteDuration(self, route):
        suma = 0
        for i in range(len(route)-1):
            city_a = route[i]
            city_b = route[i+1]
            d = self.getDuration(city_a,city_b)
            suma += d
        return suma

    def getMatingPool(self):
        print("\n")
        print("MatingPool = ")
        for i in range(len(self.matingPool)):
            print(self.matingPool[i])
            
    def getPopulation(self):
        print("\n")
        print("POPULATION = ")
        for i in range(len(self.population)):
            print(self.population[i])

class Plot:
    def __init__(self, pop):
        self.pop = pop
    
    def create(self, iterations, val, labelY):
        plt.title('Genetic algorithm')
        plt.plot(iterations, val)
        plt.xlabel('Generations')
        plt.ylabel(labelY)
        plt.grid(True)
        plt.show()

def findWorstValues(g):
    fuelSum = 0
    durationSum = 0
    for i in range(len(g)):
        worst_fuel = 0
        worst_duration = 0
        for j in range(len(g)):
            fuel_value = Population.getFuel(Population, g[i], g[j])
            duration_value = Population.getDuration(Population, g[i], g[j])
            if fuel_value > worst_fuel:
                worst_fuel = fuel_value
            if duration_value > worst_duration:
                worst_duration = duration_value
        fuelSum += worst_fuel
        durationSum += worst_duration
    return [fuelSum, durationSum]

def findRouteFuel(route):
    suma = 0
    for i in range(len(route)-1):
        city_a = route[i]
        city_b = route[i+1]
        d = Population.getFuel(Population, city_a, city_b)
        suma += d
    return suma

def findRouteDur(route):
    suma = 0
    for i in range(len(route)-1):
        city_a = route[i]
        city_b = route[i+1]
        d = Population.getDuration(Population, city_a, city_b)
        suma += d
    return suma

big = 0
small = 1000
def igd(geneticPareto, gaFuel, gaDuration, bb1_f, bb1_d, bb2_f, bb2_d):
    suma = 0
    [worstFuel, worstDuration] = findWorstValues(geneticPareto)
    fuelValue = (gaFuel - (bb1_f+bb2_f)/2)/(worstFuel-(bb1_f+bb2_f)/2)
    durationValue = (gaDuration - (bb1_d+bb2_d)/2)/(worstDuration-(bb1_d+bb2_d)/2)
    finalValue = (fuelValue + durationValue) / 2 
    return finalValue

def main():
    start = tm.time()
    executionTime = 0
    mutation = 0.001
    crossover = 0.6
    populationSize = 100
    generations = 100
    gen = generations+1
    pop = Population(populationSize, mutation, crossover)
    pop.create()
    iterations = []
    metrika = []
    final_fuel = float('inf')
    final_dur = float('inf')

    branchAndBound_result1 = ['Vilnius', 'Utena', 'Visaginas', 'Ukmergė', 'Panevėžys', 'Šiauliai', 'Mažeikiai', 'Telšiai', 'Plungė',
    'Kretinga', 'Klaipėda', 'Tauragė', 'Kėdainiai', 'Jonava', 'Kaunas', 'Marijampolė', 'Alytus', 'Vilnius']
    branchAndBound_result2 = ['Vilnius', 'Alytus', 'Marijampolė', 'Kaunas', 'Jonava', 'Kėdainiai', 'Tauragė', 'Klaipėda', 'Kretinga',
    'Plungė', 'Telšiai', 'Mažeikiai', 'Šiauliai', 'Panevėžys', 'Ukmergė', 'Utena', 'Visaginas', 'Vilnius']
    bb1_f = pop.findRouteFuelCost(branchAndBound_result1)
    bb1_d = pop.findRouteDuration(branchAndBound_result1)
    bb2_f = pop.findRouteFuelCost(branchAndBound_result2)
    bb2_d = pop.findRouteDuration(branchAndBound_result2)

    while generations > 0:
        fit = []
        iterations.append(gen-generations)
        fit = pop.fitnessEvaluation()
        p = pop.getPopulationWithValues()
        fuel = pop.getBestRouteValues(p, fit)[0]
        dur = pop.getBestRouteValues(p, fit)[1]
        if fuel < final_fuel:
            final_fuel = fuel
            path_f = pop.getBest()
        if dur < final_dur:
            final_dur = dur
            path_d = pop.getBest()
        pareto = pop.getBest()
        igdMetrika = igd(pareto, fuel, dur, bb1_f, bb1_d, bb2_f, bb2_d)
        metrika.append(igdMetrika)
        print(str(gen-generations) + " " + str(fuel) + " " + str(dur) + " " + str(igdMetrika))
        if(generations == 1 or (fuel == bb1_f and dur == bb1_d) or (fuel == bb2_f and dur == bb2_d) or (tm.time() - start) >=60):
            pop.printResults(path_f, path_d, gen-generations, (tm.time() - start))
            break
        else:
            matingPool = pop.naturalSelection()
            pop.reproduction(matingPool)
        generations-=1
    
    plot_Dist = Plot(pop)
    plot_Dist.create(iterations, metrika, "Metrika")
        
if __name__ == "__main__":
        main()