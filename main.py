from graph_tool.all import *

import math
import time
import tracemalloc

# import cairo
# import graphviz
# import os
# os.environ["PATH"] += os.pathsep + "c:/Program Files (x86)/Graphviz/bin"
# from graph_tool.all import *
# import graph_tool.all as gt
# import graph_tool.draw
# print(f"{dir(graph_tool.draw)}")
# from graph_tool.draw import graph_draw

stuff = {}
graph_tool.openmp_enabled()
'''********* Graph Creation **********'''
def createGraph(txt):
    g = graph_tool.Graph(directed=False)
    nodeColor = g.new_vertex_property("int")
    g.vertex_properties["color"] = nodeColor
    eWeight = g.new_edge_property("double")
    bot = g.add_vertex()
    stuff["bot"] = bot
    nodeColor[bot] = 10
    top = g.add_vertex()
    stuff["top"] = top
    nodeColor[top] = 11
    stuff["weight"] = eWeight
    
    with open(txt,'r') as file:
        lines = file.readlines()
        metadata = lines[0].strip().split()
        x = int(metadata[0])
        y = int(metadata[1])
        previousRow = {}
        preNode = ""
        firstrow = lines[1].strip().split()
        for i in range(x): #creates bottom row of structure
            current = g.add_vertex()
            nodeColor[current] = int(firstrow[i])
            outer = g.add_edge(current,bot)
            eWeight[outer] = 1.0
            if(i==0):
                preNode = current
                previousRow[0] = current
            else:
                num = int(firstrow[i])
                edge = g.add_edge(current,preNode)
                eWeight[edge] = 1.0
                previousRow[i] = current
                preNode = current
        # for edge in g.edges():
        #     print(edge)

        for a in range(y+1):
            if(a==0 or a==1): #skips over the metadata and the first row of the graph, since those two lines have already been processed
                continue
            row = lines[a].strip().split()
            currentRow = {}
            for i in range(x):
                currentNode = g.add_vertex()
                nodeColor[currentNode] = int(row[i])
                currentRow[i] = currentNode
                if(a==y):
                    outer1 = g.add_edge(currentNode,top)
                    eWeight[outer1] = 1.0
                if(i==0):
                    preNode = currentNode
                    edge = g.add_edge(currentNode,previousRow[i])
                    eWeight[edge] = 1.0
                    if(i+1<x):
                       edge = g.add_edge(currentNode,previousRow[i+1])
                       eWeight[edge] = math.sqrt(2)
                elif(i==x-1): #last element of a row
                    edge = g.add_edge(preNode,currentNode)
                    eWeight[edge] = 1.0
                    edge = g.add_edge(currentNode, previousRow[i])
                    eWeight[edge] = 1.0
                    edge = g.add_edge(currentNode, previousRow[i-1])
                    eWeight[edge] = math.sqrt(2)
                    previousRow = currentRow #resets previous row for the next row
                else:
                    edge = g.add_edge(currentNode,preNode)
                    eWeight[edge] = 1.0
                    edge = g.add_edge(currentNode,previousRow[i])
                    eWeight[edge] = 1.0
                    edge1 = g.add_edge(currentNode,previousRow[i-1])
                    eWeight[edge1] = math.sqrt(2)
                    edge2 = g.add_edge(currentNode,previousRow[i+1])
                    eWeight[edge2] = math.sqrt(2)
                    preNode = currentNode
    return g

g = createGraph('1000x1000.txt')

# print((time.time()-start_time))
# print(g.num_vertices)

'''********* Filtering the Graph **********'''
def edge_filter(e):
    return g.vertex_properties["color"][e.source()] == g.vertex_properties["color"][e.target()]

def vertex_filter(v):
    return True

# filter_time = time.time()
g_filtered = graph_tool.GraphView(g, vfilt=vertex_filter, efilt=edge_filter)

# # print(time.time()-filter_time)


# print(g_filtered.num_edges)
# # for edge in g_filtered.edges():
# #     print(edge)

'''********* BFS **********'''
# tracemalloc.start()
# snapshot1 = tracemalloc.take_snapshot()
# bfstime = time.time()

class VisitorExample(graph_tool.search.BFSVisitor):

    def __init__(self, name, pred, dist):
        self.name = name
        self.pred = pred
        self.dist = dist

    def discover_vertex(self, u):
        # print("-->", self.name[u], "has been discovered!")
        return

    def examine_vertex(self, u):
        # print(self.name[u], "has been examined...")
        return

    def tree_edge(self, e):
        self.pred[e.target()] = int(e.source())
        self.dist[e.target()] = self.dist[e.source()] + 1
vprop = g.new_vertex_property("int")
g.vertex_properties["vprop"] = vprop
interprop = g.vertex_properties["vprop"]

distBFS = g.new_vertex_property("int")
predBFS = g.new_vertex_property("int64_t")
graph_tool.search.bfs_search(g,stuff["bot"],VisitorExample(interprop,predBFS,distBFS))

# print(time.time()-bfstime)
# snapshot2 = tracemalloc.take_snapshot()
# stats = snapshot2.compare_to(snapshot1, 'lineno')
# for stat in stats[:5]:  # Limit to top 5 results
#     print(stat)
# print(distBFS.a)


'''********* Shortest path **********'''
tracemalloc.start()
snap1 = tracemalloc.take_snapshot()
start = time.time()
dist, pred = graph_tool.search.dijkstra_search(g,stuff["weight"],stuff["bot"])
print(time.time()-start)
snap2 = tracemalloc.take_snapshot()
stats = snap2.compare_to(snap1,'lineno')
for stat in stats[:5]:
    print(stat)
print(dist.a)






        


