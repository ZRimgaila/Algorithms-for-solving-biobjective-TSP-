#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        data = """Vilnius, Kaunas, Klaipėda, Šiauliai, Panevėžys, Alytus, Marijampolė, Mažeikiai, Jonava, Utena, Kėdainiai, Tauragė, Telšiai, Ukmergė, Visaginas, Plungė, Kretinga, Palanga, Radviliškis, Šilutė, Vilnius"""
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
        api = "AIzaSyCPtz6n9Cuskc0rq8PHmSlvXiIMfG_MQ-w" 
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + start + "&destinations=" + stop + "&key=" + api
        link = requests.get(url)
        json_loc = link.json()
        d = json_loc['rows'][0]['elements'][0]['distance']['value']
        return d
    
    # Miestai ir kuro sąnaudos gauti iš Google MAPS API 
    def getFuel(self, cityA, cityB):
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
    def getDuration(self, cityA, cityB):
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
    
    def printResults(self, gen, executionTime):
        route = self.getBest()
        bestfuelCost = self.findRouteFuelCost(route)
        bestTime = self.findRouteDuration(route)
        print("Best route: ", route)
        print("Best route fuel cost: ", bestfuelCost)
        print("Best route time: ", bestTime)
        print("Generations: ", gen)
        print("Time: ", executionTime)
        return route

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
def igd(geneticPareto, gaFuel, gaDuration, bb_fuel, bb_duration):
    # inv = 1/perfect
    suma = 0
    [worstFuel, worstDuration] = findWorstValues(geneticPareto)
    fuelValue = (gaFuel - bb_fuel)/(worstFuel-bb_fuel)
    durationValue = (gaDuration - bb_duration)/(worstDuration-bb_duration)
    finalValue = (fuelValue + durationValue) / 2 
    return finalValue

def main():
    start = tm.time()
    executionTime = 0
    mutation = 0.005
    crossover = 0.7
    populationSize = 50
    generations = 40
    gen = generations+1
    pop = Population(populationSize, mutation, crossover)
    pop.create()
    iterations = []
    metrika = []
    branchAndBound_result = ['Vilnius', 'Kaunas', 'Alytus', 'Marijampolė', 'Tauragė', 'Šilutė', 'Klaipėda', 'Kretinga', 'Palanga', 'Plungė',
    'Telšiai', 'Mažeikiai', 'Šiauliai', 'Radviliškis', 'Panevėžys', 'Kėdainiai', 'Jonava', 'Ukmergė', 'Utena', 'Visaginas', 'Vilnius']
    bb_fuelCost = pop.findRouteFuelCost(branchAndBound_result)
    bb_duration = pop.findRouteDuration(branchAndBound_result)

    while generations > 0:
        fit = []
        iterations.append(gen-generations)
        fit = pop.fitnessEvaluation()
        p = pop.getPopulationWithValues()
        fuel = pop.getBestRouteValues(p, fit)[0]
        dur = pop.getBestRouteValues(p, fit)[1]
        pareto = pop.getBest()
        igdMetrika = igd(pareto, fuel, dur, bb_fuelCost, bb_duration)
        metrika.append(igdMetrika)
        print(str(gen-generations) + " " + str(fuel) + " " + str(dur) + " " + str(igdMetrika))
        if(generations == 1 or (fuel == 118.684 and dur == 1053)):
            pareto = pop.printResults(gen-generations, executionTime)
            break
        else:
            matingPool = pop.naturalSelection()
            pop.reproduction(matingPool)
        generations-=1
        executionTime = (tm.time() - start)
    
    plot_Dist = Plot(pop)
    plot_Dist.create(iterations, metrika, "Metrika")
        
if __name__ == "__main__":
        main()