# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 06:47:33 2021

@author: psusk
"""

import time
import math
import pygame
import random
import numpy as np
from queue import PriorityQueue

def findAdj(square):
    adj = []
    
    file = ord(square[0]) - 96
    rank = int(square[1])
    for i in [-2, -1, 1, 2]:
        rankOffset = [-1, 1] if abs(i) == 2 else [-2, 2]
        for j in rankOffset:
            if 0 < file + i < 9 and 0 < rank + j < 9:
                adj.append(chr(file + i + 96) + str(rank + j))
    random.shuffle(adj)
    return adj

class PQueue:
    enqueued = []
    dequeued = []
    
    def __init__(self):
        pass
    
    def enqueue(self, new):
        insert = -1
        improve = -1
        for index, element in enumerate(self.enqueued):
            if insert != -1 and improve != -1:
                break
            if insert == -1 and new[0] <= element[0]:
                insert = index
            if improve == -1 and new[1] == element[1]:
                if new[0] < element[0]:
                    improve = index
                else:
                    return
        if improve != -1:
            self.enqueued.pop(improve)
        if insert != -1:
            self.enqueued.insert(insert, new)
        else:
            self.enqueued.append(new)
        
    def dequeue(self):
        front = self.enqueued.pop(0)
        self.dequeued.append(front)
        return front
        
    def empty(self):
        return (len(self.enqueued) == 0)

class Vertex:
    def __init__(self, name='', adj=[], dist=0, heuristic=None):
        self.name = name
        self.adj = adj
        self.dist = dist
        self.heuristic = heuristic

def createGraph(dijkstra=False, aStar=False):
    graph = {}
    
    for file in range(97, 105):
        for rank in range(1, 9):
            name = chr(file) + str(rank)
            if dijkstra:
                graph.update({name : Vertex(name, findAdj(name), math.inf)})
            elif aStar:
                graph.update({name : Vertex(name, findAdj(name), math.inf, math.inf)})
            else:
                graph.update({name : findAdj(name)})
    #print(graph)
    return graph

def popVertex(graph, name):
    vertex = graph.pop(name)
    for adj in vertex.adj:
        graph[adj].adj.remove(name)
    return vertex

def drawSquare(gameDisplay, square, color, size):
    file = ord(square[0]) - 96
    rank = 9 - int(square[1])
    pygame.draw.rect(gameDisplay, color, [size * rank, size * file, size, size])
    pygame.display.update()
    time.sleep(0.1)

def drawBoard(gameDisplay, size):
    white, black = (255, 255, 255), (0, 0, 0)
    
    boardLength = 8
    gameDisplay.fill(white)
    
    for i in range(1, boardLength + 1):
        for j in range(1, boardLength + 1):
            if (i + j) % 2 == 0:
                pygame.draw.rect(gameDisplay, white,[size * j, size * i, size, size])
            else:
                pygame.draw.rect(gameDisplay, black, [size * j, size * i, size, size])

    pygame.draw.rect(gameDisplay, black, [size, size, boardLength * size, boardLength * size], 1)
    
    pygame.display.update()

def dijkstraVisual(start, destination, graph=createGraph(dijkstra=True)):
    assert start in graph, 'invalid start square.'
    assert destination in graph, 'invalid end square.'
    
    pygame.init()

    size = 100
    red, green, blue, gray = (255, 0, 0), (0, 255, 0), (0, 0, 255), (128, 128, 128)

    gameDisplay = pygame.display.set_mode((10 * size, 10 * size))
    pygame.display.set_caption("ChessBoard")
    
    drawBoard(gameDisplay, size)
    
    
    graph[start].dist = 0
    traversedCount = 0
    traverse = PQueue()
    
    traverse.enqueue((0, graph.get(start), None))
    drawSquare(gameDisplay, destination, green, size)
    while not traverse.empty():
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break
        
        currentVertex = popVertex(graph, traverse.dequeue()[1].name)
        print('\nqueue: ', [(t[0], t[1].name, t[2].name) for t in traverse.enqueued], '\n')
        print('current: ', vars(currentVertex))
        drawSquare(gameDisplay, currentVertex.name, red, size)
        for adj in currentVertex.adj:
            adjVertex = graph.get(adj)
            print('\tadjacent: ', vars(adjVertex))
            drawSquare(gameDisplay, adjVertex.name, blue, size)
            traversedCount += 1
            if adj == destination:
                #quit from pygame
                pygame.quit()
                return currentVertex.dist + 1, traversedCount
            
            adjVertex.dist = currentVertex.dist + 1
            traverse.enqueue((adjVertex.dist, adjVertex, currentVertex))
            
    #quit from pygame
    pygame.quit()
    return -1, traversedCount

def dijkstra(start, destination, graph=createGraph(dijkstra=True)):
    assert start in graph, 'invalid start square.'
    assert destination in graph, 'invalid end square.'
    graph[start].dist = 0
    
    traversedCount = 0
    traverse = PriorityQueue()
    
    traverse.put((0, 0, start))
    while not traverse.empty():
        currentVertex = popVertex(graph, traverse.get()[2])
        print(vars(currentVertex))
        for order, adj in enumerate(currentVertex.adj):
            adjVertex = graph.get(adj)
            traversedCount += 1
            if adj == destination:
                return currentVertex.dist + 1, traversedCount
            
            adjVertex.dist = currentVertex.dist + 1
            adjVertex.prev = currentVertex.name
            traverse.put((adjVertex.dist, order, adjVertex.name))
    return -1, traversedCount

def testRand():
    runs = 1000
    #cases = [("e4", "h2"), ("e4", "g1"), ("e4", "c1"), ("e4", "b2"), ("e4", "b6"), ("e4", "c7"), ("e4", "g7"), ("e4", "h6")]
    cases = [("e4", "c2"), ("e4", "c6"), ("e4", "g2"), ("e4", "g6")]
    counts = [0] * len(cases)
    for i in range(runs):
        for index, case in enumerate(cases):
            counts[index] += dijkstra(*case)[1]
    countsAvg = np.asarray(counts) / runs
    print(countsAvg)

#dijkstra("e4", "c6")
print(dijkstraVisual("e4", "c6"))